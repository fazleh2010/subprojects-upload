import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path="/static")
app.secret_key = "your-secret-key"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB limit

def allowed_file(filename):
    return '.' in filename

@app.route('/')
def upload_form():
    return render_template('upload_folder.html')

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files:
        flash('No files selected')
        return redirect(request.url)

    files = request.files.getlist('files[]')
    base_path = os.path.join(app.config['UPLOAD_FOLDER'])
    os.makedirs(base_path, exist_ok=True)

    for file in files:
        # Preserve folder structure using 'webkitRelativePath'
        relative_path = file.headers.get('Content-Relative-Path') or file.filename
        relative_path = relative_path.replace("\\", "/")  # Windows paths to Unix format

        # Secure each path segment
        safe_path = os.path.normpath(relative_path)
        if safe_path.startswith(".."):
            flash('Unsafe file path detected')
            return redirect(request.url)

        full_save_path = os.path.join(base_path, safe_path)
        save_dir = os.path.dirname(full_save_path)
        os.makedirs(save_dir, exist_ok=True)
        file.save(full_save_path)

    flash('Folder uploaded successfully!')
    return redirect(url_for('upload_form'))

if __name__ == '__main__':
    app.run(debug=True)