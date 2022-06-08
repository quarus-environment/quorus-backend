from flask import Flask, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from keras.models import model_from_json
import numpy as np
import tensorflow as tf

import os

UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

json_file = open("mnist_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("mnist_model.h5")

loaded_model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])


@app.route('/', methods=['POST'])
def upload_file():
    request.files['file'].save(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(request.files['file'].filename)))
    img = tf.keras.utils.load_img(f"uploaded_files/{request.files['file'].filename}", target_size=(128, 128))
    img_tensor = tf.keras.utils.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    predict = loaded_model.predict(img_tensor)
    index = np.where(predict == predict.max())[1]
    return {"file": request.files['file'].filename, "predict": "logitech"}


@app.route('/uploaded_files/<path:path>')
def send_report(path):
    return send_from_directory('uploaded_files', path)


app.run()
