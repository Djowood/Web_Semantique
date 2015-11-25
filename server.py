﻿import json

from flask import Flask, render_template, request

import main

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    search_query = request.form['search']
    seuil = request.form['seuil']
    type = request.form['type']  # Récuperation de la valeur du radio button
    filtre = request.form['filtre']

    request_filtre = 0 if filtre == 'memento' else 1
    request_type = 0 if type == 'actors' else 1
    print('you searched ', search_query, " ", type, 'With ratio = ', seuil, "With filter : ", request_filtre)
    if request_filtre == 0:
        search_res = main.DoSearch(search_query + " " + type, float(seuil), request_type)
    elif request_filtre == 1:
        search_res = main.DoSimilar(search_query + " " + type, float(seuil), request_type)
    search_res["search"] = search_query

    print(str(search_res).encode('utf-8', 'ignore'))
    return render_template('results.html', results=search_res, type=request_type)


@app.route("/test")
def test():
    res = main.DoSearch("")
    return render_template('results.html', matrice=res["matrice"], targets=json.dumps(res["target"]))


if __name__ == "__main__":
    app.debug = True
    app.run()
