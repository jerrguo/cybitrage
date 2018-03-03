from flask import Flask, render_template, request, redirect, jsonify
from graph.weighted_graph import weighted_graph
import json

support_currs = ['EUR', 'USD', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD', 'GBP', 'SEK', 'NOK', 'MXN', 'TRY', 'ZAR', 'CNH', 'XAU', 'XAG']
support_currs_string = ', '.join(support_currs)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def currencies():
    currencies = ""
    temp_list = []

    if request.method == 'POST':
        currencies = request.form['currs']                          # Let currenices equal the string value in textfield
        currencies = currencies.upper().replace(" ", "")            # Set currencies to capitals and remove whitespace
        temp_list = currencies.split(',')                           # Temporary list of inputs
        curr_list = []                                              # List to store valid inputs

        # Detect any non-supported currency values and remove them
        for currency in temp_list:
            if currency in support_currs:
                curr_list.append(currency)

        curr_list = list(set(curr_list))                            # Remove duplicate currencies from list
        currencies = ', '.join(curr_list)                           # Recompile string of currencies excluding erroneous values

        print('THIS: ' + currencies)
    else:
        currencies = ""

    return render_template('home.html', currencies=currencies, support_currs_string=support_currs_string)



if __name__ == '__main__':
    app.run(debug = 'True')
