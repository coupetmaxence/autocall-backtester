# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
import datetime
from pandas.io.json import json_normalize
import json
from test_report import create_report, send_mail
from autocall import Autocall
import uuid
import time

app = dash.Dash(__name__)
server = app.server


# Describe the layout, or the UI, of the app
app.layout = html.Div([

    html.Div([

    html.Header([
        html.Div([], className="mdl-layout--large-screen-only mdl-layout__header-row"),
        html.Div([
        html.H3("Autocall backtester")
        ], className="mdl-layout--large-screen-only mdl-layout__header-row"),
        html.Div([], className="mdl-layout--large-screen-only mdl-layout__header-row"),
        html.Div([

        html.A(['Tool'], className="mdl-layout__tab is-active"),
        html.A(['About'], href='https://github.com/coupetmaxence/autocall-backtester', className="mdl-layout__tab"),
        ],className="mdl-layout__tab-bar mdl-js-ripple-effect mdl-color--primary-dark")

    ], className="mdl-layout__header mdl-layout__header--scroll mdl-color--primary"),




    html.Main([


    html.Div([

    html.Section([

    html.Div([

    html.Div([

    html.H4(['Product parameters']),


    html.Div([





        html.Div([
        html.P('Underlyings'),
        dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL',
        multi=True
        )], className="mdl-cell mdl-cell--6-col"),
        html.Div([
        html.P('Maturity (years)'),
        dcc.Input(
        placeholder='Enter maturity',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Frequency (years)'),
        dcc.Input(
        placeholder='Enter frequency',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Strike (%)'),
        dcc.Input(
        placeholder='Enter strike',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Non-callable observations'),
        dcc.Input(
        placeholder='Enter nbr non-callable obs',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Barrier (%)'),
        dcc.Input(
        placeholder='Enter barrier',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Barrier type'),
        dcc.Dropdown(
        options=[
            {'label': 'European', 'value': 'EU'},
            {'label': 'Daily', 'value': 'DAILY'}
        ],
        value='EU'
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Autocall trigger'),
        dcc.Input(
        placeholder='Enter autocall trigger',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('Coupon trigger'),
        dcc.Input(
        placeholder='Enter coupon trigger',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col")


    ], className='mdl-grid')














    ], className="mdl-card__supporting-text")

    ], className="mdl-card mdl-cell mdl-cell--12-col-desktop mdl-cell--6-col-tablet mdl-cell--4-col-phone"),


    ], className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp")

    ], className="mdl-layout__tab-panel is-active"),


    html.Div([

    html.Section([

    html.Div([

    html.Div([

    html.H4(['Backtest parameters']),


    html.Div([




        html.Div([
        html.P('Backtesting dates'),
        dcc.Input(
        placeholder='Beggining date',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--3-col"),
        html.Div([
        html.P('text', style={'visibility':'hidden'}),
        dcc.Input(
        placeholder='Ending date',
        type='text',
        value=''
        )], className="mdl-cell mdl-cell--9-col"),

        html.Div([
        html.P("Client's email address"),
        dcc.Input(
        placeholder='email address',
        type='text',
        value='')], className="mdl-cell mdl-cell--3-col")



    ], className='mdl-grid')














    ], className="mdl-card__supporting-text")

    ], className="mdl-card mdl-cell mdl-cell--12-col-desktop mdl-cell--6-col-tablet mdl-cell--4-col-phone"),


    ], className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp")

    ], className="mdl-layout__tab-panel is-active")

    ], className="mdl-layout__content"),




    html.A(['Launch backtest'], id="view-source", className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--accent mdl-color-text--accent-contrast")




    ], className="mdl-layout mdl-js-layout mdl-layout--fixed-header"),

    html.Div([], style={'display':'none'}, id='output')

], className="mdl-demo mdl-color--grey-100 mdl-color-text--grey-700 mdl-base")

@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('view-source', 'n_clicks')])
def set_display_children(nclicks):
    if nclicks != None:
        start_date = datetime.date(2008, 9, 5)
        end_date = datetime.date.today()
        autocall = Autocall(["MSFT", "AAPL"], 2, 0.5, 100, 70, 'US', 4, 100, 100)
        id = str(uuid.uuid4())
        create_report(id, autocall, start_date, end_date)
        send_mail(['maxence.coupet@gmail.com'],
                    'Backtest result - ' + time.strftime("%d/%m/%Y"), id)


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
                "https://code.jquery.com/jquery-3.2.1.min.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
