import os
import zipfile
import shutil 
from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024  # Maximum upload size of 100 MB
input_base_name = ''


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def clear_output_folder(folder):
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(folder, exist_ok=True)



def split_pdf_by_size(input_pdf_path, output_folder, max_size_mb):
    max_size_bytes = max_size_mb * 1000 * 1000
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    global input_base_name
    input_base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    
    with open(input_pdf_path, "rb") as input_pdf_file:
        pdf_reader = PdfReader(input_pdf_file)
        total_pages = len(pdf_reader.pages)
        
        current_writer = PdfWriter()
        part_number = 1
        
        for page_number in range(total_pages):
            current_writer.add_page(pdf_reader.pages[page_number])
            temp_output_path = os.path.join(output_folder, f"temp_{part_number}.pdf")
            with open(temp_output_path, "wb") as temp_output_file:
                current_writer.write(temp_output_file)
            
            current_size = os.path.getsize(temp_output_path)
            
            if current_size > max_size_bytes:
                current_writer.remove_page(len(current_writer.pages) - 1)

                output_pdf_path = os.path.join(output_folder, f"{input_base_name}_part_{part_number}.pdf")
                with open(output_pdf_path, "wb") as output_pdf_file:
                    current_writer.write(output_pdf_file)
                
                part_number += 1
                current_writer = PdfWriter()
                current_writer.add_page(pdf_reader.pages[page_number])
                
            os.remove(temp_output_path)
        
        if len(current_writer.pages) > 0:
            
            output_pdf_path = os.path.join(output_folder, f"{input_base_name}_part_{part_number}.pdf")
            with open(output_pdf_path, "wb") as output_pdf_file:
                current_writer.write(output_pdf_file)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        max_size_mb = int(request.form['size'])
        
        output_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        clear_output_folder(output_folder)
        split_pdf_by_size(file_path, output_folder, max_size_mb)
        
        zip_folder_name = f"Splitted_output_{input_base_name}"
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{zip_folder_name}.zip")
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    if not file.startswith('temp_'):
                        file_path_in_zip = os.path.join(zip_folder_name, file)
                        zipf.write(os.path.join(root, file), arcname=file_path_in_zip)
        
        return jsonify({'download_url': url_for('download_file', filename=f"{zip_folder_name}.zip", _external=True)})

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        response = send_file(file_path, as_attachment=True)
        
        # Cleanup: remove the uploaded and generated files
        original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.splitext(filename.replace('Splitted_output_', ''))[0] + '.pdf')
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        clear_output_folder(os.path.join(app.config['UPLOAD_FOLDER'], 'output'))
        clear_output_folder(app.config['UPLOAD_FOLDER'])
        return response
    else:
        return "File not found", 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)


