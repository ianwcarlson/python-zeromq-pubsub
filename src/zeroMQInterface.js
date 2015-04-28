var zmq = require('zmq')

function extractProcessConfig(configFileContents, processName){
	var processArray = configFileContents.processList;
	var processConfig = {};

	processArray.forEach(function(element){
		if (processName === element.processName){
			processConfig = element;
			break;
		}
	});

	return processConfig;
}
function convertIDToAddress(configFileContents, endPointID){
	var endPointIds = configFileContents.endPointIds;
	var address = '';
	endPointIds.forEach(function(element){
		if (endPointID === element.id){
			address = element.address;
			break;
		}
	});
	return address;
}
function importConfig(configFilePath){
	fs = require('fs');
	fileContents = fs.readFileSync(configFilePath);
	return JSON.parse(fileContents);
}
function ZeroMQPublisherClass(endPointAddress){
	var sockPub = zmq.socket('pub');
	var endPointAddress = endPointAddress;

	function bind(newEndPointAddress){
		endPointAddress = newEndPointAddress
		sockPub.bindSync(endPointAddress);
	}
	function importProcessConfig(configFilePath, publisherName){
		var fileContents = importConfig(configFilePath);
		var processConfig = extractProcessConfig(publisherName);
		var processIDEnum = processConfig.endPoint;
		var endpoint = convertIDToAddress(processIDEnum);
		bind(endpoint);
	}
	function logPubConnections(){

	}
	function send(topic, inObject){
		var newMsg = {};
		newMsg['endPointAddress'] = endPointAddress;
		newMsg['contents'] = inObject;
		sockPub.send([topic, JSON.stringify(newMsg)]);		
	}
	return {
		importProcessConfig: importProcessConfig,
		send: send
	}
}