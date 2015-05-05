var zmq = require('zmq');
var path = require('path');
var pathToLib = path.resolve(__dirname,'..','..','src','processNode.js');

var nameOfProcess = process.argv[2];
var pathToNetworkConfig = process.argv[3];

var processNode = require(pathToLib)(pathToNetworkConfig, nameOfProcess, 0);
processNode.onReceive(function(err, topic, message){
	processNode.send('fromNode', message.contents);
});