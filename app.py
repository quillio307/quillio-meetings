from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join', namespace='/meetings')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('receivemsg', {'data': username + ' has entered the room.'}, room=room)


@socketio.on('leave', namespace='/meetings')
def on_leave(data):
    username = data['username']
    room = data['room']
    emit('receivemsg', {'data':username + ' has left the room.'})
    leave_room(room)


@socketio.on('sendmsg', namespace='/meetings')
def test_message(message):
    username = message['username']
    room = message['room']
    emit('receivemsg', {'data': username+ ": " + message['data']}, room=room)


@socketio.on('connect', namespace='/meetings')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/meetings')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)