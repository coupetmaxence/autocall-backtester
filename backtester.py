from financial_data import historical_data
import pandas as pd
import datetime
from pandas.io.json import json_normalize
from autocall import Autocall




def download_data_basket(underlyings, start_date, end_date, maturity):
    """
    Download hisotirical data for a given basket, determine each starting date
    of a backtest and for each backtest compute worst of at each time
    """

    list_dataframes = []

    # Dowload all the historic data for each underlying
    for underlying in underlyings:
        hist_data = json_normalize(historical_data(underlying))
        hist_data = hist_data.transpose()
        hist_data.columns = [underlying]
        hist_data[underlying] = pd.to_numeric(hist_data[underlying])
        list_dataframes.append(hist_data)

    # Join all data in only one dataframe
    basket_data = pd.concat(list_dataframes, axis=1, join='inner')

    # Filter to get only dates of interest
    basket_data = basket_data.loc[start_date.strftime('%Y-%m-%d'):end_date.strftime('%Y-%m-%d')]

    # Historical data
    hist_data = basket_data.divide(basket_data.ix[0] / 100)

    # Compute the last date a backtest should be launched
    last_backtesting_start_date = end_date - datetime.timedelta(weeks=52*maturity)

    # list of dates where a backtest begins
    backtesting_start_dates = list(basket_data.loc[start_date.strftime('%Y-%m-%d'):last_backtesting_start_date.strftime('%Y-%m-%d')].index)

    worstof_baskets = {}

    # for each starting date of a backtest, compute the worst of the basket at each time
    for starting_date in backtesting_start_dates:
        end_backtest = datetime.datetime.strptime(starting_date,'%Y-%m-%d') + datetime.timedelta(weeks=52*maturity)

        # Compute returns over the period
        worstof_data = basket_data.loc[starting_date:end_backtest.strftime('%Y-%m-%d')]
        worstof_data = worstof_data.divide(worstof_data.ix[0]/100)

        # Compute worst of
        worstof_data['worstof'] = worstof_data.min(axis=1)

        worstof_baskets[starting_date] = {}
        worstof_baskets[starting_date]['worstof'] = worstof_data

    return hist_data, worstof_baskets






def nearest(variable, items):
    """
    Returns the nearest value of a variable inside a list
    Used to find the nearest
    """

    return min(items, key=lambda x: abs(x - variable))






def backtest(autocall, start_date, end_date):

    """
    Realize the entire backtest for variants of autocalls
    """

    # download backtest historical data
    historical_data, basket_data = download_data_basket(autocall.underlyings, start_date,
                                        end_date, autocall.maturity)

    nbr_backtests = len(basket_data.keys())

    # Check if there has been an autocall and store autocall date
    for starting_date in basket_data.keys():
        starting_datetime = datetime.datetime.strptime(starting_date,'%Y-%m-%d')
        list_dates = list(basket_data[starting_date]['worstof'].index)
        list_dates = [datetime.datetime.strptime(x,'%Y-%m-%d') for x in list_dates]
        callable_periods = range(autocall.nbr_non_callable_obs+1,int(autocall.maturity/autocall.frequency)+1)
        coupon_periods = range(0,int(autocall.maturity/autocall.frequency)+1)

        callable_dates = [nearest(starting_datetime +
                                    i*datetime.timedelta(weeks=52*autocall.frequency),
                                    list_dates) for i in callable_periods]
        coupon_dates = [nearest(starting_datetime +
                                    i*datetime.timedelta(weeks=52*autocall.frequency),
                                    list_dates) for i in coupon_periods]

        callable_dates_str = [x.strftime('%Y-%m-%d') for x in callable_dates]
        coupon_dates_str = [x.strftime('%Y-%m-%d') for x in coupon_dates]

        basket_callable_dates = basket_data[starting_date]['worstof'].loc[callable_dates_str]
        basket_coupon_dates = basket_data[starting_date]['worstof'].loc[coupon_dates_str]

        try:
            _ = len(autocall.autocall_trigger)
            autocall_schedule = autocall.autocall_trigger
        except:
            autocall_schedule = [autocall.autocall_trigger]*int((autocall.maturity/autocall.frequency) - autocall.nbr_non_callable_obs)


        for index, autocall_trigger in enumerate(autocall_schedule):
            if basket_callable_dates['worstof'].loc[callable_dates_str[index]] > autocall_trigger:
                basket_data[starting_date]['autocall'] = True
                basket_data[starting_date]['autocall_date'] = callable_dates_str[index]
                break

        try:
            _ = basket_data[starting_date]['autocall']
            coupon = coupon ** (1 / ())
        except:
            basket_data[starting_date]['autocall'] = False


        try:
            _ = len(autocall.coupon_trigger)
        except:
            autocall.coupon_trigger = [autocall.coupon_trigger]*int((autocall.maturity/autocall.frequency))



        if basket_data[starting_date]['autocall']:
            for coupon_date in coupon_dates:
                if coupon_date == basket_data[starting_date]['autocall_date']:
                    break

        else:
            for coupon_date in coupon_dates:
                pass


        return {'historical-data': historical_data,
                'nbr-backtests':nbr_backtests}










"""
start_date = datetime.date(2008, 9, 5)
end_date = datetime.date.today()
autocall = Autocall(["MSFT", "AAPL"], 2, 0.5, 100, 70, 'US', 4, 100, 100)
#print(download_data_basket(["MSFT","AAPL"], start_date, end_date, 0.5))
#print(autocall.get_info())
backtest(autocall, start_date, end_date)
"""
