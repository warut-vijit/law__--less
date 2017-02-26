function state_laws() {
    /* Boilerplate code */
    document.getElementById("extensionFrameTitle").innerHTML = "State Laws";
    document.getElementById("extensionFrame").style.display = "block";
    document.getElementById("extensionFrame").style.color = "black";
    function write(text) {
        document.getElementById("extensionFrame").innerHTML += "<span>"+text+"</span>";
    }
    function writeln(text) {
        document.getElementById("extensionFrame").innerHTML += "<span>"+text+"</span>\n";
    }
    function writeElement(elmnt) {
        document.getElementById("extensionFrame").innerHTML += "<center>\n"+elmnt+"\n</center>\n";
    }
    /* End boilerplate code */
    //Begin writing extension here.
}