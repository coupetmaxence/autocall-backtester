# coding: utf-8

import dash
from dash.dependencies import Input, Output
from app_template import web_app_template
import datetime
from test_report import create_report, send_mail
from autocall import Autocall
from backtester import backtest
import uuid
import time

app = dash.Dash(__name__)
server = app.server

NBR_CLICKS = 0


# Describe the layout, or the UI, of the app
app.layout = web_app_template()

@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('view-source', 'n_clicks'),
    dash.dependencies.Input('udls', 'value')])
def create_backtest(nclicks, underlyings):
    global NBR_CLICKS

    if nclicks != None and nclicks != NBR_CLICKS:
        NBR_CLICKS += 1
        print(underlyings)
        start_date = datetime.date(2008, 9, 5)
        end_date = datetime.date.today()
        autocall = Autocall(underlyings, 2, 0.5, 100, 70, 'US', 4, 100, 100)
        backtest_result = backtest(autocall, start_date, end_date)
        id = str(uuid.uuid4())
        create_report(id, autocall, start_date, end_date, backtest_result)
        send_mail(['maxence.coupet@gmail.com'],
                    'Backtest result - ' + autocall.underlyings_string + time.strftime("%d/%m/%Y"), id)




external_css = ["https://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en",
                "https://fonts.googleapis.com/icon?family=Material+Icons",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://fonts.googleapis.com/icon?family=Material+Icons",
                "https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://code.getmdl.io/1.3.0/material.indigo-red.min.css",
                "https://getmdl.io/templates/text-only/styles.css",
                "https://codepen.io/Maxence8/pen/PdvdRe.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.getmdl.io/1.3.0/material.min.js",
                "https://code.jquery.com/jquery-3.2.1.min.js",
                "https://codepen.io/Maxence8/pen/PdvdRe.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
