

function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function()
    {
    //    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    //        callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}

//refresh ACI token
function refTok() {
  console.log("Test refresh");

  console.log(httpGetAsync("/_api/refreshtoken"))
}

refTok()

setInterval(refTok, 60000);
