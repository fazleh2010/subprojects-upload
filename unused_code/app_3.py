import os
import csv
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CSV_FILE = '../users.csv'

institutions = ['Europa-Universität Flensburg',
                'Philipps-University Marburg',
                'Universität Gießen',
                'Universität Bielefeld',
                'Osnabrück University',
                'Heidelberg University']

names = ['Albina Kushanashvili',
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


emails = [
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


@app.route('/')
def index():
    return render_template('upload_folder.html', names=names, emails=emails, institutions=institutions)

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    # Handle name
    name = request.form['name']
    if name == 'other':
        name = request.form.get('new_name')

    # Handle email
    email = request.form['email']
    if email == 'other':
        email = request.form.get('new_email')

    # Handle institution
    institution = request.form['institution']
    if institution == 'other':
        institution = request.form.get('new_institution')

    # Create institution folder if not exists
    institution_folder = os.path.join(UPLOAD_FOLDER, secure_filename(institution))
    if not os.path.exists(institution_folder):
        os.makedirs(institution_folder)

    # Save files
    files = request.files.getlist('files[]')
    for file in files:
        file_path = os.path.join(institution_folder, file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

    # Save user info to CSV
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Email', 'Institution'])

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, email, institution])

    flash('Folder uploaded successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
