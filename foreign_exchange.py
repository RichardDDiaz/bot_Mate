import requests
import json


class NotStatus200Exception(Exception):
    pass


class Foreign_exchange():
    ACTUAL_TAXES = 1.64
    API_GENERAL = 'https://api.cambio.today/v1/quotes/{0}/{1}/json?quantity=1&key=9268|6uv1gKh1oJg1PW63hMUR_TPKjkuuJjN3'

    def __init__(self, coin1, coin2="ARS"):
        self.__coin1 = str(coin1)
        self.__coin2 = str(coin2)
        self.__conversion = self.__coin1 + " to " + self.__coin2
        self.__api = Foreign_exchange.API_GENERAL.format(
            self.__coin1, self.__coin2)
        try:
            if requests.get(self.__api).status_code != 200:
                raise NotStatus200Exception("Failure GET Request")

        except Exception as e:
            print(f'Exception - {e}, {type(e)}')

        print(f"class foreign_exchange {self.__conversion} created")

    def __str__(self):
        return(
            f"""
        {self.__conversion}
        Taxes Argentina: {Foreign_exchange.ACTUAL_TAXES}
        {self.__api}""")

    def exchange_rate(self):
        try:
            responseChange = json.loads(requests.get(self.__api).text)
        except Exception as e:
            print(f'Exception - {e}, {type(e)}')
            return "this moment the page to convert is no running, please try again later"
        value_real = f'1 dollar in pesos are: {responseChange["result"]["value"]} ARS'
        value_taxes = f'1 dollar in pesos + full taxes are: {str(float(responseChange["result"]["value"])*Foreign_exchange.ACTUAL_TAXES)} ARS'

        return f'{value_real} \n{value_taxes}'
