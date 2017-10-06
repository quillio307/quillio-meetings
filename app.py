from flask import Flask, render_template, abort, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms
from config import CONFIG_PATH
from setup import db
from mongoengine import errors
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True)
app.config.from_pyfile(CONFIG_PATH)
db.init_app(app)

from model.user import User
from model.meeting import Meeting

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/meeting/<user_id>/<room_id>')
def meeting_page(user_id, room_id):
    user = User.objects.with_id(user_id)
    meeting = Meeting.objects.with_id(room_id)
    if user is None or meeting is None:
        abort(404)

    return render_template('in_meeting.html', meeting={'title': meeting.name})


@socketio.on('join', namespace='/meetings')
def on_join(data):
    user = User.objects.with_id(data['user_id'])
    meeting = Meeting.objects.with_id(data['room_id'])
    if meeting.active is False:
        meeting.active = True
        meeting.save()
    join_room(data['room_id'])
    emit('receivemsg', {'data': data['user_id'] + ' has joined the meeting.'}, room=data['room_id'])

@socketio.on('silenceAll', namespace='/meetings')
def silence_all(data):
    emit('silence', {}, room=data['room'], include_self=False)
    emit('receivemsg', {'data': data['user'] + " is talking."}, room=data['room'])

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