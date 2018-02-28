from flask import Flask, render_template, request, redirect, jsonify
from currs.weighted_graph import weighted_graph
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    currs=None

    if request.method == 'POST':
        curr = request.form.getlist('currencies')
        if len(curr) > 1:
            currs = weighted_graph(curr)
            currs = currs.table_dict

    return render_template('test.html', currs=currs)



if __name__ == '__main__':
    app.run(debug='on')
