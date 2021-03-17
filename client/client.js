var socket = io();
socket.emit('to_server', {"message":"Hello World!"});
socket.on('to_client', function (data) {
	console.log("Message received from server");
	console.log("Message data:", data);
})
