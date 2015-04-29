var zmq = require('zmq');

function extractProcessConfig(configFileContents, processName){
	console.log('configFile: ', configFileContents);
	var processArray = configFileContents.processList;
	var processConfig = {};

	// processArray.forEach(function(element){
	for (var i; i<processArray.length; i++){
		if (processName === processArray[i].processName){
			processConfig = processArray[i];
			break;
		}
	}

	return processConfig;
}
function convertIDToAddress(configFileContents, endPointID){
	var endPointIds = configFileContents.endPointIds;
	var address = '';
	// endPointIds.forEach(function(element){
	for (var i; i<endPointIds.length; i++){
		if (endPointID === endPointIds[i].id){
			address = endPointIds[i].address;
			break;
		}
	}
	return address;
}
function importConfig(configFilePath){
	fs = require('fs');
	fileContents = fs.readFileSync(configFilePath);
	return JSON.parse(fileContents);
}
function constuctSendMsg(inMessage){
	var newMsg = {
		'endPointAddress': endPointAddress,
		'contents': inObject
	};
	return JSON.stringify(newMsg);
}

exports.ZeroMQPublisherClass = function(inEndPointAddress){
	var sockPub = zmq.socket('pub');
	var path = require('path');
	var endPointAddress = inEndPointAddress;
	var logAdapter = require(path.resolve(__dirname,'logMessageAdapter.js'))(endPointAddress);

	function bind(newEndPointAddress){
		endPointAddress = newEndPointAddress;
		sockPub.bindSync(endPointAddress);
	}
	function importProcessConfig(configFilePath, publisherName){
		var fileContents = importConfig(configFilePath);
		var processConfig = extractProcessConfig(fileContents, publisherName);
		var processIDEnum = processConfig.endPoint;
		var endpoint = convertIDToAddress(fileContents, processIDEnum);
		bind(endpoint);
	}
	function logPubConnections(){

        logMsg = 'Binding to address ' + endPointAddress;
        send('log', logAdapter.genLogMessage(1, logMsg));
	}
	function send(topic, inObject){
		var newMsg = constructSendMsg(inObject);
		sockPub.send([topic, newMsg]);		
	}
	return {
		importProcessConfig: importProcessConfig,
		send: send
	};
};

exports.ZeroMQSubscriberClass = function(publisher){
	var sockSub = zmq.socket('sub');
	var path = require('path');
	var subscriptions = [];
	// Every subscriber is a publisher because of logging
	var sockPub = publisher;
	var logAdapter = require(path.resolve(__dirname,'logMessageAdapter.js'))(endPointAddress);
	var endPoint = '';

	function importProcessConfig(configFilePath, subscriberName){
		var fileContents = importConfig(configFilePath);
		var processConfig = extractProcessConfig(subscriberName);
		var processIDEnum = processConfig.endPoint;
		endpoint = convertIDToAddress(processIDEnum);

		subscriptions = processConfig.subscriptions;
        if (typeof subscriptions !== undefined){
            subscriptions.forEach(function(element){
            	sockSub.connect(convertIDToAddress(element.endPoint, endPointsIdsList));
            	if (typeof element.topics !== undefined){
            		element.topics.forEach(function(innerTopicElement){
            			sockSub.subscribe(innerTopicElement);
            			sockSub.setsockopt('subscribe', innerTopicElement);
            		});
            	}
            });
        }
	}

	function logSubConnections(){
		logMsg = 'Connecting to ';
		subscriptions.forEach(function(element){
			logMsg += element.endPoint + ' under the following topics: ';
			element.topics.forEach(function(topicElement){
				logMsg += topicElement + ' ';
			});
		});
        send('log', logAdapter.genLogMessage(1, logMsg));
	}

	function send(topic, inObject){
		var newMsg = constructSendMsg(inObject);
		sockPub.send([topic, newMsg]);		
	}

	function assignCallback(callback){
		sockSub.on('message', function(topic, message){
			// Don't know what to do with topic since that should be
			// automatically filtered by ZeroMQ
			topic = new Buffer(topic).toString('utf-8');
			message = new Buffer(message).toString('utf-8');
			message = JSON.parse(message);
			err = false;
			callback(err, message);	
		});
	}
	return {
		send: send,
		importProcessConfig: importProcessConfig,
		assignCallback: assignCallback
	}
};