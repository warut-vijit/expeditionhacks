MAX_LAT = 30.49
MIN_LAT = 30.12
MAX_LONG = -97.55
MIN_LONG = -97.95
DIVISIONS = 90
def get_variations():
  data = []
  lat_div = (MAX_LAT - MIN_LAT)/DIVISIONS
  long_div = (MAX_LONG - MIN_LONG)/DIVISIONS 
  counter = 0
  with open('static/data/variation.txt') as f:
    for line in f:
      # get coords
      min_lat = MIN_LAT + lat_div * int(counter / DIVISIONS)
      max_lat = min_lat + lat_div
      min_long = MIN_LONG + long_div * (counter % DIVISIONS)
      max_long = min_long + long_div
      # read line
      variation = float(line);
      data.append( {
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_long': min_long,
        'max_long': max_long,
        'variation': variation
      } )
      counter+=1
  return data
