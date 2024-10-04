"""Module representing an Exchange"""

from decimal import Decimal
from common.order import Order
from common.orderbook import OrderBook


class Exchange:
    """Class representing an Exchange"""

    def __init__(self, name, api_url, query_params, price_key, quantity_key):
        """Exchange Constructor"""

        self.name = name
        self.api_url = api_url
        self.query_params = query_params
        self.price_key = price_key
        self.quantity_key = quantity_key
        self.orderbook = {}

    def get_product_orderbook(self):
        """Function to get the product order book"""

        raise NotImplementedError()

    def add_orders_to_orderbook(self, bids_q: OrderBook, offers_q: OrderBook):
        """Function to add the orders to the OrderBook"""

        self.__add_bids_to_orderbook(bids_q=bids_q)

        self.__add_offers_to_orderbook(offers_q=offers_q)

    def __add_bids_to_orderbook(self, bids_q: OrderBook):
        """Function to add bids to the OrderBook"""

        for bid in self.orderbook["bids"]:

            order_dict = dict(
                price=Decimal(bid[self.price_key]),
                quantity=Decimal(bid[self.quantity_key]),
            )

            # Create an Order
            order = Order(order=order_dict, is_bid=True)

            # Add the Order to queue
            bids_q.put(order)

    def __add_offers_to_orderbook(self, offers_q: OrderBook):
        """Function to add offers to the OrderBook"""

        for ask in self.orderbook["asks"]:

            order_dict = dict(
                price=Decimal(ask[self.price_key]),
                quantity=Decimal(ask[self.quantity_key]),
            )

            # Create an Order
            order = Order(order=order_dict, is_bid=False)

            # Add the Order to queue
            offers_q.put(order)
