from flask import Flask, render_template, request, jsonify, after_this_request, send_file
from io import BytesIO
from waitress import serve
import base64
import subprocess
import os
import random
import string
import re
import shlex
import json


app = Flask(__name__)

app.debug = True  # Activa el modo debug de Flask

modelos = 'D:\\Python\\modelos\\'
audio = 'D:\\Python\\output\\'
piper = 'D:\\Python\\piper\\'


# Models with specific character replacements
models_replacements = {
    "Español México | Claude": {
        "model_path": "es_MX-claude-14947-epoch-high.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    },
    "Español México | Cortana Infinnity": {
        "model_path": "es_MX-cortana-19669-epoch-high.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    },
    "Español México | TheGevy": {
        "model_path": "es_MX-gevy-10196-epoch-high.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    },
    "English US | Voice": {
        "model_path": "en_US-ljspeech-high.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    },
    "audio": {
        "model_path": "es_ES-davefx-medium.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    },
    "audio_mujer": {
        "model_path": "es_ES-mls_10246-low.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    },
    "audio_sefla": {
        "model_path": "es_MX-laura-high.onnx",
        "replacements": [('(', ','), (')', ','), ('?', ','), ('¿', ','), (':', ','), ('\n', ' ')]
    }
}

def filter_text(text):
    # Escapa caracteres especiales
    escaped_text = shlex.quote(text)
    return escaped_text

def convert_text_to_speech(parrafo, model):
    # Limitar el texto a 10000 caracteres
    parrafo = parrafo[:10000]
    
    model_info = models_replacements.get(model)
    if model_info:
        model_path = modelos + model_info.get("model_path")
        parrafo_filtrado = filter_text(parrafo)
        print(parrafo_filtrado," este es el modelo")

        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.wav'
        output_file = os.path.join(audio, random_name)
        app.logger.info("Audio file created at: %s", output_file)
        piper_exe = os.path.join(piper, 'piper.exe')  # Adjusted the path for piper

        # Verifica si la ruta del archivo piper es correcta
        #print(piper_exe, "hola ")
        if os.path.isfile(piper_exe):
            comando = f'echo {parrafo_filtrado} | "{piper_exe}" -m {model_path} -f {output_file}'
            print(comando,"comando ")
            subprocess.run(comando, shell=True)
            return output_file
        else:
            app.logger.error("The piper executable was not found in the correct directory.")
            return "The piper executable was not found in the correct directory."
    else:
        app.logger.error("Model not found.")
        return "Model not found."

@app.route('/')
def index():
    model_options = list(models_replacements.keys())
    # Log the contents of the current folder
    #app.logger.info("Contents of current folder: %s", os.listdir(file_folder))
    app.logger.debug('Este es un mensaje de debug')
    app.logger.info('Este es un mensaje informativo')
    app.logger.warning('Este es un mensaje de advertencia')
    app.logger.error('Este es un mensaje de error')

    return render_template('index.html', model_options=model_options)

@app.route('/convert', methods=['POST'])
def convert_text():
    #text = request.form['text']
    #model = request.form['model']

    text = request.json['mensaje']

    model = request.json['modelo']

    #print(request.json['mensaje'], request.json['modelo'])


    #print(text, "hola como estas", model)

    output_file = convert_text_to_speech(text, model)
        

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=7860, debug=True)
    serve(app, host='0.0.0.0', port=8050)
