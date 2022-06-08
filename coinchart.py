import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

import plotly.express as px
import requests


class Livecoinwatch:
    def __init__(self, token, start_time=None, end_time=None, crypto=None, period=30):
        self.token = token
        self.url = 'https://api.livecoinwatch.com/coins/single/history/'
        self.header = {'x-api-key': self.token, 'content-type': 'application/json'}
        self.end_time = self.convert_to_miliseconds(end_time or datetime.now())
        self.start_time = self.convert_to_miliseconds(start_time) or int(
            self.end_time - timedelta(days=period).total_seconds() * 1000
        )
        self.crypto = crypto or ['BTC']
        self.body_list = self.construct_body_list()

    def convert_to_miliseconds(self, date):
        return int(date.timestamp() * 1000) if date else None

    def construct_body_list(self):
        return [
            {
                'currency': 'USD',  # Only USD is supported.
                'code': crypto,
                'start': self.start_time,
                'end': self.end_time,
                'meta': True,
            }
            for crypto in self.crypto
        ]

    def query(self):
        results = []
        responses = [
            requests.post(self.url, data=json.dumps(body), headers=self.header)
            for body in self.body_list
        ]
        for response in responses:
            result = response.json()
            result = {
                'name': result['name'],
                'history': [
                    {
                        'price': segment['rate'],
                        'date': datetime.fromtimestamp(segment['date'] / 1000.0),
                    }
                    for segment in result['history']
                ],
            }
            results.append(result)
        return results

    def get_exchange_rates(self, crpytos: List[Dict]) -> Dict:
        '''
        Input: (Should be a list of two dictionaries.)
            [
                {
                    'name': <String>,
                    'history': [
                        {
                            'price': <Float>,
                            'date': <Unix Timestamp in miliseconds>
                        },
                        ...
                    ]
                },
                {
                    'name': <String>,
                    'history': [
                        {
                            'price': <Float>,
                            'date': <Unix Timestamp in miliseconds>
                        },
                        ...
                    ]
                },
            ]
        Output:
            {
                'name': <String>,
                'history': [
                    {
                        'price': <Float>,
                        'date': <Unix Timestamp in miliseconds>
                    },
                    ...
                ]
            },
        '''

        crypto_one = crpytos[0]
        crypto_two = crpytos[1]
        name = f'{crypto_one["name"]} / {crypto_two["name"]} Exchange Rate'
        history = []
        for index, value in enumerate(crypto_one['history']):
            if value['date'] == crypto_two['history'][index]['date']:
                history.append(
                    {
                        'price': value['price'] / crypto_two['history'][index]['price'],
                        'date': value['date'],
                    }
                )
        return {
            'name': name,
            'history': history,
        }

    def get_graph(self, exchanges: Dict, mode='show'):
        fig = px.line(
            x=[segment['date'] for segment in exchanges['history']],
            y=[segment['price'] for segment in exchanges['history']],
            title=exchanges['name'],
            labels={'x': 'Date', 'y': 'Price'},
            line_shape='spline',
        )
        if mode == 'show':
            fig.show()
        elif mode == 'to_image':
            fig.write_image('./static/exchange_rate.png')
        elif mode == 'to_coin_image':
            fig.write_image(f'./static/{self.crypto[0]}.png')

    def run(self, mode='show'):
        results = self.query()
        results = self.get_exchange_rates(results)
        self.get_graph(results, mode)

    def get_coin_chart(self, mode='show'):
        results = self.query()
        self.get_graph(results[0], mode)
