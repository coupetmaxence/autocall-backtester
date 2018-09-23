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

app = dash.Dash(__name__)
server = app.server

# read data for tables (one df per table)
df_fund_facts = pd.read_csv('https://plot.ly/~bdun9/2754.csv')

product_info = [{'column': 'Underlyings', 'value': 'MSFT / AAPL'}, {'column': 'Maturity', 'value': '2 Years'},
{'column': 'Barrier', 'value': '70 %'}, {'column': 'Strike', 'value': '100 %'}]
df_fund_facts = json_normalize(product_info)
df_price_perf = pd.read_csv('https://plot.ly/~bdun9/2756.csv')
df_current_prices = pd.read_csv('https://plot.ly/~bdun9/2753.csv')
df_hist_prices = pd.read_csv('https://plot.ly/~bdun9/2765.csv')
df_avg_returns = pd.read_csv('https://plot.ly/~bdun9/2793.csv')
df_after_tax = pd.read_csv('https://plot.ly/~bdun9/2794.csv')
df_recent_returns = pd.read_csv('https://plot.ly/~bdun9/2795.csv')
df_equity_char = pd.read_csv('https://plot.ly/~bdun9/2796.csv')
df_equity_diver = pd.read_csv('https://plot.ly/~bdun9/2797.csv')
df_expenses = pd.read_csv('https://plot.ly/~bdun9/2798.csv')
df_minimums = pd.read_csv('https://plot.ly/~bdun9/2799.csv')
df_dividend = pd.read_csv('https://plot.ly/~bdun9/2800.csv')
df_realized = pd.read_csv('https://plot.ly/~bdun9/2801.csv')
df_unrealized = pd.read_csv('https://plot.ly/~bdun9/2802.csv')

df_graph = pd.read_csv("https://plot.ly/~bdun9/2804.csv")

# reusable componenets
def make_dash_table(df):
    ''' Return a dash definition of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table







def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Back-testing Analysis    |    {}'.format(datetime.datetime.today().strftime("%d/%m/%Y")))
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header







# Describe the layout, or the UI, of the app
app.layout = html.Div([

    html.Div([
    html.Br(),
    html.H2('Autocall Backtester'),

html.Br(),
html.H4('Product parameters'),

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
    )], className='four columns'),
    html.Div([
    html.P('Maturity (years)'),
    dcc.Input(
    placeholder='Enter maturity',
    type='text',
    value=''
    )], className='two columns'),
    html.Div([
    html.P('Frequency (years)'),
    dcc.Input(
    placeholder='Enter frequency',
    type='text',
    value=''
    )], className='two columns'),
    html.Div([
    html.P('Strike (%)'),
    dcc.Input(
    placeholder='Enter strike',
    type='text',
    value=''
    )], className='two columns'),
    html.Div([
    html.P('Non-callable observations'),
    dcc.Input(
    placeholder='Enter nbr non-callable obs',
    type='text',
    value=''
    )], className='two columns')
], className='row'),

html.Div([
    html.Div([
    html.P('Barrier (%)'),
    dcc.Input(
    placeholder='Enter barrier',
    type='text',
    value=''
    )], className='two columns'),
    html.Div([
    html.P('Barrier type'),
    dcc.Dropdown(
    options=[
        {'label': 'European', 'value': 'EU'},
        {'label': 'Daily', 'value': 'DAILY'}
    ],
    value='EU'
    )], className='two columns'),
    html.Div([
    html.P('Autocall trigger'),
    dcc.Input(
    placeholder='Enter autocall trigger',
    type='text',
    value=''
    )], className='two columns'),
    html.Div([
    html.P('Coupon trigger'),
    dcc.Input(
    placeholder='Enter coupon trigger',
    type='text',
    value=''
    )], className='two columns'),
    html.Div([
    html.P('Coupon guaranteed'),
    dcc.Dropdown(
    options=[
        {'label': 'True', 'value': 'True'},
        {'label': 'False', 'value': 'False'}
    ],
    value='True'
    )], className='two columns'),
    html.Div([
    html.P('Memory effect'),
    dcc.Dropdown(
    options=[
        {'label': 'True', 'value': 'True'},
        {'label': 'False', 'value': 'False'}
    ],
    value='True'
    )], className='two columns')
], className='row'),


html.Br(),
html.H4('Backtest parameters'),

html.Div([
    html.Div([
    html.P('Backtesting dates'),
    dcc.DatePickerRange(
    id='date-picker-range',
    start_date=datetime.datetime(1997, 5, 3),
    end_date_placeholder_text='Select a date!'
    )], className='four columns')
], className='row'),

html.Br(),
html.Button('Launch backtest', id='backtest'),
html.Br(),
html.H4("Backtesting report"),

html.Div([
    html.Div(['fdsfds'],style={'visibility':'hidden'},className='nine columns'),
    html.Div([
    html.Button('PRINT PDF', id='button', className='print')
    ],className='three columns')
], className='row')], style={'padding-left':'2em','padding-right':'2em'},className='no-print'),
    html.Div([  # page 1
            html.Div([

                # Header
                get_header(),
                html.Br([]),

                # Row 3

                html.Div([

                    html.Div([
                        html.H6('Product Description',
                                className="gs-header gs-text-header padded"),

                        html.Br([]),

                        html.P("\
                                Autocallable products (‘autocalls’) are structured \
                                products linked to an underlying asset, which can \
                                automatically mature (or ‘kick out’) prior to their \
                                scheduled maturity date if certain pre-determined \
                                market conditions have been met with regard to the \
                                underlying asset. \
                                An autocall is an investment package which comprises \
                                several financial instruments; a zero coupon bond \
                                combined with call and put options referencing the \
                                underlying asset."),

                    ], className="six columns"),

                    html.Div([
                        html.H6(["Products details"],
                                className="gs-header gs-table-header padded"),
                        html.Table(make_dash_table(df_fund_facts))
                    ], className="six columns"),

                ], className="row "),


                html.Div([

                    html.Div([
                        html.H6('Methodology',
                                className="gs-header gs-text-header padded"),

                        html.Br([]),

                        html.P("\
                                Over the period from 20/01/2001 to 12/08/2017, the returns of \
                                an investments in this product have been simulated. \
                                Each date as been taken as a launch date. 6547 tests \
                                were carried out on similar investments for which \
                                the historical annualized rate of return has been \
                                computed."),

                    ], className="twelve columns")

                ], className="row "),
                # Row 4

                html.Div([

                    html.Div([
                        html.H6("Evolution of the Annualized Rate of Return (%)",
                                className="gs-header gs-table-header padded"),
                        dcc.Graph(
                            id="grpah-2",
                            figure={
                                'data': [
                                    go.Scatter(
                                        x = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"],
                                        y = ["6", "5.5", "0", "4", "6", "6", "-2", "5.5", "5.7", "2", "6"],
                                        line = {"color": "rgb(53, 83, 255)"},
                                        mode = "lines",
                                        name = "500 Index Fund Inv"
                                    )
                                ],
                                'layout': go.Layout(
                                    autosize = False,
                                    title = "",
                                    font = {
                                      "family": "Raleway",
                                      "size": 10
                                    },
                                    height = 200,
                                    width = 340,
                                    hovermode = "closest",
                                    legend = {
                                      "x": -0.0277108433735,
                                      "y": -0.142606516291,
                                      "orientation": "h"
                                    },
                                    margin = {
                                      "r": 20,
                                      "t": 20,
                                      "b": 20,
                                      "l": 50
                                    },
                                    showlegend = False,
                                    xaxis = {
                                      "autorange": True,
                                      "linecolor": "rgb(0, 0, 0)",
                                      "linewidth": 1,
                                      "showgrid": False,
                                      "showline": True,
                                      "title": "",
                                      "type": "linear"
                                    },
                                    yaxis = {
                                      "autorange": True,
                                      "gridcolor": "rgba(127, 127, 127, 0.2)",
                                      "mirror": False,
                                      "nticks": 4,
                                      "showgrid": True,
                                      "showline": True,
                                      "ticklen": 10,
                                      "ticks": "outside",
                                      "type": "linear",
                                      "zeroline": False,
                                      "zerolinewidth": 4
                                    }
                                )
                            },
                            config={
                                'displayModeBar': False
                            }
                        ),
                        html.P('Source : AlphaVantage')
                    ], className="six columns"),


                    html.Div([
                        html.H6('Early redemption distribution',
                                className="gs-header gs-text-header padded"),
                        dcc.Graph(
                            id = "graph-1",
                            figure={
                                'data': [
                                    go.Bar(
                                        x = ["Period 1", "Period 2", "¨Period 3", "Period 4", "Period 5"],
                                        y = ["40", "30", "10", "0", "20"],
                                        name = "500 Index Fund"
                                    ),
                                ],
                                'layout': go.Layout(
                                    autosize = False,
                                    bargap = 0.35,
                                    font = {
                                      "family": "Raleway",
                                      "size": 10
                                    },
                                    height = 200,
                                    hovermode = "closest",
                                    legend = {
                                      "x": -0.0228945952895,
                                      "y": -0.189563896463,
                                      "orientation": "h",
                                      "yanchor": "top"
                                    },
                                    margin = {
                                      "r": 0,
                                      "t": 20,
                                      "b": 20,
                                      "l": 20
                                    },
                                    showlegend = False,
                                    title = "",
                                    width = 340,
                                    xaxis = {
                                      "autorange": True,
                                      "showline": True,
                                      "title": "",
                                      "type": "category"
                                    },
                                    yaxis = {
                                      "autorange": True,
                                      "showgrid": True,
                                      "showline": True,
                                      "title": "",
                                      "type": "linear",
                                      "zeroline": False
                                    }
                                )
                            },
                            config={
                                'displayModeBar': False
                            }
                        ),
                        html.P('Source : AlphaVantage')
                    ], className="six columns"),



                ], className="row "),

                # Row 5

                html.Div([


                    html.Div([
                        html.H6("Underlyings historical data",
                                className="gs-header gs-table-header padded"),
                        dcc.Graph(
                            id="grpah-6",
                            figure={
                                'data': [
                                    go.Scatter(
                                        x = ["2008", "2009", "2010", "2011", "2012"],
                                        y = ["100", "105", "102", "110", "108"],
                                        mode = "lines",
                                        name = "MSFT"
                                    ),
                                    go.Scatter(
                                        x = ["2008", "2009", "2010", "2011", "2012"],
                                        y = ["100", "95", "92", "98", "104"],
                                        mode = "lines",
                                        name = "AAPL"
                                    )
                                ],
                                'layout': go.Layout(
                                    autosize = False,
                                    title = "",
                                    font = {
                                      "family": "Raleway",
                                      "size": 10
                                    },
                                    height = 320,
                                    hovermode = "closest",
                                    legend = {
                                      "x": -0.0277108433735,
                                      "y": -0.142606516291,
                                      "orientation": "h"
                                    },
                                    margin = {
                                      "r": 20,
                                      "t": 20,
                                      "b": 20,
                                      "l": 50
                                    },
                                    showlegend = True,

                                )
                            },
                            config={
                                'displayModeBar': False
                            }
                        ),
                        html.P('Source : AlphaVantage')
                    ], className="twelve columns"),

                ], className="row "),

                html.Br(),
                html.Br(),
                html.P(' Disclaimer : Historical data and simulations are not a reliable \
                        indicator for future development. This tool is \
                        furnishing "as is". The developper does not provide \
                        any warranty of the tool whatsoever, whether express, \
                        implied, or statutory, including, but not limited to, \
                        any warranty of merchantability or fitness for a \
                        particular purpose or any warranty that the contents \
                        of the tool will be error-free.')


            ], className="subpage")

        ], className="page")


])



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/Maxence8/pen/RJrPmb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=True)
