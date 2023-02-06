from flask import Flask, jsonify, render_template, request, make_response, session
import re
import pandas as pd
import os 
from werkzeug.utils import secure_filename
import csv 

app = Flask(__name__, template_folder='templateFiles')

from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from flask import request

app.json_encoder = LazyJSONEncoder
swagger_template = dict (
    info = {
        'title': LazyString(lambda: 'API for Cleaning Text'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API')
    },
    host=LazyString(lambda: request.host)
)

swagger_template

swagger_config = {
    "headers": [],
    "specs" :[
        {
            "endpoint":"docs",
            "route":'/docs.json'
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app=app,
                 config=swagger_config,
                 template=swagger_template)

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    clean_text = text.replace("USER","").replace("RT","").lower().strip()
    clean_text_2 = re.sub(r'[^a-zA-Z]',' ', clean_text)
    total_char = len(clean_text_2)
    total_word = len(clean_text_2.split())

    abusive_words = []
    with open('abusive.csv', 'r') as f:
        for x in f:
            if ";" in x:
                continue
            elif len(x.strip())>0:
                abusive_words.append(x.strip())

    jumlah_abusive = 0
    for kata in clean_text_2.split():
        for abusive_word in abusive_words:
            if kata == abusive_word:
                jumlah_abusive += 1
                break

    is_abusive_sentence = []
    if jumlah_abusive > 0:
        is_abusive_sentence.append("Kalimat Abusive")
    else:
        is_abusive_sentence.append("Bukan Kalimat Abusive")

    json_response = {
        'data' : clean_text_2.split(),
        'jumlah karakter' : total_char,
        'jumlah kata' : total_word,
        'jumlah abusive word' : jumlah_abusive,
        'kesimpulan' : is_abusive_sentence
    }

    response_data = jsonify(json_response)
    return response_data
    
if __name__=='__main__':
    app.run(debug = True)