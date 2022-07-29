from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
socketio = SocketManager(app=app, cors_allowed_origins="*")

html="""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title></title>
  </head>
  <body>

    <ul id="messages"></ul>
    <input id="myMessage" type="text">
    <button id="send">Send</button>

    <script
      src="http://code.jquery.com/jquery-3.3.1.min.js"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
    crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.js"></script>
  <script>
    const socket = io();


    socket.emit('message', 'hello');

    socket.on('message', function(msg) {
      $('#messages').append('<li>' + msg + '</li>');
    });

    $('#send').on('click', function() {
      socket.send($('#myMessage').val());
      $('#myMessage').val('');
    });
  </script>
</body>
</html>
"""

@app.get("/")
def index():
    return HTMLResponse(html)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    socketio.send(msg)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)