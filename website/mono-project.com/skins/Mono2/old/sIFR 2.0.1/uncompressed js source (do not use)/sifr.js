/*	sIFR v2.0.1 SOURCE
	Copyright 2004 - 2005 Mike Davidson, Shaun Inman, Tomas Jogin and Mark Wubben

	This software is licensed under the CC-GNU LGPL <http://creativecommons.org/licenses/LGPL/2.1/>
*/

var hasFlash = function(){
	var nRequiredVersion = 6;	
	
	if(navigator.appVersion.indexOf("MSIE") != -1 && navigator.appVersion.indexOf("Windows") > -1){
		document.write('<script language="VBScript"\> \non error resume next \nhasFlash = (IsObject(CreateObject("ShockwaveFlash.ShockwaveFlash." & ' + nRequiredVersion + '))) \n</script\> \n');
		/*	If executed, the VBScript above checks for Flash and sets the hasFlash variable. 
			If VBScript is not supported it's value will still be undefined, so we'll run it though another test
			This will make sure even Opera identified as IE will be tested */
		if(window.hasFlash != null){
			return window.hasFlash;
		};
	};
	
	if(navigator.mimeTypes && navigator.mimeTypes["application/x-shockwave-flash"] && navigator.mimeTypes["application/x-shockwave-flash"].enabledPlugin){
		var flashDescription = (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]).description;
		return parseInt(flashDescription.charAt(flashDescription.indexOf(".") - 1)) >= nRequiredVersion;
	};
	
	return false;
}();

String.prototype.normalize = function(){
	return this.replace(/\s+/g, " ");
};

/* IE 5.0 does not support the push method, so here goes */
if(Array.prototype.push == null){
	Array.prototype.push = function(){
		var i = 0, index = this.length, limit = arguments.length;
		while(i < limit){
			this[index++] = arguments[i++];
		};
		return this.length;
	};
};

/*	Implement function.apply for browsers which don't support it natively
	Courtesy of Aaron Boodman - http://youngpup.net */
if (!Function.prototype.apply){
	Function.prototype.apply = function(oScope, args) {
		var sarg = [];
		var rtrn, call;

		if (!oScope) oScope = window;
		if (!args) args = [];

		for (var i = 0; i < args.length; i++) {
			sarg[i] = "args["+i+"]";
		};

		call = "oScope.__applyTemp__(" + sarg.join(",") + ");";

		oScope.__applyTemp__ = this;
		rtrn = eval(call);
		oScope.__applyTemp__ = null;
		return rtrn;
	};
};

/*	The following code parses CSS selectors.
	This script however is not the right place to explain it,
	please visit the documentation for more information. */
var parseSelector = function(){
	var reParseSelector = /^([^#.>`]*)(#|\.|\>|\`)(.+)$/;
	function parseSelector(sSelector, oParentNode){
		var listSelectors = sSelector.split(/\s*\,\s*/);
		var listReturn = [];
		for(var i = 0; i < listSelectors.length; i++){
			listReturn = listReturn.concat(doParse(listSelectors[i], oParentNode));
		};
		
		return listReturn;
	};
	
	function doParse(sSelector, oParentNode, sMode){
		sSelector = sSelector.replace(" ", "`");
		var selector = sSelector.match(reParseSelector);
		var node, listNodes, listSubNodes, subselector, i, limit;
		var listReturn = [];
		
		if(selector == null){ selector = [sSelector, sSelector] };
		if(selector[1] == ""){ selector[1] = "*" };
		if(sMode == null){ sMode = "`" };
		if(oParentNode == null){
			oParentNode = document;
		};

		switch(selector[2]){
			case "#":
				subselector = selector[3].match(reParseSelector);
				if(subselector == null){ subselector = [null, selector[3]] };
				node = 	document.getElementById(subselector[1]);
				if(node == null || (selector[1] != "*" && !matchNodeNames(node, selector[1]))){
					return listReturn;
				};
				if(subselector.length == 2){
					listReturn.push(node);
					return listReturn;	
				};
				return doParse(subselector[3], node, subselector[2]);
			case ".":
				if(sMode != ">"){
					listNodes = getElementsByTagName(oParentNode, selector[1]);
				} else {
					listNodes = oParentNode.childNodes;
				};
				
				for(i = 0, limit = listNodes.length; i < limit; i++){
					node = listNodes[i];
					if(node.nodeType != 1){
						continue;	
					};
					subselector = selector[3].match(reParseSelector);
					if(subselector != null){
						if(node.className == null || node.className.match("\\b" + subselector[1] + "\\b") == null){
							continue;
						};
						listSubNodes = doParse(subselector[3], node, subselector[2]);
						listReturn = listReturn.concat(listSubNodes);	
					} else if(node.className != null && node.className.match("\\b" + selector[3] + "\\b") != null){
						listReturn.push(node);
					};
				};
				return listReturn;
			case ">":
				if(sMode != ">"){
					listNodes = getElementsByTagName(oParentNode, selector[1]);
				} else {
					listNodes = oParentNode.childNodes;
				};
								
				for(i = 0, limit = listNodes.length; i < limit; i++){
					node = listNodes[i];
					
					if(node.nodeType != 1){
						continue;	
					};
					
					if(!matchNodeNames(node, selector[1])){
						continue;
					};
					listSubNodes = doParse(selector[3], node, ">");
					listReturn = listReturn.concat(listSubNodes);	
				};
				return listReturn;
			case "`":
				listNodes = getElementsByTagName(oParentNode, selector[1]);
				for(i = 0, limit = listNodes.length; i < limit; i++){
					node = listNodes[i];
					listSubNodes = doParse(selector[3], node, "`");
					listReturn = listReturn.concat(listSubNodes);	
				};
				return listReturn;
			default:
				if(sMode != ">"){
					listNodes = getElementsByTagName(oParentNode, selector[1]);
				} else {
					listNodes = oParentNode.childNodes;
				};

				for(i = 0, limit = listNodes.length; i < limit; i++){
					node = listNodes[i];
					if(node.nodeType != 1){
						continue;	
					};
					if(!matchNodeNames(node, selector[1])){
						continue;
					};
					listReturn.push(node);
				};
				return listReturn;
		};
	};
	
	function getElementsByTagName(oParentNode, sTagName){
		/*	IE5.x does not support document.getElementsByTagName("*")
			therefore we're falling back to element.all */
		if(sTagName == "*" && oParentNode.all != null){
			return oParentNode.all;
		};
		return oParentNode.getElementsByTagName(sTagName);
	};
	
	function matchNodeNames(node, sMatch){
		if(sMatch == "*"){
			return true;
		};
		return node.nodeName.toLowerCase().replace("html:", "") == sMatch.toLowerCase();
	};
	
	return parseSelector;
}();

/*	Adds named arguments support to JavaScript. */
function named(oArgs){ 
	return new named.Arguments(oArgs);
};

named.Arguments = function(oArgs){
	this.oArgs = oArgs;
};

named.Arguments.prototype.constructor = named.Arguments;

named.extract = function(listPassedArgs, oMapping){
	var oNamedArgs, passedArg;
	
	var i = listPassedArgs.length;
	while(i--){
		passedArg = listPassedArgs[i];
		if(passedArg != null && passedArg.constructor != null && passedArg.constructor == named.Arguments){
			oNamedArgs = listPassedArgs[i].oArgs; /* oNamedArgs isn't the named.Arguments class! */
			break;
		};
	};

	if(oNamedArgs == null){ return };
	
	for(sName in oNamedArgs){
		if(oMapping[sName] != null){
			oMapping[sName](oNamedArgs[sName]);
		};
	};
	
	return;
};

/*	Executes an anonymous function which returns the function sIFR (defined inside the function).
	You can replace elements using sIFR.replaceElement()
	All other variables and methods you see are private. If you want to understand how this works you should
	learn more about the variable-scope in JavaScript. */
var sIFR = function(){
	/* Opera and Mozilla require a namespace when creating elements in an XML page */
	var sNameSpaceURI = "http://www.w3.org/1999/xhtml";
	var bIsInitialized = false;
	var bIsSetUp = false;
	var bInnerHTMLTested = false;
	var sDocumentTitle;
	var stackReplaceElementArguments = [];
	var UA = function(){
		var sUA = navigator.userAgent.toLowerCase();
		var oReturn =  {
			bIsWebKit : sUA.indexOf("applewebkit") > -1,
			bIsSafari : sUA.indexOf("safari") > -1,
			bIsKonq: navigator.product != null && navigator.product.toLowerCase().indexOf("konqueror") > -1,
			bIsOpera : sUA.indexOf("opera") > -1,
			bIsXML : document.contentType != null && document.contentType.indexOf("xml") > -1,
			bHasTransparencySupport : true,
			bUseDOM : true,
			nFlashVersion : null,
			nOperaVersion : null,
			nGeckoBuildDate : null,
			nWebKitVersion : null
		};
		
		oReturn.bIsKHTML = oReturn.bIsWebKit || oReturn.bIsKonq;
		oReturn.bIsGecko = !oReturn.bIsWebKit && navigator.product != null && navigator.product.toLowerCase() == "gecko";
		if(oReturn.bIsGecko){ oReturn.nGeckoBuildDate = new Number(sUA.match(/.*gecko\/(\d{8}).*/)[1]) };
		oReturn.bIsIE = sUA.indexOf("msie") > -1 && !oReturn.bIsOpera && !oReturn.bIsKHTML && !oReturn.bIsGecko;
		oReturn.bIsIEMac = oReturn.bIsIE && sUA.match(/.*mac.*/) != null;
		if(oReturn.bIsOpera){ oReturn.nOperaVersion = new Number(sUA.match(/.*opera(\s|\/)(\d+\.\d+)/)[2]) };
		if(oReturn.bIsIE || (oReturn.bIsOpera && oReturn.nOperaVersion < 7.6)){ oReturn.bUseDOM = false };
		if(oReturn.bIsWebKit){ oReturn.nWebKitVersion = new Number(sUA.match(/.*applewebkit\/(\d+).*/)[1]) };
		if(window.hasFlash && (!oReturn.bIsIE || oReturn.bIsIEMac)){ 
			var flashDescription = (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]).description;
			oReturn.nFlashVersion = parseInt(flashDescription.charAt(flashDescription.indexOf(".") - 1));
		};
		if(sUA.match(/.*(windows|mac).*/) == null || 
		oReturn.bIsIEMac || oReturn.bIsKonq || 
		(oReturn.bIsOpera && oReturn.nOperaVersion < 7.6) || 
		(oReturn.bIsSafari && oReturn.nFlashVersion < 7) ||
		(!oReturn.bIsSafari && oReturn.bIsWebKit && oReturn.nWebKitVersion < 124) || 
		(oReturn.bIsGecko && oReturn.nGeckoBuildDate < 20020523)){
			oReturn.bHasTransparencySupport = false;
		};

		if(!oReturn.bIsIEMac && !oReturn.bIsGecko && document.createElementNS){
			try {
				document.createElementNS(sNameSpaceURI, "i").innerHTML = "";
			} catch(e){
				oReturn.bIsXML = true;
			};
		};
		
		oReturn.bUseInnerHTMLHack = oReturn.bIsKonq || (oReturn.bIsWebKit && oReturn.nWebKitVersion < 312) || oReturn.bIsIE;
		
		return oReturn;
	}();
	
	/*	Disable sIFR for non-Flash or old browsers
		Also disable it for IE and KHTML browsers in XML mode, since we are using innerHTML for those browsers */
	if(window.hasFlash == false || !document.createElement || !document.getElementById || (UA.bIsXML && UA.bUseInnerHTMLHack)){
		return {UA:UA};
	};
	
	function sIFR(e){
		if((!self.bAutoInit && (window.event || e) != null) || !mayReplace(e)){
			return;	
		};
		bIsInitialized = true;
		
		for(var i = 0, limit = stackReplaceElementArguments.length; i < limit; i++){
			replaceElement.apply(null, stackReplaceElementArguments[i]);
		};
		stackReplaceElementArguments = [];
	};
	
	var self = sIFR;

	function mayReplace(e){
		if(bIsSetUp == false || self.bIsDisabled == true || ((UA.bIsXML && UA.bIsGecko || UA.bIsKHTML) && e == null && bIsInitialized == false) || (document.body == null || document.getElementsByTagName("body").length == 0)){
			return false;
		};
		return true;
	};
	
	function escapeHex(sHex){
		if(UA.bIsIE){ /* The RegExp for IE breaks old Gecko's, the RegExp for non-IE breaks IE 5.01 */
			return sHex.replace(new RegExp("%\d{0}", "g"), "%25");
		}
		return sHex.replace(new RegExp("%(?!\d)", "g"), "%25");
	};
	
	function matchNodeNames(node, sMatch){
		if(sMatch == "*"){
			return true;
		};	
		return node.nodeName.toLowerCase().replace("html:", "") == sMatch.toLowerCase();
	};

	function fetchContent(node, nodeNew, sCase, nLinkCount, sLinkVars){
		var sContent = "";
		var oSearch = node.firstChild;
		var oRemove, nodeRemoved, oResult, sValue;

		if(nLinkCount == null){ nLinkCount = 0 };
		if(sLinkVars == null){ sLinkVars = "" };

		while(oSearch){
			if(oSearch.nodeType == 3){
				sValue = oSearch.nodeValue.replace("<", "&lt;");
				switch(sCase){
					case "lower":
						sContent += sValue.toLowerCase();
						break;
					case "upper":
						sContent += sValue.toUpperCase();
						break;
					default:
						sContent += sValue;
				};
			} else if(oSearch.nodeType == 1){
				if(matchNodeNames(oSearch, "a") && !oSearch.getAttribute("href") == false){
					if(oSearch.getAttribute("target")){
						sLinkVars += "&sifr_url_" + nLinkCount + "_target=" + oSearch.getAttribute("target");
					};
					sLinkVars += "&sifr_url_" + nLinkCount + "=" + escapeHex(oSearch.getAttribute("href")).replace(/&/g, "%26");
					sContent += '<a href="asfunction:_root.launchURL,' + nLinkCount + '">';
					nLinkCount++;
				} else if(matchNodeNames(oSearch, "br")){
					sContent += "<br/>";
				};
				if(oSearch.hasChildNodes()){
					/*	The childNodes are already copied with this node, so nodeNew = null */
					oResult = fetchContent(oSearch, null, sCase, nLinkCount, sLinkVars);
					sContent += oResult.sContent;
					nLinkCount = oResult.nLinkCount;
					sLinkVars = oResult.sLinkVars;
				};
				if(matchNodeNames(oSearch, "a")){
					sContent += "</a>";
				};
			};
			oRemove = oSearch;
			oSearch = oSearch.nextSibling;
			if(nodeNew != null){
				nodeRemoved = oRemove.parentNode.removeChild(oRemove);
				nodeNew.appendChild(nodeRemoved);	
			};
		};
		
		return {"sContent" : sContent, "nLinkCount" : nLinkCount, "sLinkVars" : sLinkVars};
	};
	
	function createElement(sTagName){
		if(document.createElementNS && UA.bUseDOM){
			return document.createElementNS(sNameSpaceURI, sTagName);	
		} else {
			return document.createElement(sTagName);
		};
	};

	function createObjectParameter(nodeObject, sName, sValue){
		var node = createElement("param");
		node.setAttribute("name", sName);	
		node.setAttribute("value", sValue);
		nodeObject.appendChild(node);
	};
	
	/*	Konqueror does not treat empty classNames as strings, so we need a workaround */
	function appendToClassName(node, sAppend){
		var sClassName = node.className;
		if(sClassName == null){
			sClassName = sAppend;
		} else {
			sClassName = sClassName.normalize() + (sClassName == "" ? "" : " ") + sAppend;
		};
		node.className = sClassName;
	};
	
	function prepare(bNow){
		var node = document.documentElement;
		if(self.bHideBrowserText == false){
			node = document.getElementsByTagName("body")[0];
		};
		if((self.bHideBrowserText == false || bNow) && node){
			if(node.className == null || node.className.match(/\bsIFR\-hasFlash\b/) == null){
				appendToClassName(node, "sIFR-hasFlash");
			};
		};
	};
	
	function replaceElement(sSelector, sFlashSrc, sColor, sLinkColor, sHoverColor, sBgColor, nPaddingTop, nPaddingRight, nPaddingBottom, nPaddingLeft, sFlashVars, sCase, sWmode){
		if(!mayReplace()){
			return stackReplaceElementArguments.push(arguments);	
		};

		prepare();
		
		/*	Extract any named arguments.	*/
		named.extract(arguments, {
			sSelector : function(value){ sSelector = value },
			sFlashSrc : function(value){ sFlashSrc = value },
			sColor : function(value){ sColor = value },
			sLinkColor : function(value){ sLinkColor = value },
			sHoverColor : function(value){ sHoverColor = value },
			sBgColor : function(value){ sBgColor = value },
			nPaddingTop : function(value){ nPaddingTop = value },
			nPaddingRight : function(value){ nPaddingRight = value },
			nPaddingBottom : function(value){ nPaddingBottom = value },
			nPaddingLeft : function(value){ nPaddingLeft = value },
			sFlashVars : function(value){ sFlashVars = value },
			sCase : function(value){ sCase = value },
			sWmode : function(value){ sWmode = value }
		});

		/* Check if we can find any nodes first */
		var listNodes = parseSelector(sSelector);
		if(listNodes.length == 0){ return false };

		/*	Set default values. */
		if(sFlashVars != null){
			sFlashVars = "&" + sFlashVars.normalize();
		} else {
			sFlashVars = "";	
		};
		
		if(sColor != null){sFlashVars += "&textcolor=" + sColor};
		if(sHoverColor != null){sFlashVars += "&hovercolor=" + sHoverColor};
		if(sHoverColor != null || sLinkColor != null){sFlashVars += "&linkcolor=" + (sLinkColor || sColor)};
		
		if(nPaddingTop == null){ nPaddingTop = 0 };
		if(nPaddingRight == null){ nPaddingRight = 0 };
		if(nPaddingBottom == null){ nPaddingBottom = 0 };
		if(nPaddingLeft == null){ nPaddingLeft = 0 };

		if(sBgColor == null){ sBgColor = "#FFFFFF" };
		
		if(sWmode == "transparent"){
			if(!UA.bHasTransparencySupport){
				sWmode = "opaque";
			} else {
				sBgColor = "transparent";
			};
		};
		
		if(sWmode == null){ sWmode = "" };
	
		/*	Do the actual replacement. */
		var node, sWidth, sHeight, sMargin, sPadding, sVars, nodeAlternate, nodeFlash, oContent;
		var nodeFlashTemplate = null;

		for(var i = 0, limit = listNodes.length; i < limit; i++){
			node = listNodes[i];

			/* Prevents elements from being replaced multiple times. */
			if(node.className != null && node.className.match(/\bsIFR\-replaced\b/) != null){ continue };
			
			sWidth = node.offsetWidth - nPaddingLeft - nPaddingRight;
			sHeight = node.offsetHeight - nPaddingTop - nPaddingBottom;
			
			if(isNaN(sWidth) || isNaN(sHeight)){
				self.bIsDisabled = true;
				document.documentElement.className = document.documentElement.className.replace(/\bsIFR\-hasFlash\b/, "");
				return;
			};

			nodeAlternate = createElement("span");
			nodeAlternate.className = "sIFR-alternate";

			oContent = fetchContent(node, nodeAlternate, sCase);
			sVars = "txt=" + escapeHex(oContent.sContent).replace(/\+/g, "%2B").replace(/&/g, "%26").replace(/\"/g, "%22").normalize() + sFlashVars + "&w=" + sWidth + "&h=" + sHeight + oContent.sLinkVars;
			
			appendToClassName(node, "sIFR-replaced");

			/*	Opera only supports the object element, other browsers are given the embed element,
				for backwards compatibility reasons between different browser versions.
				Opera versions below 7.60 use innerHTML, from 7.60 and up we use the DOM */

			if(nodeFlashTemplate == null || !UA.bUseDOM){
				if(!UA.bUseDOM){
					node.innerHTML = ['<embed class="sIFR-flash" type="application/x-shockwave-flash" src="', sFlashSrc, '" quality="best" wmode="', sWmode, '" bgcolor="', sBgColor, '" flashvars="', sVars, '" width="', sWidth, '" height="', sHeight, '" sifr="true"></embed>'].join("");
				} else {
					if(UA.bIsOpera){
						nodeFlash = createElement("object");
						nodeFlash.setAttribute("data", sFlashSrc);
						createObjectParameter(nodeFlash, "quality", "best");
						createObjectParameter(nodeFlash, "wmode", sWmode);
						createObjectParameter(nodeFlash, "bgcolor", sBgColor);
					} else {
						nodeFlash = createElement("embed");
						nodeFlash.setAttribute("src", sFlashSrc);
						nodeFlash.setAttribute("quality", "best");
						nodeFlash.setAttribute("flashvars", sVars);
						nodeFlash.setAttribute("wmode", sWmode);
						nodeFlash.setAttribute("bgcolor", sBgColor);
						nodeFlash.setAttribute("pluginspace", "http://www.macromedia.com/go/getflashplayer");
						nodeFlash.setAttribute("scale", "noscale");
					};
					nodeFlash.setAttribute("sifr", "true");
					nodeFlash.setAttribute("type", "application/x-shockwave-flash");
					nodeFlash.className = "sIFR-flash";
					if(!UA.bIsKHTML || !UA.bIsXML){
						nodeFlashTemplate = nodeFlash.cloneNode(true);
					};
				};
			} else {
				nodeFlash = nodeFlashTemplate.cloneNode(true);
			};
			if(UA.bUseDOM){
				/* General settings */
				if(UA.bIsOpera){
					createObjectParameter(nodeFlash, "flashvars", sVars);
				} else {
					nodeFlash.setAttribute("flashvars", sVars);
				};
				nodeFlash.setAttribute("width", sWidth);
				nodeFlash.setAttribute("height", sHeight);
				nodeFlash.style.width = sWidth + "px";
				nodeFlash.style.height = sHeight + "px";
				node.appendChild(nodeFlash);
			};
			
			node.appendChild(nodeAlternate);

			/*	Workaround to force KHTML-browsers to repaint the document. 
				Additionally, IE for both Mac and PC need this.
				See: http://neo.dzygn.com/archive/2004/09/forcing-safari-to-repaint */

			if(UA.bUseInnerHTMLHack){
				node.innerHTML += "";
			};
		};
		
		if(UA.bIsIE && self.bFixFragIdBug){
			setTimeout(function(){document.title = sDocumentTitle}, 0);
		};
	};
	
	function updateDocumentTitle(){
		sDocumentTitle = document.title;
	};
	
	function setup(){
		if(self.bIsDisabled == true){ return };

		bIsSetUp = true;
		/*	Providing a hook for you to hide certain elements if Flash has been detected. */
		if(self.bHideBrowserText){
			prepare(true);
		};
		
		if(window.attachEvent){
			window.attachEvent("onload", sIFR);
		} else if(!UA.bIsKonq && (document.addEventListener || window.addEventListener)){
			if(document.addEventListener){
				document.addEventListener("load", sIFR, false);	
			};
			if(window.addEventListener){
				window.addEventListener("load", sIFR, false);	
			};
		} else {
			if(typeof window.onload == "function"){
				var fOld = window.onload;
				window.onload = function(){ fOld(); sIFR(); };
			} else {
				window.onload = sIFR;
			};
		};
		
		if(!UA.bIsIE || window.location.hash == ""){
			self.bFixFragIdBug = false;
		} else {
			updateDocumentTitle();
		};
	};
	
	function debug(){
		prepare(true);
	};
	
	debug.replaceNow = function(){
		setup();
		sIFR();
	};
	
	/* Public Fields */
	self.UA = UA;
	self.bAutoInit = true;
	self.bFixFragIdBug = true;
	self.replaceElement = replaceElement;
	self.updateDocumentTitle = updateDocumentTitle;
	self.appendToClassName = appendToClassName;
	self.setup = setup;
	self.debug = debug;
	self.bIsDisabled = false;
	self.bHideBrowserText = true;
	
	return self;
}();

/*	sIFR setup. You can add browser detection here. 
	sIFR's browser detection is exposed through sIFR.UA. */

if(typeof sIFR == "function" && !sIFR.UA.bIsIEMac){
	sIFR.setup();
};