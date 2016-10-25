import controller
import threading

from flask import Flask, render_template, request

app = Flask(__name__)
params = None

def initialize(_params):
    global params
    params=_params

@app.route("/")
def main():   
    templateData = {
      'playback' : params.pause
      }
    
    return render_template('main.html',**templateData)

@app.route("/play")
def togglePause():
    global params 
    controller.togglePause()

    templateData = {
      'playback' : params.pause
      }
    
    return render_template('main.html',**templateData)

@app.route("/volup")
def volup():
    global params 
    controller.volUp()

    templateData = {
      'playback' : params.pause
      }
    
    return render_template('main.html',**templateData)

@app.route("/voldown")
def voldown():
    global params 
    controller.volDown()

    templateData = {
      'playback' : params.pause
      }
    
    return render_template('main.html',**templateData)
    

def run():
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
    print('Server started')
    return

@app.route("/shutdown")
def shutdown_server():
    controller.stopPlayback()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running the Werkzeug Server')
    func()

 

    
