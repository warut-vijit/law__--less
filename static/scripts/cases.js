var initialState = true;
var clientID = Math.floor(Math.random()*1000000)+""
function call_api_generic(addr, params) {
    var address = addr+'?';
    for(var index=0;index<Object.keys(params).length;index++){
        if(index>0){address+="&";}
        address += Object.keys(params)[index]+"="+params[Object.keys(params)[index]]
    }
    var xhr = new XMLHttpRequest();
    xhr.open('GET', address);
    xhr.send(null);
    xhr.onreadystatechange = function () {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
        if (xhr.status === OK) {
        return xhr.responseText;
        }
    }
    };
}
function toggle_briefing () {
    if(initialState){
        get_target();
        initialState=false;
    }
    document.getElementById("output").style.display = document.getElementById("output").style.display == "none" ? "block" : "none";
}
function encryptxor (key, message) {
    var message_out = "";
    for(var x=0; x<message.length; x++){
        message_out += String.fromCharCode(message.charCodeAt(x) ^ key.charCodeAt(x%key.length));
    }
    return message_out;
}
function get_target() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get-target');
    xhr.send(null);
    xhr.onreadystatechange = function () {
        var DONE = 4; // readyState 4 means the request is done.
        var OK = 200; // status 200 is a successful return.
        if (xhr.readyState === DONE) {
            if (xhr.status === OK) {
                document.getElementById("output").innerHTML = encryptxor("imaginecup2017", xhr.responseText);
            }
        }
    };
}
function download() {
get_target();
var link = document.createElement("a");
link.href = 'data:text/plain;charset=utf-8,' + document.getElementById("output").innerHTML;
link.download = "law--less.txt";
link.click();
}