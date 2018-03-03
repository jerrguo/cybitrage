from flask import Flask, render_template, request, redirect
from graph.weighted_graph import weighted_graph
import time

support_currs = ['EUR', 'USD', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD', 'GBP', 'SEK', 'NOK', 'MXN', 'TRY', 'ZAR', 'CNH', 'XAU', 'XAG']
support_currs_string = ', '.join(support_currs)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def currencies():
    currencies_string = ""
    opportunity_string = ""
    temp_list = []
    opportunites = []

    if request.method == 'POST':
        currencies_string = request.form['currs']                                                   # Let currenices equal the string value in textfield
        currencies_string = currencies_string.upper().replace(" ", "")                              # Set currencies to capitals and remove whitespace
        temp_list = currencies_string.split(',')                                                    # Temporary list of inputs
        curr_list = []                                                                              # List to store valid inputs

        # Detect any non-supported currency values and remove them
        for currency in temp_list:
            if currency in support_currs:
                curr_list.append(currency)

        curr_list = list(set(curr_list))                                                            # Remove duplicate currencies from list
        currencies_string = ', '.join(curr_list)                                                    # Recompile string of currencies excluding erroneous values

        # Arbitrage Detection Algorithm
        if len(curr_list) > 1:
            graph = weighted_graph(curr_list)
            opportunities = graph.show_arbitrage_opportunities()                                    # Opportunities stores the arbitrage cycles in list form
            time_epoch = graph.get_time()                                                           # Get timestamp from graph
            time_string = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(time_epoch))      # Convert to readable time

            if len(opportunites) == 0:
                opportunity_string = "No arbitrage opportunity (" + time_string + ")"

            else:
                opp_string = ' -> '.join(opportunites[0])
                opportunity_string = opp_string + ' at ' + time_string

        else:
            opportunity_string = "No arbitrage opportunity available with less than two currencies..."

    else:
        opportunity_string = "No arbitrage opportunity available with less than two currencies..."


    return render_template('home.html', currencies=currencies_string, support_currs=support_currs_string, opportunity=opportunity_string)



if __name__ == '__main__':
    app.run(debug = 'True')
