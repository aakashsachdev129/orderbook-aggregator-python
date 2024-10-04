"""Kraken Module"""

import requests
from common.exchange import Exchange


class Kraken(Exchange):
    """Class representing the Kraken Exchange"""

    def get_product_orderbook(self):
        """Function to get the product order book"""

        payload = {}
        headers = {"Accept": "application/json"}

        response = requests.get(
            self.api_url, params=self.query_params, headers=headers, data=payload
        )
        data = response.json()

        self.orderbook = data["result"]["XXBTZUSD"]
