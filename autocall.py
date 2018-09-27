

def int_to_date(date):
    """
    Transform date to string
    """

    nbr_years = int(date)
    nbr_months = int((date - nbr_years)*12)
    maturity_string = ''
    if nbr_years != 0:
        if nbr_years > 1:
            maturity_string += str(nbr_years) + ' Years'
        else:
            maturity_string += str(nbr_years) + ' Year'

        if nbr_months != 0:
            if nbr_months > 1:
                maturity_string += ', ' + str(nbr_months) + ' Months'
            else:
                maturity_string += ', ' + str(nbr_months) + ' Month'
    else:
        if nbr_months > 1:
            maturity_string += str(nbr_months) + ' Months'
        else:
            maturity_string += str(nbr_months) + ' Month'

    return maturity_string

def underlyings_to_string(underlyings):
    """
    Convert the list of tickers to a string
    """

    if len(underlyings) == 1:
        underlyings_info = underlyings[0]
    else:
        underlyings_info = ""
        for index, underlying in enumerate(underlyings):
            if index != len(underlyings)-1:
                underlyings_info += underlying + ' / '
            else:
                underlyings_info += underlying



class Autocall:

    def __init__(self, underlyings, maturity, frequency, strike, barrier,
                barrier_type, coupon, autocall_trigger, coupon_trigger,  nbr_non_callable_obs=1,
                coupon_guaranteed=False, memory_effect=False):
        """
        Store each caracteristic in the object
        """

        Autocall.underlyings = underlyings
        Autocall.underlyings_string = underlyings_to_string(underlyings)
        Autocall.maturity = maturity
        Autocall.frequency = frequency
        Autocall.strike = strike
        Autocall.barrier = barrier
        Autocall.coupon = coupon
        Autocall.barrier_type = barrier_type
        Autocall.autocall_trigger = autocall_trigger
        Autocall.coupon_trigger = coupon_trigger
        Autocall.nbr_non_callable_obs = nbr_non_callable_obs
        Autocall.coupon_guaranteed = coupon_guaranteed
        Autocall.memory_effect = memory_effect



    def get_info(self):
        """
        Returns a formated info table to display on the PDF
        """




        return [{'field':'Underlyings','value':self.underlyings_string},
                {'field':'Maturity','value':int_to_date(self.maturity)},
                {'field':'Period','value':int_to_date(self.frequency)},
                {'field':'Barrier','value':str(self.barrier) + ' %'},
                {'field':'Barrier type','value':self.barrier_type},
                {'field':'Strike','value':str(self.strike) + ' %'},
                {'field':'Coupon (p.a.)','value':str(self.coupon) + ' %'},
                {'field':'Autocall trigger','value':str(self.autocall_trigger) + ' %'},
                {'field':'Coupon trigger','value':str(self.coupon_trigger) + ' %'},]
