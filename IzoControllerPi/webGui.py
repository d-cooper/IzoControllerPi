import controller
import threading

from parameters import Params
from flask import Flask, render_template, request

app = Flask(__name__);

params = None

def initialize(_params):
    global params
    params=_params

@app.route("/")
def main():
    templateData = {
      'pause': params.pause,
      'volume': params.volume,
      'page': 'main'
      }
    
    return render_template('main.html',**templateData)

@app.route("/showlog")
def showlog():
    with open('/home/pi/Desktop/IzoControllerPi/log.txt','r') as myfile:
        log=myfile.read()
    templateData = {
      'pause': params.pause,
      'volume': params.volume,
      'log':   log,
      'page': 'log'
      }
    
    return render_template('main.html',**templateData)


@app.route("/play")
def togglePause():
    global params 
    controller.togglePause()

    templateData = {
      'pause' : params.pause,
      'volume': params.volume,
      'page': 'main'
      }
    
    return render_template('main.html',**templateData)

@app.route("/volup")
def volup():
    global params 
    controller.volUp()

    templateData = {
      'pause' : params.pause,
      'volume': params.volume,
      'page': 'main'
      }
    
    return render_template('main.html',**templateData)

@app.route("/voldown")
def voldown():
    global params 
    controller.volDown()

    templateData = {
      'pause' : params.pause,
      'volume': params.volume,
      'page': 'main'
      }
    
    return render_template('main.html',**templateData)
    

def run():
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
    print('Server started')
    return

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running the Werkzeug Server')
    func()
    
@app.route('/shutdown')
def shutdown():
    controller.stopPlayback()
    shutdown_server()
    return 'Server shut down'

    
