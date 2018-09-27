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
    dash.dependencies.Input('udls', 'value'),
    dash.dependencies.Input('maturity', 'value'),
    dash.dependencies.Input('frequency', 'value'),
    dash.dependencies.Input('strike', 'value'),
    dash.dependencies.Input('non_callable', 'value'),
    dash.dependencies.Input('barrier', 'value'),
    dash.dependencies.Input('barrier_type', 'value'),
    dash.dependencies.Input('coupon', 'value'),
    dash.dependencies.Input('autocall_trigger', 'value'),
    dash.dependencies.Input('coupon_trigger', 'value'),
    dash.dependencies.Input('begin_date', 'value'),
    dash.dependencies.Input('end_date', 'value'),
    dash.dependencies.Input('email', 'value')])
def create_backtest(nclicks, underlyings, maturity, frequency, strike,
                    nbr_non_callable_obs, barrier, barrier_type, coupon,
                    autocall_trigger, coupon_trigger, begin_date_string,
                    end_date_string, email):
    global NBR_CLICKS

    if nclicks != None and nclicks != NBR_CLICKS:
        NBR_CLICKS += 1
        print(underlyings)
        begin_date_string = begin_date_string.split('/')
        start_date = datetime.date(int(begin_date_string[2]),
                                    int(begin_date_string[1]),
                                    int(begin_date_string[0]))
        end_date_string = end_date_string.split('/')
        end_date = datetime.date(int(end_date_string[2]),
                                    int(end_date_string[1]),
                                    int(end_date_string[0]))
        autocall = Autocall(underlyings, maturity, frequency, strike, barrier,
                            barrier_type, coupon, autocall_trigger, coupon_trigger,
                            nbr_non_callable_obs)
        backtest_result = backtest(autocall, start_date, end_date)
        id = str(uuid.uuid4())
        create_report(id, autocall, start_date, end_date, backtest_result)
        send_mail([email],
                    'Backtest result - ' + autocall.underlyings_string + ' - ' + time.strftime("%d/%m/%Y"), id)




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
