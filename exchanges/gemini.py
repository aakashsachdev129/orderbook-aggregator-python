"""Gemini Module"""

import requests
from common.exchange import Exchange


class Gemini(Exchange):
    """Class representing the Gemini Exchange"""

    def get_product_orderbook(self):
        """Function to get the product order book"""

        response = requests.get(self.api_url, params=self.query_params)
        self.orderbook = response.json()
