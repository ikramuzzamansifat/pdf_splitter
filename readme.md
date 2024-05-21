# PDF Splitter

This Flask-based web application allows users to upload a large PDF file (Upto 150 MB) and split it into smaller PDFs such that each split PDF does not exceed a specified size. The resulting PDFs are then compressed into a ZIP file for easy download.

## Features

- Upload a large PDF file (Upto 150 MB)
- Specify the maximum size (in MB) for each split PDF
- Generate split PDF files based on the specified size
- Download the split PDFs as a single ZIP file, named `Splitted_output_<input_file_name>.zip`
- Files within the ZIP are organized in a folder named after the ZIP file

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/ikramuzzamansifat/pdf_splitter.git
    cd pdf_splitter_app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies listed in `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the Flask application:
    ```sh
    python app.py
    ```

5. Open your web browser and navigate to `http://127.0.0.1:5000/`.

6. Use the web interface to upload a PDF file and specify the maximum size for each split PDF.

7. After processing, download the resulting ZIP file containing the split PDFs.
## Project Structure

The project directory contains the following files and directories:

- **`pdf_splitter_app/`**: The main project directory.
  - **`templates/`**: Directory containing HTML templates for the web interface.
    - `index.html`: HTML template for the web interface.
  - **`static/`**: Directory containing static files (e.g., CSS, JavaScript).
    - `styles.css`: CSS file for styling the web interface.
    - `script.js`: JavaScript file for handling form submission and progress display.
  - `app.py`: Main Flask application file.
  - `README.md`: Project documentation.

