var zmq = require('zmq');
var path = require('path');
var pathToLib = path.resolve(__dirname,'..','..','src','processNode.js');

var pathToNetworkConfig = process.argv[2];
var nameOfProcess = process.argv[3];

var processNode = require(pathToLib)(pathToNetworkConfig, nameOfProcess, 0);

processNode.onReceive(function(err, message){
	console.log('message: ', message);
	processNode.send('fromNode', message);
});