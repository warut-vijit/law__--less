function police_reports() {
    /* Boilerplate code */
    document.getElementById("extensionFrameTitle").innerHTML = "Twitter Analyst";
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
    writeElement("<b>UK Police Crime Records</b>");
    writeElement("<span style='min-width:120px'>Latitude</span><input placeholder='51.473747' type='text' id='lat'/><br/>");
    writeElement("<span style='min-width:120px'>Longitude</span><input placeholder='-0.092985' type='text' id='long'/><br/>");
    writeElement("<span style='min-width:120px'>Time</span><input placeholder='2013-01' type='text' id='date'/><br/>");
    writeElement("<input type='button' onclick='ask_api()' value='Submit'/>")
    writeElement("<p id='police_output'></p>");

    //Begin writing extension here.
}
function ask_api() {
    var lat = parseFloat(document.getElementById("lat").value);
    var long = parseFloat(document.getElementById("long").value);
    var time = document.getElementById("date").value
    var receiver = call_api_generic("https://data.police.uk/api/crimes-street/all-crime", {"poly":(lat+0.4)+','+(long+0.4)+':'+(lat-0.4)+','+(long+0.4)+':'+(lat-0.4)+','+(long-0.4)+':'+(lat+0.4)+','+(long-0.4),"date":time});
    if(receiver != "400" && receiver != "401" && receiver != "402" && receiver != "403" && receiver != "404" && receiver != "500" && receiver != "503"){
        document.getElementById('police_output').innerHTML = receiver;
    } else {
        document.getElementById('police_output').innerHTML = "Error occurred while processing API request: "+receiver;
    }
}