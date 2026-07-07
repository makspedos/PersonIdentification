function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

function activateCheckbox(item) {
  var checkbox = item.querySelector('input[type="checkbox"]');
  if (checkbox) {
    checkbox.checked = !checkbox.checked;
  }
}

function validateForm() {
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');
  var atLeastOneChecked = Array.from(checkboxes).some(function(checkbox) {
    return checkbox.checked;
  });

  if (!atLeastOneChecked) {
    document.getElementById('error-message').style.display = 'block';
    return false;
  }
  return true;
}

function displayFileName() {
  const input = document.getElementById('img-upload');
  const fileNameSpan = document.getElementById('file-name');

  if (input.files.length > 0) {
    fileNameSpan.textContent = 'Selected';
  } else {
    fileNameSpan.textContent = '';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('image-url').addEventListener('change', function () {
    var imageUrl = this.value;
    var uploadInput = document.getElementById('img-upload');
    if (imageUrl) {
      uploadInput.value = '';
      displayFileName();
    }
  });

  document.getElementById('img-upload').addEventListener('change', function () {
    var uploadInput = this.value;
    var imageUrl = document.getElementById('image-url');
    if (uploadInput) {
      imageUrl.value = '';
      displayFileName();
    }
  });
});