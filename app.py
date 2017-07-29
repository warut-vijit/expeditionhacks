import os
from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('map.html', api_key=open('api.key').read())

if __name__=="__main__":
  port = int(os.environ.get('PORT', 5000))
  # run flask app
  app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
