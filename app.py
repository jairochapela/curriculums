import uuid
from flask import Flask, flash, redirect, render_template, request
from pathlib import Path
from werkzeug.utils import secure_filename
import os
from models import Candidato

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key =  'super secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data
        email = request.form.get('email')
        if not email:
            flash('Email is required')
            return redirect(request.url)

        # Save the candidate
        candidato = Candidato(
            id=str(uuid.uuid4()),
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=email,
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            education=request.form.get('education'),
            experience=request.form.get('experience'),
            languages=request.form.get('languages')
        )
        candidato.save()

        # Create a folder with the canonical version of the email
        folder_name = email.lower().replace('@', '-').replace('.', '_')
        unique_id = uuid.uuid4().hex
        folder_path = Path(app.config['UPLOAD_FOLDER']) / folder_name / unique_id
        folder_path.mkdir(exist_ok=True, parents=True)

        if 'resume' in request.files:
            resume = request.files['resume']
            resume.save(folder_path / secure_filename(resume.filename))
        else:
            flash('Falta archivo adjunto')
            return redirect(request.url)
        
        if 'certifications' in request.files:
            certifications = request.files['certifications']
            certifications.save(folder_path / secure_filename(certifications.filename))

        #folder_path = os.path.join('/path/to/save/folder', folder_name)
        #os.makedirs(folder_path, exist_ok=True)
        for k,file in request.files.items():
            filename = secure_filename(file.filename)
            subfolder = secure_filename(k)
            upload_to = folder_path / subfolder
            upload_to.mkdir(exist_ok=True, parents=True)
            file.save(upload_to / filename)

        flash('Archivos subidos correctamente')
        return redirect('/')

    return render_template('index.html')

if __name__ == '__main__':
    app.run()