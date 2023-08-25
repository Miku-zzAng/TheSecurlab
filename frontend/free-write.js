document.getElementById('file').addEventListener('change', function() {
    var fileName = this.value.split('\\').pop();
    document.querySelector('.upload-name').value = fileName;
});