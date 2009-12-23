function NiftyCheck(){
    if(!document.getElementById || !document.createElement)
        return(false);
    isXHTML=/html\:/.test(document.getElementsByTagName('body')[0].nodeName);
    if(Array.prototype.push==null){Array.prototype.push=function(){
        this[this.length]=arguments[0]; return(this.length);}}
    return(true);
}

function Rounded(selector,wich,bk,color,opt){
    var i,prefixt,prefixb,cn="r",ecolor="",edges=false,eclass="",b=false,t=false;

    if(color=="transparent"){
        cn=cn+"x";
        ecolor=bk;
        bk="transparent";
    }
    else if(opt && opt.indexOf("border")>=0){
        var optar=opt.split(" ");
        for(i=0;i<optar.length;i++)
            if(optar[i].indexOf("#")>=0) ecolor=optar[i];
        if(ecolor=="") ecolor="#666";
        cn+="e";
        edges=true;
    }
    else if(opt && opt.indexOf("smooth")>=0){
        cn+="a";
        ecolor=Mix(bk,color);
    }
    if(opt && opt.indexOf("small")>=0) cn+="s";
    prefixt=cn;
    prefixb=cn;
    if(wich.indexOf("all")>=0){t=true;b=true}
    else if(wich.indexOf("top")>=0) t="true";
    else if(wich.indexOf("tl")>=0){
        t="true";
        if(wich.indexOf("tr")<0) prefixt+="l";
    }
    else if(wich.indexOf("tr")>=0){
        t="true";
        prefixt+="r";
    }
    if(wich.indexOf("bottom")>=0) b=true;
    else if(wich.indexOf("bl")>=0){
        b="true";
        if(wich.indexOf("br")<0) prefixb+="l";
    }
    else if(wich.indexOf("br")>=0){
        b="true";
        prefixb+="r";
    }
    var v=getElementsBySelector(selector);
    var l=v.length;
    for(i=0;i<l;i++){
        if(edges) AddBorder(v[i],ecolor);
        if(t) AddTop(v[i],bk,color,ecolor,prefixt);
        if(b) AddBottom(v[i],bk,color,ecolor,prefixb);
        if (v[i].classname != "") {
            v[i].classname += " rounded";
        } else {
            v[i].classname="rounded";
        }
    }
}

function AddBorder(el,bc){
    var i;
    if(!el.passed){
        if(el.childNodes.length==1 && el.childNodes[0].nodeType==3){
            var t=el.firstChild.nodeValue;
            el.removeChild(el.lastChild);
            var d=CreateEl("span");
            d.style.display="block";
            d.appendChild(document.createTextNode(t));
            el.appendChild(d);
        }
        for(i=0;i<el.childNodes.length;i++){
            if(el.childNodes[i].nodeType==1){
                el.childNodes[i].style.borderLeft="1px solid "+bc;
                el.childNodes[i].style.borderRight="1px solid "+bc;
            }
        }
    }
    el.passed=true;
}

function AddTop(el,bk,color,bc,cn){
    var i,lim=4,d=CreateEl("b");

    if(cn.indexOf("s")>=0) lim=2;
    if(bc) d.className="artop";
    else d.className="rtop";
    d.style.backgroundColor=bk;
    for(i=1;i<=lim;i++){
        var x=CreateEl("b");
        x.className=cn + i;
        x.style.backgroundColor=color;
        if(bc) x.style.borderColor=bc;
        d.appendChild(x);
    }
    el.style.paddingTop=0;
    el.insertBefore(d,el.firstChild);
}

function AddBottom(el,bk,color,bc,cn){
    var i,lim=4,d=CreateEl("b");

    if(cn.indexOf("s")>=0) lim=2;
    if(bc) d.className="artop";
    else d.className="rtop";
    d.style.backgroundColor=bk;
    for(i=lim;i>0;i--){
        var x=CreateEl("b");
        x.className=cn + i;
        x.style.backgroundColor=color;
        if(bc) x.style.borderColor=bc;
        d.appendChild(x);
    }
    el.style.paddingBottom=0;
    el.appendChild(d);
}

function CreateEl(x){
    if(isXHTML) return(document.createElementNS('http://www.w3.org/1999/xhtml',x));
    else return(document.createElement(x));
}

/*
   function getElementsBySelector(selector){
   var i,selid="",selclass="",tag=selector,f,s=[],objlist=[];

   if(selector.indexOf(" ")>0){  //descendant selector like "tag#id tag"
   s=selector.split(" ");
   var fs=s[0].split("#");
   if(fs.length==1) return(objlist);
   f=document.getElementById(fs[1]);
   if(f) return(f.getElementsByTagName(s[1]));
   return(objlist);
   }
   if(selector.indexOf("#")>0){ //id selector like "tag#id"
   s=selector.split("#");
   tag=s[0];
   selid=s[1];
   }
   if(selid!=""){
   f=document.getElementById(selid);
   if(f) objlist.push(f);
   return(objlist);
   }
   if(selector.indexOf(".")>0){  //class selector like "tag.class"
   s=selector.split(".");
   tag=s[0];
   selclass=s[1];
   }
   var v=document.getElementsByTagName(tag);  // tag selector like "tag"
   if(selclass=="")
   return(v);
   for(i=0;i<v.length;i++){
   if(v[i].className.indexOf(selclass)>=0){
   objlist.push(v[i]);
   }
   }
   return(objlist);
   }
 */

/* document.getElementsBySelector(selector)
   - returns an array of element objects from the current document
   matching the CSS selector. Selectors can contain element names, 
   class names and ids and can be nested. For example:

   elements = document.getElementsBySelect('div#main p a.external')

   Will return an array of all 'a' elements with 'external' in their 
   class attribute that are contained inside 'p' elements that are 
   contained inside the 'div' element which has id="main"

   New in version 0.4: Support for CSS2 and CSS3 attribute selectors:
   See http://www.w3.org/TR/css3-selectors/#attribute-selectors

   Version 0.4 - Simon Willison, March 25th 2003
   -- Works in Phoenix 0.5, Mozilla 1.3, Opera 7, Internet Explorer 6, Internet Explorer 5 on Windows
   -- Opera 7 fails 
 */

function getAllChildren(e) {
    // Returns all children of element. Workaround required for IE5/Windows. Ugh.
    return e.all ? e.all : e.getElementsByTagName('*');
}

function getElementsBySelector(selector) {
    // Attempt to fail gracefully in lesser browsers
    if (!document.getElementsByTagName) {
        return new Array();
    }
    // Split selector in to tokens
    var tokens = selector.split(' ');
    var currentContext = new Array(document);
    for (var i = 0; i < tokens.length; i++) {
        token = tokens[i].replace(/^\s+/,'').replace(/\s+$/,'');;
        if (token.indexOf('#') > -1) {
            // Token is an ID selector
            var bits = token.split('#');
            var tagName = bits[0];
            var id = bits[1];
            var element = document.getElementById(id);
            if (tagName && element.nodeName.toLowerCase() != tagName) {
                // tag with that ID not found, return false
                return new Array();
            }
            // Set currentContext to contain just this element
            currentContext = new Array(element);
            continue; // Skip to next token
        }
        if (token.indexOf('.') > -1) {
            // Token contains a class selector
            var bits = token.split('.');
            var tagName = bits[0];
            var className = bits[1];
            if (!tagName) {
                tagName = '*';
            }
            // Get elements matching tag, filter them for class selector
            var found = new Array;
            var foundCount = 0;
            for (var h = 0; h < currentContext.length; h++) {
                var elements;
                if (tagName == '*') {
                    elements = getAllChildren(currentContext[h]);
                } else {
                    elements = currentContext[h].getElementsByTagName(tagName);
                }
                for (var j = 0; j < elements.length; j++) {
                    found[foundCount++] = elements[j];
                }
            }
            currentContext = new Array;
            var currentContextIndex = 0;
            for (var k = 0; k < found.length; k++) {
                if (found[k].className && found[k].className.match(new RegExp('\\b'+className+'\\b'))) {
                    currentContext[currentContextIndex++] = found[k];
                }
            }
            continue; // Skip to next token
        }
        // Code to deal with attribute selectors
        if (token.match(/^(\w*)\[(\w+)([=~\|\^\$\*]?)=?"?([^\]"]*)"?\]$/)) {
            var tagName = RegExp.$1;
        var attrName = RegExp.$2;
        var attrOperator = RegExp.$3;
        var attrValue = RegExp.$4;
        if (!tagName) {
            tagName = '*';
        }
        // Grab all of the tagName elements within current context
        var found = new Array;
        var foundCount = 0;
        for (var h = 0; h < currentContext.length; h++) {
            var elements;
            if (tagName == '*') {
                elements = getAllChildren(currentContext[h]);
            } else {
                elements = currentContext[h].getElementsByTagName(tagName);
            }
            for (var j = 0; j < elements.length; j++) {
                found[foundCount++] = elements[j];
            }
        }
        currentContext = new Array;
        var currentContextIndex = 0;
        var checkFunction; // This function will be used to filter the elements
        switch (attrOperator) {
            case '=': // Equality
                checkFunction = function(e) { return (e.getAttribute(attrName) == attrValue); };
                break;
            case '~': // Match one of space seperated words 
                checkFunction = function(e) { return (e.getAttribute(attrName).match(new RegExp('\\b'+attrValue+'\\b'))); };
                break;
            case '|': // Match start with value followed by optional hyphen
                checkFunction = function(e) { return (e.getAttribute(attrName).match(new RegExp('^'+attrValue+'-?'))); };
                break;
            case '^': // Match starts with value
                checkFunction = function(e) { return (e.getAttribute(attrName).indexOf(attrValue) == 0); };
                break;
            case '$': // Match ends with value - fails with "Warning" in Opera 7
                checkFunction = function(e) { return (e.getAttribute(attrName).lastIndexOf(attrValue) == e.getAttribute(attrName).length - attrValue.length); };
                break;
            case '*': // Match ends with value
                checkFunction = function(e) { return (e.getAttribute(attrName).indexOf(attrValue) > -1); };
                break;
            default :
                // Just test for existence of attribute
                checkFunction = function(e) { return e.getAttribute(attrName); };
        }
        currentContext = new Array;
        var currentContextIndex = 0;
        for (var k = 0; k < found.length; k++) {
            if (checkFunction(found[k])) {
                currentContext[currentContextIndex++] = found[k];
            }
        }
        // alert('Attribute Selector: '+tagName+' '+attrName+' '+attrOperator+' '+attrValue);
        continue; // Skip to next token
    }
    // If we get here, token is JUST an element (not a class or ID selector)
    tagName = token;
    var found = new Array;
    var foundCount = 0;
    for (var h = 0; h < currentContext.length; h++) {
        var elements = currentContext[h].getElementsByTagName(tagName);
        for (var j = 0; j < elements.length; j++) {
            found[foundCount++] = elements[j];
        }
    }
    currentContext = found;
    }
    return currentContext;
}

/* That revolting regular expression explained 
   /^(\w+)\[(\w+)([=~\|\^\$\*]?)=?"?([^\]"]*)"?\]$/
   \---/  \---/\-------------/    \-------/
   |      |         |               |
   |      |         |           The value
   |      |    ~,|,^,$,* or =
   |   Attribute 
   Tag
 */


function Mix(c1,c2){
    var i,step1,step2,x,y,r=new Array(3);
    if(c1.length==4)step1=1;
    else step1=2;
    if(c2.length==4) step2=1;
    else step2=2;
    for(i=0;i<3;i++){
        x=parseInt(c1.substr(1+step1*i,step1),16);
        if(step1==1) x=16*x+x;
        y=parseInt(c2.substr(1+step2*i,step2),16);
        if(step2==1) y=16*y+y;
        r[i]=Math.floor((x*50+y*50)/100);
    }
    return("#"+r[0].toString(16)+r[1].toString(16)+r[2].toString(16));
}
