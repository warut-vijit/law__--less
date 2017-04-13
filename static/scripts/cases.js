var initialState = true;
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