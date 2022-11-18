import requests
import json
import datetime


class Conversion:
    def __init__(self, date, curr_from, curr_to, ratio):
        self.date = date
        self.curr_from = curr_from
        self.curr_to = curr_to
        self.ratio = ratio

    def get_all_values(self):
        return self.date, self.curr_from, self.curr_to, self.ratio


class Currency_converter:

    def __init__(self):
        pass

    @classmethod
    def history_ratios(cls, date='', curr_from='', curr_to='') -> int:
        """
        This method is searching for specific day of currency ratio which is then used to compare with
        the current date
        :param date: date of currency ratio
        :param curr_from: currency used to buy desired currency
        :param curr_to: desired currency
        :return: currency "ratio" of previous or specific day not exceeding one year ago
        """
        url = 'https://api.fastforex.io/historical?date=' + date + '&from=' + curr_from + '&to=' + curr_to + \
              '&api_key=f88e964a1c-0f1d5d0477-rlcaeb'

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        response_info = json.loads(response)
        ratio_results = response_info['results']
        ratio = 0
        for i in ratio_results:
            ratio = round(ratio_results.get(i), 2)

        return ratio

    @classmethod
    def currency_exchange(cls):
        """
        This method will prompt user to enter currencies to exchanged of specific amount of money then it will compare
        with page whether they exist and if so it will exchange them and store them in database.

        :return: currency ratio of actual and previous day for comparison and also a currencies which will be
        exchanged in specific amount of money
        """
        list_of_conversions = []
        # user inputs from local method
        curr_from, curr_to, amount = Currency_converter.user_inputs()

        # searching for exchange ratio of actual day2
        url = 'https://api.fastforex.io/fetch-multi?from=' + curr_from + '&to=' + curr_to + '&amount=' + amount + \
              '&api_key=f88e964a1c-0f1d5d0477-rlcaeb'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        response_info = json.loads(response)
        ratio_results = response_info['results']
        current_ratio = 0
        for i in ratio_results:
            current_ratio = round(ratio_results.get(i), 2)

        # current time and yesterday from local method
        current_date, previous_date = Currency_converter.getTime()
        prev_day_ratio = Currency_converter.history_ratios(previous_date, curr_from, curr_to)

        # comparing current ratio and ratio of previous date
        if prev_day_ratio < current_ratio:
            print(f'\33[0;32;40m {current_ratio} \033[0;0m')
            current_ratio = str(current_ratio) + ">"
        else:
            print(f'\33[0;31;40m {current_ratio} \033[0;0m')
            current_ratio = str(current_ratio) + "<"

        conversion = Conversion(current_date, curr_from, curr_to, current_ratio)

        return conversion.get_all_values()

    @classmethod
    def menu_of_currencies(cls) -> list:
        """
        This method will store all currencies provided by the page and then store it into the list 'currencies'
        :return: all available currencies
        """
        currencies = []
        # url to all currencies provided by this page which will be then stored in the list 'currencies'
        currencies_url = 'https://api.fastforex.io/currencies?api_key=f88e964a1c-0f1d5d0477-rlcaeb'
        headers = {"accept": "application/json"}
        response = requests.get(currencies_url, headers=headers).text
        response_info = json.loads(response)

        # iteration over dictionary to store all the currencies
        for currency in response_info["currencies"]:
            currencies.append(currency)

        return currencies

    @classmethod
    def user_inputs(cls) -> tuple:
        """
        This method prompt users to enter values and evaluates their inputs. If it is incorrect it asks them to do it
        again and if not it will store it into the list 'currencies'
        :return: tuple of values: currency paid with; desired currency; amount of money used to buy desired currency
        """

        input_values = []
        currencies = Currency_converter.menu_of_currencies()

        while True:
            curr_from = str(input("Enter currency you want to pay with: ").upper())
            curr_to = str(input("Enter currency you want to buy: ").upper())
            amount = input("How much money you want to spend: ")
            if amount.isnumeric():
                if (curr_from not in currencies) or (curr_to not in currencies) or (int(amount) <= 0):
                    print("At least one of the values is inappropriate, please enter them again.")
                else:
                    input_values += [curr_from, curr_to, str(amount)]
                    break
            else:
                print("You have used alphabet instead of numeric value, do it again please.")
        return tuple(input_values)

    @classmethod
    def getTime(cls):
        """
        Catches time and date15 of current day and previous day date
        :return current day time and previous day:
        """
        date = datetime.datetime.now()
        current_day = date.strftime("%Y-%m-%d %H:%M:%S")
        previous_day = datetime.datetime.today() - datetime.timedelta(days=1)
        previous_day = previous_day.strftime("%Y-%m-%d")

        return current_day, previous_day
