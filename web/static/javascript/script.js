
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

function validateForm() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var atLeastOneChecked = Array.from(checkboxes).some(function(checkbox) {
        return checkbox.checked;
    });

    if (!atLeastOneChecked) {
        setTimeout(5000);
        document.getElementById('error-message').style.display = 'block';
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}