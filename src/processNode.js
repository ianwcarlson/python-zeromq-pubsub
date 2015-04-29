module.exports = function(appNetworkConfig, processName, minLogLevel){
    path = require('path');
    scriptDir = __dirname;
    zeroMQInterface = require(path.resolve(scriptDir,'zeroMQInterface.js'));
    
    if (typeof(minLogLevel) === undefined){minLogLevel = 0;}
 
    var publisher = zeroMQInterface.ZeroMQPublisherClass();
    publisher.importProcessConfig(path.resolve(scriptDir,appNetworkConfig), processName);

    var subscriber = zeroMQInterface.ZeroMQSubscriberClass();
    // all subscribers are publishers for logging, so a reference to the publisher needs
    // to be passed in
    subscriber.setPublisherRef(publisher);
    subscriber.importProcessConfig(path.resolve(scriptDir,appNetworkConfig), processName);

    // minLogLevel = minLogLevel;
    var logAdapter = logMessageAdapter.LogMessageAdapter(processName);

    // need to wait until zeroMQ socket connections establish, otherwise
    // messages will be initially lost
    // time.sleep(1)

    publisher.logPubConnections();
    subscriber.logSubConnections();

    function send(topic, message){
        publisher.send(topic, message);
    }

    function onReceive(callback){
        return subscriber.assignCallback();
    }

    function log(logLevel, message){
        if (logLevel >= minLogLevel){
            publisher.send('log', logAdapter.genLogMessage(logLevel, message));
        }
    }
    return{
        log: log,
        send: send,
        receive: receive
    }
};