import requests

API_KEY = 'KNZX'



def historical_data(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol='
    url_api = '&apikey=' + API_KEY
    data = requests.request('GET',url + ticker + url_api).json()["Time Series (Daily)"]

    for key in data.keys():
        data[key] = data[key]['5. adjusted close']


    return data
