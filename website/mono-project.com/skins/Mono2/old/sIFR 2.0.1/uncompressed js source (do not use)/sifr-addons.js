/*	sIFR 2.0.1 Official Add-ons 1.2
	Copyright 2005 Mark Wubben

	This software is licensed under the CC-GNU LGPL <http://creativecommons.org/licenses/LGPL/2.1/>
*/

if(typeof sIFR == "function"){
	sIFR.removeDecoyClasses = function(){
		function removeClass(node, sClass){
			if(node && node.className != null){
				node.className = node.className.replace(/\bsIFR-hasFlash\b/, "");
			};
		};
			
		return function(){
			removeClass(document.documentElement);
			removeClass(document.getElementsByTagName("body")[0]);
		};
	}();

	sIFR.preferenceManager = {
		storage : {
			sCookieId : "sifr",
				
			set : function(bValue){
				var date = new Date();
				date.setFullYear(date.getFullYear() + 3);
				document.cookie = [this.sCookieId, "=", bValue, ";expires=", date.toGMTString(), ";path=/"].join("");
			},
		
			get : function(){
				var value =  document.cookie.match(new RegExp(";?" + this.sCookieId + "=([^;]+);?"));
				if(value != null && value[1] == "false"){
					return false;
				} else {
					return true;
				};
			},
			
			reset : function(){
				var date = new Date();
				date.setFullYear(date.getFullYear() - 1);
				document.cookie = this.sCookieId + "=true;expires=" + date.toGMTString();
			}
		},
		
		disable : function(){
			this.storage.set(false);
		},
		
		enable : function(){
			this.storage.set(true);
		},
		
		test : function(){
			return this.storage.get();
		}
	};
	
	if(sIFR.preferenceManager.test() == false){
		sIFR.bIsDisabled = true;
		sIFR.removeDecoyClasses();
	};
	
	sIFR.rollback = function(){
		function rollback(sSelector){
			named.extract(arguments, {sSelector:function(value){sSelector=value}});
			
			if(sSelector == null){
				sSelector = "";
			} else {
				sSelector += ">";
			};
		
			sIFR.removeDecoyClasses();
			
			sIFR.bHideBrowserText = false;
			
			if(doRollback(sSelector+"embed") == false){
				doRollback(sSelector+"object");
			};
		};
		
		function doRollback(sSelector){
			var node, nodeParent, nodeAlternate, nodeAlternateChild, nodeAlternateNextChild, indexNodeToRemove;
			var listNodes = parseSelector(sSelector);
			var i = listNodes.length - 1;
			var bHasRun = false;
			
			while(i >= 0){
				node = listNodes[i];
				listNodes.length--;
				nodeParent = node.parentNode;
				
				if(node.getAttribute("sifr") == "true"){
					/*	Flash blockers may add other nodes as siblings to the Flash element. 
						Thus, we remove all children of nodeParent, and look for nodeAlternate at the same time */
					indexNodeToRemove = 0;
					
					while(indexNodeToRemove < nodeParent.childNodes.length){
						node = nodeParent.childNodes[indexNodeToRemove];
						if(node.className == "sIFR-alternate"){
							nodeAlternate = node;
							indexNodeToRemove++;
							continue;
						};
						nodeParent.removeChild(node);
					};
					
					if(nodeAlternate != null){
						nodeAlternateChild = nodeAlternate.firstChild;
						while(nodeAlternateChild != null){
							nodeAlternateNextChild = nodeAlternateChild.nextSibling;
							nodeParent.appendChild(nodeAlternate.removeChild(nodeAlternateChild));
							nodeAlternateChild = nodeAlternateNextChild;
						};
						nodeParent.removeChild(nodeAlternate);
					};
					
					if(!sIFR.UA.bIsXML && sIFR.UA.bUseInnerHTMLHack){
						nodeParent.innerHTML += "";
					};

					nodeParent.className = nodeParent.className.replace(/\bsIFR\-replaced\b/, "");
					bHasRun = true;
				};
				
				i--;
			};
			
			return bHasRun;
		};
		
		return rollback;
	}();
};