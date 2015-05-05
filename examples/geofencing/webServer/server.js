var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var path = require('path');
var pathToLib = path.resolve(__dirname,'..','..','..','..',
	'src','processNode.js');
var processNode = require(pathToLib)(pathToNetworkConfig, 
	nameOfProcess, 0);

var nameOfProcess = process.argv[2];
var pathToNetworkConfig = process.argv[3];

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

app.use(express.static(__dirname + '/dist'));

io.on('connection', function(socket){
	socket.on('newPolygonPoints', function(newPolygonPoints){			
		processNode.send(['newPolygonPoints', newMsg]);
	});
});

http.listen(3698, function(){
  console.log('listening on *:3698');
});	

pointInPolygon = false;
processNode.onReceive(function(err, topic, message){
	switch (topic){
		case ('pointInPolygon'):
			if (message['contents'] != pointInPolygon){
				io.emit('pointInPolygon', message['contents']);
				pointInPolygon = message['contents'];	
			}
			break;
		case ('gpsData'):
			io.emit('newGpsPoint', message['contents']);
			break;
		default:
			console.log('unrecognized topic');
	}
});	