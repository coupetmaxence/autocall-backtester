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

    # Number of backtest realized
    nbr_backtests = len(basket_data.keys())

    # Empty dictionnary to store simulated ARR
    ARR = {}

    # dictionnary to store early redemption distribution
    early_distribution = {}

    for period in range(1,int(autocall.maturity/autocall.frequency)):
        early_distribution['Period ' + str(period)] = 0

    early_distribution['Period ' +
                        str(int(autocall.maturity/autocall.frequency)) +
                        ' no barrier'] = 0
    early_distribution['Period ' +
                        str(int(autocall.maturity/autocall.frequency)) +
                        ' barrier'] = 0


    # Check if there has been an autocall and store autocall date
    for starting_date in basket_data.keys():
        starting_datetime = datetime.datetime.strptime(starting_date,'%Y-%m-%d')
        list_dates = list(basket_data[starting_date]['worstof'].index)
        list_dates = [datetime.datetime.strptime(x,'%Y-%m-%d') for x in list_dates]
        coupon_periods = range(1,int(autocall.maturity/autocall.frequency)+1)

        coupon_dates = [nearest(starting_datetime +
                                    i*datetime.timedelta(weeks=52*autocall.frequency),
                                    list_dates) for i in coupon_periods]
        callable_dates = coupon_dates[autocall.nbr_non_callable_obs:-1]


        callable_dates_str = [x.strftime('%Y-%m-%d') for x in callable_dates]
        coupon_dates_str = [x.strftime('%Y-%m-%d') for x in coupon_dates]

        basket_callable_dates = basket_data[starting_date]['worstof'].loc[callable_dates_str]
        basket_coupon_dates = basket_data[starting_date]['worstof'].loc[coupon_dates_str]

        coupon = 0
        basket_data[starting_date]['autocall'] = False

        for period, date_coupon in enumerate(coupon_dates_str):

            # Get worst of value
            basket_value = basket_data[starting_date]['worstof']['worstof'].loc[date_coupon]
            basket_data[starting_date]['last-period'] = period + 1

            # add coupon if coupon trigger is reached
            if basket_value > autocall.coupon_trigger:
                coupon += autocall.coupon * autocall.frequency

            # check for autocalls
            if date_coupon in callable_dates_str and basket_value > autocall.autocall_trigger:
                basket_data[starting_date]['autocall'] = True
                break

        # Check for barrier event if no autocall
        if basket_data[starting_date]['autocall'] == False:
            end_value = basket_data[starting_date]['worstof']['worstof'].loc[coupon_dates_str[-1]]
            min_value = basket_data[starting_date]['worstof']['worstof'].min()

            barrier_event_eu = autocall.barrier_type == 'EU' and  end_value < autocall.barrier
            barrier_event_us = autocall.barrier_type == 'US' and min_value < autocall.barrier
            if barrier_event_eu or barrier_event_us:
                basket_data[starting_date]['barrier-event'] = True
                coupon += min(autocall.strike - end_value, 0)
                early_distribution['Period ' +
                                    str(basket_data[starting_date]['last-period']) +
                                    ' barrier'] += 1
            else:
                early_distribution['Period ' +
                                    str(basket_data[starting_date]['last-period']) +
                                    ' no barrier'] += 1
        else:
            early_distribution['Period ' + str(basket_data[starting_date]['last-period'])] += 1

        coupon = coupon / (basket_data[starting_date]['last-period']*autocall.frequency)

        ARR[starting_date] = coupon







    return {'historical-data': historical_data,
            'nbr-backtests':nbr_backtests,
            'arr':ARR,
            'early_redemption':early_distribution}










"""
start_date = datetime.date(2008, 9, 5)
end_date = datetime.date.today()
autocall = Autocall(["MSFT", "AAPL"], 2, 0.5, 100, 70, 'US', 4, 100, 100)
#print(download_data_basket(["MSFT","AAPL"], start_date, end_date, 0.5))
#print(autocall.get_info())
print(backtest(autocall, start_date, end_date)['early_redemption'])
"""
