module.exports = function(inPubID){
    var pubID = inPubID;

    function genLogMessage(logLevel, message){
        return {
            'pubID': pubID,
            'logLevel': logLevel,
            'message': message
        };
    }
    return{
        genLogMessage: genLogMessage
    };
};
