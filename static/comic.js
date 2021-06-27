function getBlock(name) {
  if (document.getElementById(name)) {
	return document.getElementById(name);
  } else if (document.all) {
	return document.all[name];
  } else if (document.layers) {
	return document.layers[name];
  }
}
function getStyle(name) {
  return getBlock(name).style;
}

function hideBlock(name) {
  getStyle(name).display="none";
}

function showBlock(name) {
  getStyle(name).display="";
}
function toggleBlock(name){
    if(getStyle(name).display === "none"){
        showBlock(name);
    }else{
        hideBlock(name);
    }
}