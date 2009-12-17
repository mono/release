function create_cookie (name, value, days) {
	if (days) {
		var date = new Date ();
		date.setTime (date.getTime () + (days * 24 *60 * 60 * 1000));
		var expires = "; expires=" + date.toGMTString();
	} else {
	    var expires = "";
	}
	
	document.cookie = name + "=" + value + expires + "; path=/";
}

function read_cookie (name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split (';');
	
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
		    c = c.substring (1, c.length);
		}
		
		if (c.indexOf (nameEQ) == 0) {
		    return c.substring (nameEQ.length, c.length);
		}
	}
	
	return null;
}

function erase_cookie (name) 
{
	create_cookie (name, "", -1);
}

function toggle_toolbox (toolbox, link)
{
    if (toolbox.getStyle ("display") != "none") {
        link.innerHTML = "show";   
        toolbox.setStyle ("display: none");
        create_cookie ("wiki_toolbox_visible", "false", 60);
    } else {
        link.innerHTML = "hide";
        toolbox.setStyle ("display: block");
        create_cookie ("wiki_toolbox_visible", "true", 60);
    }
}

function install_toolbox_hack ()
{
    var link = $('utility-bar-toggle-link');
    var toolbox = $('utility-bar-contents');
    
    if (link && toolbox) {
        link.observe ('click', function () { 
            toggle_toolbox (toolbox, link); 
        });
        
        var show = read_cookie ("wiki_toolbox_visible");
        if (!show || show == "true") {
            toggle_toolbox (toolbox, link);
        } else {
            link.innerHTML = "show";
        }
    }
}

function install_toc_hack ()
{
    var toc = $('toc');
    var wrapper = $('wrapper');
    var content = $('content');
    var tocparent = $('toc-parent');
    
    if (toc && tocparent) {
        wrapper.removeClassName ('wide');
        content.removeClassName ('wide');
        
        toc = toc.remove ();
        tocparent.insert (toc);
        toc.setStyle ('display: block');
    }
}

function install_hacks ()
{
    install_toc_hack ();
    install_toolbox_hack ();
}

Event.observe (window, 'load', install_hacks);

