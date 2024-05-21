document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/upload', true);

    xhr.onloadstart = function() {
        document.getElementById('loading').style.display = 'flex';
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var downloadLink = document.getElementById('download-link');
            var downloadUrl = document.getElementById('download-url');
            downloadUrl.href = response.download_url;
            downloadLink.style.display = 'block';
        } else {
            alert('An error occurred while processing your request. Please try again.');
        }
        document.getElementById('loading').style.display = 'none';
    };

    xhr.onerror = function() {
        alert('An error occurred while processing your request. Please try again.');
        document.getElementById('loading').style.display = 'none';
    };

    xhr.send(formData);
});
