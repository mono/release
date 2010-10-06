String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim = function() {
	return this.replace(/^\s+/,"");
}
String.prototype.rtrim = function() {
	return this.replace(/\s+$/,"");
}

Array.prototype.indexOf = function(val) {
  for (var i=0;i<this.length;i++) {
    if (this[i] == val) return i;
  }
  return -1;
}

function txtServerName_Changed(server, admin, root)  {
    var txtServer = document.getElementById(server);
    var txtAdmin = document.getElementById(admin);
    var txtRoot = document.getElementById(root);
    if (txtServer.value.length > 0) {
        if (txtAdmin.value.length == 0) 
            txtAdmin.value = "web-admin@" + txtServer.value;
        if (txtRoot.value.length == 0) 
            txtRoot.value = "/srv/www/" + txtServer.value;   
    }  
}

function txtApplicationName_Changed(app, root)  {
    var txtApp = document.getElementById(app);
    var txtRoot = document.getElementById(root);
    if (txtRoot.value.length == 0) 
        txtRoot.value = "/srv/www/" + txtApp.value;     
}

function radApplicationType_Click(elm)  {
    if (elm.value == 'radVhost' && elm.checked) {
        setStyleByClass('vhost', 'display', 'inline');
        setStyleByClass('application', 'display', 'none');
    }  else {
        setStyleByClass('vhost', 'display', 'none');
        setStyleByClass('application', 'display', 'inline');
    } 
}

function setStyleByClass(className, attribute, value) {
  var elms = document.getElementsByClassName(className);
  for (j = 0; j < elms.length; j++) {
    elms[j].style[attribute] = value;
  }
}

function btnAddServerAlias_click() {
  var lstAliases = document.getElementById('lstServerAliases');
  var source = document.getElementById(lstAliases.getAttribute('sourcefield'));
  var values = document.getElementById(lstAliases.getAttribute('valuesfield'));
  var alias = source.value.trim();
  var aliases = (values.value.trim().length > 0) ? values.value.trim().split(",") : new Array();
  // reset list to value from global array
  if (alias.length > 0 && aliases.indexOf(alias) == -1) {  
      aliases.push(alias);
      values.value = aliases;
      rebuildAliasList();
  } 
  source.value = '';  
  source.focus();
}

function txtServerAlias_keypress(field, e) {
    var key = (e && e.which) ? e.which : window.event.keycode;    
    if(key == 13) {
        document.getElementById('btnAddServerAlias').click();
        return false;        
    } 
}

function removeAlias(val) {
  var lstAliases = document.getElementById('lstServerAliases');
  var source = document.getElementById(lstAliases.getAttribute('sourcefield'));
  var values = document.getElementById(lstAliases.getAttribute('valuesfield'));
  var aliases = values.value.split(",");
  for(var i=aliases.length-1; i>=0; i--) {
    if (aliases[i] == val) {
      aliases.splice(i,1);
    }
  }  
  values.value = aliases;
  rebuildAliasList();
}

function rebuildAliasList() {
  var lstAliases = document.getElementById('lstServerAliases');
  var source = document.getElementById(lstAliases.getAttribute('sourcefield'));
  var values = document.getElementById(lstAliases.getAttribute('valuesfield'));
  if (values.value.trim().length > 0) {
    var aliases = values.value.split(",");
    var innerHTML = '<table>'
    for (var i=0;i<aliases.length;i++) {
      innerHTML+="<tr><td>" + aliases[i] + "</td>";
      innerHTML+="<td align=\"right\"><a href=\"javascript:removeAlias('" + aliases[i] + "');\">Remove</a></td></tr>";
    }
    lstAliases.innerHTML = innerHTML;
  } else {
    lstAliases.innerHTML = '';
  }
}

