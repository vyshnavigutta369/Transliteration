#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from deeptranslit import DeepTranslit
import csv

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/output', methods=['GET'])
def api_transliterate():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'word' in request.args:
        word = request.args['word']
    else:
        return "Error: No word provided. Please enter a word."


    transliterator = DeepTranslit('hindi')


    WordsandScores=list(transliterator.transliterate(word))

    Top5=[]

    for tup in WordsandScores:
        Top5.append(tup[0])

    return jsonify(Top5)

app.run()
'''
with open('../../xlit_movies.csv','r') as r1:
     l1 = csv.reader(r1, delimiter=',')
     for i,line in enumerate(l1):
         if (i==0):
             continue
         top5=list(transliterator.transliterate(line[0]))
         print (top5[0][0])
'''

