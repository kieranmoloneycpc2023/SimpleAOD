
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import re
from PyPDF2 import PdfFileReader, PdfFileMerger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload():
    # Check if the 'pdf_files' field exists in the request
    if 'pdf_files' not in request.files:
        return redirect('/')

    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    files = request.files.getlist('pdf_files')
    filenames = []

    # Save each uploaded file to the uploads folder
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

    # Extract dates from the uploaded PDFs
    dates = extract_dates(filenames)

    # Sort the filenames based on the extracted dates
    sorted_filenames = sort_files_by_date(filenames, dates)

    # Merge the sorted PDFs into a single PDF
    merged_filename = merge_pdfs(sorted_filenames)

    return redirect('/result?filename=' + merged_filename)

# Route to display the merged PDF
@app.route('/result')
def result():
    filename = request.args.get('filename')
    return render_template('result.html', filename=filename)

# Helper function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Helper function to extract dates from PDFs
def extract_dates(filenames):
    dates = []
    for filename in filenames:
        pdf = PdfFileReader(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        text = ''
        for page in pdf.pages:
            text += page.extract_text()

        # Extract dates using regular expressions
        date_matches = re.findall(r'\d{2}/\d{2}/\d{4}', text)
        dates.extend(date_matches)

    return dates

# Helper function to sort filenames based on dates
def sort_files_by_date(filenames, dates):
    return sorted(filenames, key=lambda x: dates[filenames.index(x)])

# Helper function to merge PDFs
def merge_pdfs(filenames):
    merger = PdfFileMerger()
    for filename in filenames:
        merger.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert a blank page between merged documents
        merger.add_blank_page()

    merged_filename = 'merged.pdf'
    merger.write(os.path.join(app.config['UPLOAD_FOLDER'], merged_filename))
    merger.close()

    return merged_filename

if __name__ == '__main__':
    app.run()
