var OSName = "";
if (navigator.appVersion.indexOf("Win")!=-1) OSName="Windows";
if (navigator.appVersion.indexOf("Mac")!=-1) OSName="MacOS";
if (navigator.appVersion.indexOf("X11")!=-1) OSName="Linux";
if (navigator.appVersion.indexOf("Linux")!=-1) OSName="Linux";

function browsercanvas() 
{
	console.log(OSName);
	checkIfNeedsUpdate();

}




function handle_update_messages(messages) 
{

	for(var i=0;i<messages.length; i++) {
		var message=messages[i];
		console.log(message);
		try {
			eval(message);
		}
		catch(e) {
			console.log(e);
		}
	}
}







function go_to_new_location()
{
	window.location = g_new_location;
}

function checkIfNeedsUpdate() 
{
	new Ajax.Request('/needsupdate.dyn', {
		method:'get',
		onSuccess: function(transport){
            if (transport.status == 0) {
                console.info('Server shutdown...');
                return;
            }
			try {
			var response = transport.responseText.evalJSON();
			}
			catch (e) {
				console.warn("illegal json", e);
				checkIfNeedsUpdate();
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
			handle_update_messages( response.messages);


			checkIfNeedsUpdate();
		},
		onFailure: function(){ 
			console.error('Something went wrong...');
		 }
	});
}


