import os
import logging
from flask import Flask, jsonify, request, render_template, redirect
from events import get_events

app = Flask(__name__)

@app.route('/')
def home():
  event_markers = get_events()
  return render_template('map.html', markers=event_markers)

@app.route('/events')
def events():
  return jsonify(get_events())

if __name__=="__main__":
  port = int(os.environ.get('PORT', 5000))
  # run flask app
  app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
