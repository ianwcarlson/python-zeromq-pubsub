module.exports = function(){
	var express = require('express');
	var app = express();
	var http = require('http').Server(app);
	var io = require('socket.io')(http);
		// Publisher.  Need to write javascript bindings for processNode.py
	var zmq = require('zmq')
	  , sockPub = zmq.socket('pub');
	var pubEndPointAddress = 'tcp://127.0.0.1:5562';
	sockPub.bindSync(pubEndPointAddress);

	app.get('/', function(req, res){
	  console.log('sending index file');
	  res.sendFile(__dirname + '/index.html');
	});

	app.use(express.static(__dirname + '/dist'));

	io.on('connection', function(socket){
		console.log('connected to client');
		socket.on('chat message', function(msg){
			io.emit('chat message', msg);
		});
		socket.on('newPolygonPoints', function(newPolygonPoints){
			
			var newMsg = {};
			newMsg['endPointAddress'] = pubEndPointAddress;
			newMsg['contents'] = newPolygonPoints;
			console.log('sending new poly points: ', newMsg);
			sockPub.send(['newPolygonPoints', JSON.stringify(newMsg)]);
		});
	});

	http.listen(3698, function(){
	  console.log('listening on *:3698');
	});	

	// Subscriber.  Need to write javascript bindings...
	sockSubPolygon = zmq.socket('sub');
	sockSubPolygon.connect('tcp://127.0.0.1:5561');
	sockSubPolygon.subscribe('pointInPolygon');
	console.log('Subscriber connected to port 3000');
	pointInPolygon = false;

	sockSubPolygon.on('message', function(topic, message) {
		topic = new Buffer(topic).toString('utf-8');
		message = new Buffer(message).toString('utf-8');
		message = JSON.parse(message);
		console.log('received a message related to:', topic, 'containing message:', message);
		if (topic === 'pointInPolygon'){		
			if (message['contents'] != pointInPolygon){
				console.log('New polygon status!!!!!!!!!!!!!!!!!!!!!');
				io.emit('pointInPolygon', message['contents']);
				pointInPolygon = message['contents'];	
			}
		}		  
	});	

	sockSubGpsData = zmq.socket('sub');
	sockSubGpsData.connect('tcp://127.0.0.1:5550');
	sockSubGpsData.subscribe('gpsData');
	console.log('Subscriber connected to port 3000');

	sockSubGpsData.on('message', function(topic, message) {
		topic = new Buffer(topic).toString('utf-8');
		message = new Buffer(message).toString('utf-8');
		message = JSON.parse(message);
		//console.log('received a message related to:', topic, 'containing message:', message);
		if (topic == 'gpsData'){
			io.emit('newGpsPoint', message['contents']);
		}
	});
}
	