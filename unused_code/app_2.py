import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, session
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path="/static")
app.secret_key = "your-secret-key"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max upload

INSTITUTIONS = ['Europa-Universität Flensburg',
                'Philipps-University Marburg',
                'Universität Gießen',
                'Universität Bielefeld',
                'Osnabrück University',
                'Heidelberg University']

NAMES = ['Albina Kushanashvili',
         'Dezso Mate',
         'Mohammad Fazleh Elahi',
         'Maria Schwab',
         'Kirsten von Hagen',
         'Iulia Karin Patrut',
         'Klaus-Michael Bogdal'
         'Matthias Bauer',
         'Melanie Ulz',
         'Nele Feuring',
         'Peter Bell',
         'Radmila Mladenova',
         'Frank Reuter',
         'Tanja Penter',
         'Thomas Bohn',
         'Tobias.haberkorn'
         'Verena Meier',
         'Magdalena Watrin'
         ]


EMAILS = [
    "Albina.Kushanashvili@uni-flensburg.de",
    "Dezso.Mate@uni-flensburg.de",
    "elahim@staff.uni-marburg.de",
    "maria.schwab@uni-flensburg.de",
    "Kirsten.v.Hagen@romanistik.uni-giessen.de",
    "Iulia-Karin.Patrut@uni-flensburg.de",
    "Klaus_michael.bogdal@uni-bielefeld.de",
    "magdalena.watrin@uni-giessen.de",
    "matthias.bauer@uni-flensburg.de",
    "Melanie.Ulz@psk.uni-regensburg.de",
    "Nele.Feuring@uni-flensburg.de",
    "peter.bell@uni-marburg.de",
    "Radmila.Mladenova@zegk.uni-heidelberg.de",
    "Frank.reuter@zegk.uni-heidelberg.de",
    "Tanja.penter@zegk.uni-heidelberg.de",
    "Thomas.Bohn@geschichte.uni-giessen.de",
    "Tobias.haberkorn@geschichte.uni-giessen.de",
    "Verena.meier@zegk.uni-heidelberg.de"
]


def allowed_file(filename):
    return '.' in filename

@app.route('/')
def upload_form():
    user_uploads = session.get('uploaded_files', [])
    return render_template('upload_folder.html', user_uploads=user_uploads, institutions=INSTITUTIONS,emails=EMAILS,names=NAMES)

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files or 'fullname' not in request.form or 'email' not in request.form or 'institution' not in request.form:
        flash('Missing information')
        return redirect(request.url)

    fullname = request.form['fullname'].strip()
    email = request.form['email'].strip()
    institution = request.form['institution'].strip()

    if not fullname or not email or not institution:
        flash('Full name, email, and institution are required')
        return redirect(request.url)

    files = request.files.getlist('files[]')
    base_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(institution))
    os.makedirs(base_path, exist_ok=True)

    uploaded_files = []

    for file in files:
        relative_path = file.filename.replace("\\", "/")  # Normalize Windows paths
        safe_path = os.path.normpath(relative_path)

        if safe_path.startswith(".."):
            flash('Unsafe file path detected')
            return redirect(request.url)

        full_save_path = os.path.join(base_path, safe_path)
        save_dir = os.path.dirname(full_save_path)
        os.makedirs(save_dir, exist_ok=True)
        file.save(full_save_path)

        uploaded_files.append({
            'institution': institution,
            'file_path': safe_path
        })

    session['uploaded_files'] = uploaded_files
    flash('Folder uploaded successfully!')

    return redirect(url_for('upload_form'))

@app.route('/download/<institution>/<path:filepath>')
def download_file(institution, filepath):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(institution))
    return send_from_directory(directory, filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
