module.exports = function(){
	// Publisher.  Need to write javascript bindings for processNode.py
	var zmq = require('zmq')
	  , sock = zmq.socket('pub');

	sock.bindSync('tcp://127.0.0.1:3000');
	console.log('Publisher bound to port 3000');

	//setInterval(function(){
	//  console.log('sending a multipart message envelope');
	//  sock.send(['kitty cats', 'meow!']);
	//}, 500);

	// Subscriber.  Need to write javascript bindings...
	sock.connect('tcp://127.0.0.1:3000');
	sock.subscribe('kitty cats');
	console.log('Subscriber connected to port 3000');

	sock.on('message', function(topic, message) {
	  console.log('received a message related to:', topic, 'containing message:', message);
	});	
}

