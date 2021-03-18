# Hello! The first part of the code is setting up
# a server, binding socket.io, and creating a routing
# function. After that, the program will set what
# happens when the server receives a socket.io
# event. Finally, the routing function will be
# attached to the server, and the server will start.

# Set up server

import time
from aiohttp import web
import socketio

# Create a new Async Socket IO Server
sio = socketio.AsyncServer()
# Create a new Aiohttp Web Application
app = web.Application()
# Bind the Socket.IO server to the Web App
# instance
sio.attach(app)



# Set up a routing function
async def routing(request):
	# "request" contains some information about
	# the get request. Below the "path" attribute
	# is used to get the exact path requested by
	# the client
	if request.path == '/':
		with open('client/client.html') as f:
			return web.Response(text=f.read(), content_type='text/html')
	elif request.path == '/client.js':
		with open('client/client.js') as f:
		    return web.Response(text=f.read(), content_type='text/javascript')


# This will detect when a message is received.
# All messages to the server are of type
# "to_server". The type attribute in the data
# defines the event type.

# A list of people on the list
people = []
pw = "a"
lastfail = 0

@sio.on('to_server')
async def event_to_server(sid, data):
	global lastfail
	global pw
	global people
	if data['type'] == 'get':
		await sio.emit('to_client', {'type':'people', 'people':people}, room=sid)
		return
	if not (lastfail < time.time() - 5):
		await sio.emit('to_client', {'type':'wait'}, room=sid)
		return
	if data['type'] == 'verify':
		EnteredPW = (data['pw'])
		if EnteredPW == pw:
			await sio.emit('to_client', {'type':'verify', 'result':True}, room=sid)
		else:
			lastfail = time.time()
			await sio.emit('to_client', {'type':'verify', 'result':False}, room=sid)
		return
	if data['pw'] == pw:
		# The password is correct
		if data['type'] == 'add':
			found = False
			for iteration in range(len(people)):
				if str(people[iteration]) == str(data['name']):
					found = True
			if not found: #checks if the person was already added to the list
				#The person is not in the list
				people.append(data['name'])
			else:
				await sio.emit('to_client', {'type':'in_list', 'name':data['name']}, room=sid)
		elif data['type'] == 'remove':
			# User requested to remove a person.
			found = False
			for iteration in range(len(people)):
				if str(people[iteration]) == str(data['name']):
					found = True
			if found:
				people.remove(str(data['name']))
			else:
				await sio.emit('to_client', {'type':'not_found', 'name':data['name']}, room=sid)
		# Every time an event is received, broadcast the list
		# of people to all clients
		await sio.emit('to_client', {'type':'people', 'people':people})
	else:
		lastfail = time.time()


# Attach routing function to server get request for "/"
# (the default page) and /client.js
app.router.add_get('/', routing)
app.router.add_get('/client.js', routing)

# Start the server
if __name__ == '__main__':
	# "__name__ == 'main'" will show if the file
	# is running directly and not imported.

	web.run_app(app)
