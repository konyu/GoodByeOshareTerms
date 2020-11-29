'use strict';

let changeColor = document.getElementById('changeColor');

function popup() {
  chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
  var activeTab = tabs[0];
  chrome.tabs.sendMessage(activeTab.id, {"message": "start", "dic": katakanaDic});
 });
}

document.addEventListener("DOMContentLoaded", function() {
  changeColor.addEventListener("click", popup);
});
