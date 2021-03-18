var socket = io();
var password;
socket.on('to_client', function (data) {
	if (data['type'] == 'people') {
		list.innerHTML = '';
		for (var i = 0; i < data['people'].length; i++) {
			var elem = document.createElement('div');
			elem.textContent = data['people'][i];
			list.appendChild(elem);
		}
	} else if (data['type'] == 'verify') {
		if (data['result'] == true) {
			login_section.style.display = 'none';
			signed_in.style.display = 'block';
			options.style.display = 'block';
		} else {
			alert("Incorrect password!");
		}
	} else if (data['type'] == 'wait') {
		wait_text.style.display = 'block';
	} else if (data['type'] == 'in_list') {
		alert(data['name'] + " is already on the list!");
	} else if (data['type'] == 'not_found') {
		alert(data['name'] + " is not on the list!");
	}
})
function add() {
	socket.emit('to_server', {'type':'add','name':who.value,'pw':password});
}
function remove() {
	socket.emit('to_server', {'type':'remove','name':who.value,'pw':password});
}
function login() {
	password = pw_input.value;
	socket.emit('to_server', {'type':'verify','pw':password});
	socket.emit('to_server', {'type':'get'});
}
function skip() {
	login_section.style.display = 'none';
	signed_in.style.display = 'block';
	socket.emit('to_server', {'type':'get'});
}
