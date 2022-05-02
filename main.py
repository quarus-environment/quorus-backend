# usage: export FLASK_APP=server.py && flask run

from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST'])
def upload_file():
    print(' * received form with', list(request.form.items()))
    # check if the post request has the file part
    print('132', request.files)
    request.files['file'].save(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(request.files['file'].filename)))
    # for file in request.files.getlist('files'):
    #     if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         print(' * file uploaded', filename)
    return request.files['file'].filename


@app.route('/uploaded_files/<path:path>')
def send_report(path):
    return send_from_directory('uploaded_files', path)


app.run()
