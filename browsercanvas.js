var OSName = "";
if (navigator.appVersion.indexOf("Win")!=-1) OSName="Windows";
if (navigator.appVersion.indexOf("Mac")!=-1) OSName="MacOS";
if (navigator.appVersion.indexOf("X11")!=-1) OSName="Linux";
if (navigator.appVersion.indexOf("Linux")!=-1) OSName="Linux";

function browsercanvas() 
{
	checkIfNeedsUpdate();

}




function handle_update_messages(messages) 
{
	reply=new Array();

	for(var i=0;i<messages.length; i++) {
		var message=messages[i];
		console.log(message);
		try {
			if ( typeof message == "string" ) {
				eval(message);
			}
		}
		catch(e) {
			reply.push(e);
		}
	}
	return reply;
}







function go_to_new_location()
{
	window.location = g_new_location;
}

function checkIfNeedsUpdate(reply) 
{
	if ( reply==undefined) reply=null
	new Ajax.Request('/needsupdate.dyn', {
		method:'post',
		parameters: "reply="+Object.toJSON(reply),
		onSuccess: function(transport){
            if (transport.status == 0) {
                console.info('Server shutdown...');
                return;
            }
			try {
			var response = transport.responseText.evalJSON();
			}
			catch (e) {
				checkIfNeedsUpdate(e);
				return;

			}
			//console.log("/needsupdate:"+transport.responseText);
			if ( response['new_url'] ) {
				// bug with new_url handling
				//alert("window.location="+response.new_url);
				//alert(transport.responseText);
				g_new_location =response.new_url;
				window.setTimeout(go_to_new_location, 100);
				//window.location=response.new_url;
				return;
			}
			var reply = handle_update_messages( response.messages);
			checkIfNeedsUpdate(reply);
		},
		onFailure: function(){ 
			console.error('Something went wrong...');
		 }
	});
}


