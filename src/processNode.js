module.exports = function(appNetworkConfig, processName, minLogLevel){
    path = require('path');
    scriptDir = path.dirname(module.filename);
    zeroMQInterface = require(path.join(scriptDir,'zeroMQInterface.js'));
    
    if (typeof(minLogLevel) === undefined){minLogLevel = 0;}
 
    var publisher = zeroMQInterface.ZeroMQPublisherClass();
    publisher.importProcessConfig(path.join(scriptDir,appNetworkConfig), processName);

    var subscriber = zeroMQInterface.ZeroMQSubscriberClass();
    // all subscribers are publishers for logging, so a reference to the publisher needs
    // to be passed in
    subscriber.setPublisherRef(publisher);
    subscriber.importProcessConfig(path.join(scriptDir,appNetworkConfig), processName);

    var pubEndpoint = publisher.getPublisherEndpoint();
    var logAdapter = require(path.join(scriptDir,'logMessageAdapter.js'))(pubEndpoint);

    publisher.logPubConnections();
    subscriber.logSubConnections();

    function send(topic, message){
        publisher.send(topic, message);
    }

    function onReceive(callback){
        return subscriber.assignCallback(callback);
    }

    function log(logLevel, message){
        if (logLevel >= minLogLevel){
            publisher.send('log', logAdapter.genLogMessage(logLevel, message));
        }
    }
    return{
        log: log,
        send: send,
        onReceive: onReceive
    };
};