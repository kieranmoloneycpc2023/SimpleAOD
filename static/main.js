// Display selected file names in the form
const fileInput = document.querySelector('input[name="pdf_files"]');
const fileInputLabel = document.querySelector('.file-input-label');

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        const fileNames = Array.from(fileInput.files).map(file => file.name);
        fileInputLabel.textContent = fileNames.join(', ');
    } else {
        fileInputLabel.textContent = 'Choose PDF files';
    }
});
