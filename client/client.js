var socket = io();
var password;
var fail = 0;
socket.on('to_client', function (data) {
	if (data['type'] == 'people') {
		list.innerHTML = '';
		for (var i = 0; i < data['people'].length; i++) {
			var elem = document.createElement('div');
			elem.textContent = data['people'][i];
			elem.classList.add('item');
			list.appendChild(elem);
		}
	} else if (data['type'] == 'verify') {
		if (data['result'] == true) {
			login_section.style.display = 'none';
			signed_in.style.display = 'block';
			options.style.display = 'block';
		} else {
			pw_input.classList.add('error');
			wait_text.textContent = "Incorrect Password";
			wait_text.style.opacity = '1';
		}
	} else if (data['type'] == 'wait') {
		pw_input.classList.add('error');
		wait_text.style.opacity = '1';
		wait_text.textContent = "Wait " + Math.round(data['wait_time']) + " seconds and retry";
		fail = Date.now() + data['wait_time'] * 1000;
		var int = setInterval(function () {
			wait_text.textContent = "Wait " + Math.round((fail - Date.now()) / 1000) + " seconds and retry";
			if (Math.round((fail - Date.now()) / 1000) <= 0) {
				pw_input.classList.remove('error');
				wait_text.style.opacity = '0';
				clearInterval(int);
			}
		}, 100);
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
