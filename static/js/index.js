(function () {
'use strict';

var app_id = "DemoAppId01082013GAL";
var app_code = "AJKnXv84fjrb0KIHawS0Tg";

// initialize communication with the platform
const platform = new H.service.Platform({
    app_id,
    app_code,
    useCIT: true,
    useHTTPS: true
});

const pixelRatio = devicePixelRatio > 1 ? 2 : 1;
let defaultLayers = platform.createDefaultLayers({
    tileSize: 256 * pixelRatio
});
const layers = platform.createDefaultLayers({
  tileSize: 256 * pixelRatio,
  ppi: pixelRatio > 1 ? 320 : 72
});

// initialize a map  - not specifying a location will give a whole world view.
let map = new H.Map(
    document.getElementsByClassName('dl-map')[0],
    defaultLayers.normal.basenight,
    {
        pixelRatio,
        center: new H.geo.Point(30.3, -97.7),
        zoom: 15
    }
);

// make the map interactive
const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
const ui = H.ui.UI.createDefault(map, layers);

// resize map on window resize
window.addEventListener('resize', function() {
    map.getViewPort().resize();
});

let provider = new H.datalens.RawDataProvider({
    dataUrl: 'http://localhost:5000/static/data/aggregated.csv',
    dataToFeatures: (data, helpers) => {
        let parsed = helpers.parseCSV(data);
        let features = [];
        console.log(parsed.length);
        for (let i = 1; i < parsed.length; i++) {
            let row = parsed[i];
            let feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [Number(row[6]), Number(row[5])]
                },
                "properties": {
                    "passenger_count": 10 //row[3]
                }
            };
            features.push(feature);
        }
        return features;
    },
    featuresToRows: (features, x, y, z, tileSize, helpers) => {
        let counts = {};
        for (let i = 0; i < features.length; i++) {
            let feature = features[i];
            let coordinates = feature.geometry.coordinates;
            let lng = coordinates[0];
            let lat = coordinates[1];

            let p = helpers.latLngToPixel(lat, lng, z, tileSize);
            let px = p[0];
            let py = p[1];
            let tx = px % tileSize;
            let ty = py % tileSize;
            let key = tx + '-' + ty;

            if (counts[key]) {
                counts[key] += 1;
            } else {
                counts[key] = 1;
            }
        }

        let rows = [];
        for (let key in counts) {
            let t = key.split('-');
            let tx = Number(t[0]);
            let ty = Number(t[1]);
            let count = counts[key];
            rows.push({tx, ty, count, value: count});
        }
        return rows;
    }
});

function viridisWithAlpha(t) {
    let c = d3.color(d3.interpolateViridis(t));
    c.opacity = d3.scaleLinear().domain([0, 0.05, 1]).range([0, 1, 1])(t);
    return c + '';
}

let baseCount = 10000;
let nonLinearity = 2;

// heatmap layer
let layer = new H.datalens.HeatmapLayer(provider, {
    rowToTilePoint: row => {
        return {
            x: row.tx,
            y: row.ty,
            count: row.count,
            value: row.count
        };
    },
    bandwidth: [{
        value: 1,
        zoom: 9
    }, {
        value: 10,
        zoom:16
    }],
    valueRange:  z => [0,baseCount/Math.pow(z,2 * nonLinearity)],
    countRange: [0, 0],
    opacity: 1,
    colorScale: viridisWithAlpha,
    aggregation: H.datalens.HeatmapLayer.Aggregation.SUM,
    inputScale: H.datalens.HeatmapLayer.InputScale.LINEAR
});

// add layer to map
map.addLayer(layer);

}());
