module.exports = function(){
	var app = require('express')();
	var http = require('http').Server(app);
	var io = require('socket.io')(http);

	app.get('/', function(req, res){
	  console.log('sending index file');
	  res.sendFile(__dirname + '/index.html');
	});

	app.use(express.static('./'));

	io.on('connection', function(socket){
	  console.log('connected to client');
	  socket.on('chat message', function(msg){
	    io.emit('chat message', msg);
	  });
	});

	http.listen(3698, function(){
	  console.log('listening on *:3698');
	});	

	// Publisher.  Need to write javascript bindings for processNode.py
	var zmq = require('zmq')
	  , sockPub = zmq.socket('pub');

	sockPub.bindSync('tcp://127.0.0.1:5562');
	console.log('Web server bound to port 5562');

	io.on('newPolygonPoints', function(newPolygonPoints){
		sockPub.send(['newPolygonPoints', newPolygonPoints]);
	});

	// Subscriber.  Need to write javascript bindings...
	sockSubPolygon = zmq.socket('sub');
	sockSubPolygon.connect('tcp://127.0.0.1:5561');
	sockSubPolygon.subscribe('pointInPolygon');
	console.log('Subscriber connected to port 3000');
	pointInPolygon = false;

	sockSubPolygon.on('message', function(topic, message) {
		console.log('received a message related to:', topic, 'containing message:', message);
		if (topic === 'pointInPolygon'){		
			if (message['isPointInPolygon'] !== pointInPoly){
				io.emit('pointInPolygon', message['isPointInPolygon']);
				pointInPolygon = message['isPointInPolygon'];	
			}
		}		  
	});	

	sockSubGpsData = zmq.socket('sub');
	sockSubGpsData.connect('tcp://127.0.0.1:5550');
	sockSubGpsData.subscribe('pointInPoly');
	console.log('Subscriber connected to port 3000');

	sockSubGpsData.on('message', function(topic, message) {
		console.log('received a message related to:', topic, 'containing message:', message);
		if (topic == 'gpsData'){
			io.emit('newGpsPoint', message['contents']);
		}
	});
}
	