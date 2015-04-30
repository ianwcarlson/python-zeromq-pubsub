var zmq = require('zmq');

function extractProcessConfig(configFileContents, processName){

	var processArray = configFileContents.processList;
	var processConfig = {};
	var configFound = false;
	for (var i=0; i<processArray.length; i++){
		if (processName === processArray[i].processName){
			processConfig = processArray[i];
			configFound = true;
			break;
		}
	}
	if (!configFound){console.log('Process Config not found');}
	return processConfig;
}
function convertIDToAddress(configFileContents, endPointID){
	var endPointIds = configFileContents.endPointsIds;
	var address = '';
	var idFound = false;
	for (var i=0; i<endPointIds.length; i++){
		if (endPointID === endPointIds[i].id){
			address = endPointIds[i].address;
			idFound = true;
			break;
		}
	}
	if (!idFound){console.log('Endpoint ID not found');}

	return address;
}
function importConfig(configFilePath){
	fs = require('fs');
	fileContents = fs.readFileSync(configFilePath);
	return JSON.parse(fileContents);
}
function constructSendMsg(endPointAddress, inObject){
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
        var logLevel = 1;
        send('log', logAdapter.genLogMessage(logLevel, logMsg));
	}
	function send(topic, inObject){
		var newMsg = constructSendMsg(endPointAddress, inObject);
		sockPub.send([topic, newMsg]);		
	}
	function getPublisherEndpoint(){
		return endPointAddress;
	}
	return {
		importProcessConfig: importProcessConfig,
		logPubConnections: logPubConnections,
		send: send,
		getPublisherEndpoint: getPublisherEndpoint
	};
};

exports.ZeroMQSubscriberClass = function(publisher){
	var sockSub = zmq.socket('sub');
	var path = require('path');
	var subscriptions = [];
	// Every subscriber is a publisher because of logging
	var sockPub = publisher;
	var endPoint = '';
	var callback = null;

	sockSub.on('message', function(topic, message){
		// Don't know what to do with topic since that should be
		// automatically filtered by ZeroMQ
		topic = new Buffer(topic).toString('utf-8');
		message = new Buffer(message).toString('utf-8');
		message = JSON.parse(message);
		err = true;
		if (callback !== null){
			err = false;
			callback(err, message);	
		} else {
			console.log('Subscriber callback uninitialized');
		}
	});

	function importProcessConfig(configFilePath, subscriberName){
		var fileContents = importConfig(configFilePath);
		var processConfig = extractProcessConfig(fileContents, subscriberName);
		var processIDEnum = processConfig.endPoint;
		endpoint = convertIDToAddress(fileContents, processIDEnum);

		subscriptions = processConfig.subscriptions;
        if (typeof subscriptions !== undefined){
            subscriptions.forEach(function(element){
            	sockSub.connect(convertIDToAddress(fileContents, element.endPoint));
            	if (typeof element.topics !== undefined){
            		element.topics.forEach(function(innerTopicElement){
            			sockSub.subscribe(innerTopicElement);
            		});
            	}
            });
        }
	}

	function setPublisherRef(publisher){
		sockPub = publisher;
	}

	function logSubConnections(){
		var logAdapter = require(path.resolve(__dirname,'logMessageAdapter.js'))(endPoint);
		logMsg = 'Connecting to ';
		subscriptions.forEach(function(element){
			logMsg += element.endPoint + ' under the following topics: ';
			element.topics.forEach(function(topicElement){
				logMsg += topicElement + ' ';
			});
		});
		var logLevel = 1;
        send('log', logAdapter.genLogMessage(logLevel, logMsg));
	}

	function send(topic, inObject){
		var newMsg = constructSendMsg(endPoint, inObject);
		sockPub.send([topic, endPoint, newMsg]);		
	}

	function assignCallback(assignedCallback){
		callback = assignedCallback;
	}
	return {
		send: send,
		importProcessConfig: importProcessConfig,
		logSubConnections: logSubConnections,
		setPublisherRef: setPublisherRef,
		assignCallback: assignCallback
	};
};