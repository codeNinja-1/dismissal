# Hello! The first part of the code is setting up
# a server, binding socket.io, and creating a routing
# function. After that, the program will set what
# happens when the server receives a socket.io
# event. Finally, the routing function will be
# attached to the server, and the server will start.

# Set up server

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
# It will only detect messages called "to_server".
# The name can always be changed, though must be
# the same in both the client's and server's code.
@sio.on('to_server')
async def event_to_server(sid, data):

	# A message is received!  Print the socket id
	# (sid) of the client who sent the message.
	print("Message received from: ", sid)

	# The "data" parameter is used to transmit data
	# between a client and server. Please keep the
	# data parameter a dictionary/object.
	print("Message data: ", data['message'])

	# Here, a message is sent out to the client. The
	# message type is called "to_client". It can be renamed
	# just like the "to server message", though has to be
	# updated in both the client's and server's code.
	# The second parameter is for data being sent to
	# the client. Please keep the data parameter a
	# dictionary/object. The room attribute is for
	# transmitting the message to a single client only,
	# and has the socket id of the receiving client
	# inputted. Await is used here because the sio.emit
	# method is asynchronous
	await sio.emit('to_client', {'message':'Message received :)'}, room=sid)





# Attach routing function to server get request for "/"
# (the default page) and /client.js
app.router.add_get('/', routing)
app.router.add_get('/client.js', routing)

# Start the server
if __name__ == '__main__':
	# "__name__ == 'main'" will show if the file
	# is running directly and not imported.

	web.run_app(app)
