from app.extensions import socketio as sio
from flask_socketio import send, emit, join_room, leave_room, rooms
from flask import request
import json

users = {}

@sio.on('connect')
def handle_connect():
	print('Connected')

@sio.on('user_join')
def handle_user_join(data):
	room = int(data['room'])
	join_room(room)
	emit('room_join', data, to=room) # skip_sid=request.sid

@sio.on('user_message')
def handle_user_message(data):
	room = int(data['room'])
	emit('chat', data, to=room) # broadcast=True

@sio.on('user_leave')
def handle_user_leave(data):
	room = int(data['room'])
	emit('room_leave', data, to=room) # skip_sid=request.sid
	leave_room(room)

@sio.on('disconnect')
def disconnect():
	print('Client disconnected')

@sio.on_error()
def error_handler(e):
	try:
		del users[request.sid]
	except:
		pass
	print('socketio error:', e)


