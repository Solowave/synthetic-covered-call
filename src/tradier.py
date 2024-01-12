import requests
import pandas as pd
import numpy as np


class Tradier:
    def __init__(self, access_token):
        self.access_token = access_token

    def getPriceChanges(self, symbol, start_date, end_date):
        response = requests.get('https://api.tradier.com/v1/markets/history',
                                params={'symbol': symbol, 'interval': 'daily',
                                        'start': start_date, 'end': end_date, 'session_filter': 'all'},
                                headers={'Authorization': 'Bearer ' +
                                         self.access_token, 'Accept': 'application/json'}
                                )

        json_response = response.json()
        data = pd.DataFrame(json_response['history']['day'])

        data['change'] = data['open'].pct_change()
        return data[['date', 'change']]

    def getVolatility(self, symbol, start_date, end_date):
        response = requests.get('https://api.tradier.com/v1/markets/history',
                                params={'symbol': symbol, 'interval': 'daily',
                                        'start': start_date, 'end': end_date, 'session_filter': 'all'},
                                headers={'Authorization': 'Bearer ' +
                                         self.access_token, 'Accept': 'application/json'}
                                )

        json_response = response.json()
        data = pd.DataFrame(json_response['history']['day'])

        data['date'] = pd.to_datetime(data['date'])

        count = data['open'].count()

        mean = data['open'].mean()

        data['residual'] = data['open'] - mean
        data['rs'] = pow(data['residual'], 2)

        variance = data['rs'].mean()

        daily_std = np.sqrt(variance) / np.sqrt(count)
        # print("Daiy Standard Deviation:", daily_std)

        return daily_std

    def getSymbolExpirationDates(self, symbol):
        response = requests.get('https://api.tradier.com/v1/markets/options/expirations',
                                params={'symbol': symbol, 'includeAllRoots': 'true',
                                        'contractSize': 'true', 'expirationType': 'true'},
                                headers={'Authorization': 'Bearer ' +
                                         self.access_token, 'Accept': 'application/json'}
                                )
        json_response = response.json()
        dates = [entry['date']
                 for entry in json_response['expirations']['expiration']]
        return dates

    def getOptionChain(self, symbol, expiration_date):
        response = requests.get('https://api.tradier.com/v1/markets/options/chains',
                                params={
                                    'symbol': symbol, 'expiration': expiration_date, 'greeks': 'true'},
                                headers={'Authorization': 'Bearer ' +
                                         self.access_token, 'Accept': 'application/json'}
                                )

        return response.json()

    def getMarketPrice(self, symbol):
        response = requests.get('https://api.tradier.com/v1/markets/quotes',
                                params={'symbols': symbol, 'greeks': 'false'},
                                headers={'Authorization': 'Bearer ' +
                                         self.access_token, 'Accept': 'application/json'}
                                )


        json_response = response.json()
        price = json_response['quotes']['quote']['last']
        return price
