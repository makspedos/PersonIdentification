
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}


function activateCheckbox(item){
  var checkbox = item.querySelector('input[type="checkbox"]')
  if (checkbox){
     checkbox.checked = !checkbox.checked;
  }
}