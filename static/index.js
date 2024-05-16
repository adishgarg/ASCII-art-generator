var dropbox = document.getElementById('dropbox');

dropbox.addEventListener("dragenter", function (e) {
    e.preventDefault();
    dropbox.style.background = "#f7f7f7";
});

dropbox.addEventListener("dragover", function (e) {
    e.preventDefault();
});

dropbox.addEventListener("dragleave", function (e) {
    e.preventDefault();
    dropbox.style.background = "";
});

dropbox.addEventListener('drop', function(e) {
    e.preventDefault();
    dropbox.style.background = '';
    var file = e.dataTransfer.files[0];
    document.getElementById('imageInput').files = e.dataTransfer.files;
});

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append('image', document.getElementById('imageInput').files[0]);

    fetch('/ascii', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.write(data);  // Replace the current document with the response
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
