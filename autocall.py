


class Autocall:

    def __init__(self, underlyings, maturity, frequency, strike, barrier,
                barrier_type, coupon, autocall_trigger, coupon_trigger,  nbr_non_callable_obs=1,
                coupon_guaranteed=True, memory_effect=False):
        """
        Store each caracteristic in the object
        """

        Autocall.underlyings = underlyings
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

        if len(self.underlyings) == 1:
            underlyings_info = self.underlyings[0]
        else:
            underlyings_info = ""
            for index, underlying in enumerate(self.underlyings):
                if index != len(self.underlyings)-1:
                    underlyings_info += underlying + ' / '
                else:
                    underlyings_info += underlying

        nbr_years = int(self.maturity)
        nbr_months = self.maturity - nbr_years
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

        return [{'column':'Underlyings','value':underlyings_info},
                {'column':'Maturity','value':maturity_string},
                {'column':'Barrier','value':str(self.barrier) + ' %'},
                {'column':'Strike','value':str(self.strike) + ' %'}]
