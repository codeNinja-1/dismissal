var socket = io();
socket.on('to_client', function (data) {
	if (data['type'] == 'people') {
		list.innerHTML = '';
		for (var i = 0; i < data['people'].length; i++) {
			var elem = document.createElement('div');
			elem.textContent = data['people'][i];
			list.appendChild(elem);
		}
	}
})
function add() {
	socket.emit('to_server', {'type':'add','name':who.value});
}
function remove() {
	socket.emit('to_server', {'type':'remove','name':who.value});
}
