from flask import Flask, render_template,request, Response, stream_with_context, jsonify
import random, logging
from redis import Redis
import os, time, json


db = Redis(host='redis', port=6379)

app = Flask(__name__)
#app.logger.addHandler(logging.StreamHandler())
#app.logger.setLevel(logging.INFO)

images_path = 'data/images.txt'
try:
    with open(images_path,'r') as images_file:
        images = images_file.read().splitlines()
except:
    app.logger.warning('Unable to load {images} - falling back to default list'.format(images=images_path))
    # Default list of cat images courtesy of buzzfeed
    images = [
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26388-1381844103-11.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr01/15/9/anigif_enhanced-buzz-31540-1381844535-8.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26390-1381844163-18.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-1376-1381846217-0.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3391-1381844336-26.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-29111-1381845968-0.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3409-1381844582-13.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr02/15/9/anigif_enhanced-buzz-19667-1381844937-10.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26358-1381845043-13.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-18774-1381844645-6.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-25158-1381844793-0.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/10/anigif_enhanced-buzz-11980-1381846269-1.gif"
    ]

@app.route('/randomCat')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)
@app.route('/')
def home():
    return ("There is no place like 127.0.0.1")

@app.route('/count')
def hello():
    db.incr('count')
    return 'Count is %s.' % db.get('count')

@app.route('/<path:path>', methods = ['PUT', 'GET'])
def homehome(path):

    if (request.method == 'PUT'):
       event = request.json
       event['last_updated'] = int(time.time())
       event['ttl'] = ttl
       db.delete(path) #remove old keys
       db.hmset(path, event)
       db.expire(path, ttl)
       return flask.jsonify(event), 201


    if not db.exists(path):
        return "Error: thing doesn't exist"

    event = db.hgetall(path)
    event["ttl"] = db.ttl(path)
    return flask.jsonify(event), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)