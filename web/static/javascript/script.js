
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

function displayFileName() {
        const input = document.getElementById('img-upload');
        const fileNameSpan = document.getElementById('file-name');

        if (input.files.length > 0) {
            fileNameSpan.textContent = 'Обрано';
        }
        else if (document.getElementById('image-url').value){
            fileNameSpan.textContent = '';
        }
        else {
            fileNameSpan.textContent = '';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('image-url').addEventListener('change', function () {
        var imageUrl = this.value;
        var uploadInput = document.getElementById('img-upload');
        if (imageUrl) {
            uploadInput.value = ''; // Clear the value of the file input
            displayFileName()
        }
    });

    document.getElementById('img-upload').addEventListener('change', function () {
        var uploadInput = this.value;
        var imageUrl = document.getElementById('image-url');
        if (uploadInput) {
            imageUrl.value = ''; // Clear the value of the file input
            displayFileName()
        }
    });
});