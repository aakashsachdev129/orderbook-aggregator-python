"""Module representing an Orderbook Aggregator"""

from decimal import Decimal
from common.orderbook import OrderBook
from exchanges.coinbase import Coinbase
from exchanges.gemini import Gemini
from exchanges.kraken import Kraken
import json


class Aggregator:
    """Class representing an Orderbook Aggregator"""

    def __init__(self):
        """Aggregator Constructor"""

        self.bids_q = OrderBook()
        self.offers_q = OrderBook()

    def get_orderbooks(self, add_kraken):
        """Function to get the orderbooks"""

        self.__get_exchange_orderbook("coinbase")

        self.__get_exchange_orderbook("gemini")

        if add_kraken == "y":
            self.__get_exchange_orderbook("kraken")

    def __get_exchange_orderbook(self, exchange_name: str):
        """Function to get the exchange orderbook"""

        try:
            exchange = self.__get_exchange_object(exchange_name)

            # Fetch orderbook data
            exchange.get_product_orderbook()

            # add orderbook data to priority queue
            exchange.add_orders_to_orderbook(bids_q=self.bids_q, offers_q=self.offers_q)
        except Exception as e:
            print(f"An Error occured while fetching {exchange_name} orderbook: {e}")

    def __get_exchange_object(self, exchange_name: str):
        """Function to get the exchange object"""

        config = self.__get_config("config.json")

        match exchange_name:
            case "coinbase":
                # Initialize exchange object
                return Coinbase(
                    name=config["coinbase"]["name"],
                    api_url=config["coinbase"]["api_url"],
                    query_params=config["coinbase"]["query_params"],
                    price_key=config["coinbase"]["price_key"],
                    quantity_key=config["coinbase"]["quantity_key"],
                )
            case "gemini":
                # Initialize exchange object
                return Gemini(
                    name=config["gemini"]["name"],
                    api_url=config["gemini"]["api_url"],
                    query_params=config["gemini"]["query_params"],
                    price_key=config["gemini"]["price_key"],
                    quantity_key=config["gemini"]["quantity_key"],
                )
            case "kraken":
                # Initialize exchange object
                return Kraken(
                    name=config["kraken"]["name"],
                    api_url=config["kraken"]["api_url"],
                    query_params=config["kraken"]["query_params"],
                    price_key=config["kraken"]["price_key"],
                    quantity_key=config["kraken"]["quantity_key"],
                )
            case _:
                raise ValueError()

    def __get_config(self, config_file):
        """Function to load config"""

        with open(config_file, "r") as jsonfile:
            return json.load(jsonfile)

    def market_order(self, quantity: Decimal, is_buy: bool):
        """Function to send a buy/sell market order"""

        if is_buy:
            return self.__execute_order(quantity=quantity, orderbook=self.offers_q)
        else:
            return self.__execute_order(quantity=quantity, orderbook=self.bids_q)

    def __execute_order(self, quantity: Decimal, orderbook: OrderBook):
        """Function to execute a buy/sell market order"""

        remaining_quantity = quantity
        total_cost = Decimal(0.0)

        try:
            while remaining_quantity > 0:
                try:
                    current_order = orderbook.get_min()
                except Exception as e:
                    print(
                        f"An Error occurred while fetching the next order from orderbook: {e}"
                    )
                    raise Exception(e)

                current_order_price = Decimal(current_order.order["price"])
                current_order_quantity = Decimal(current_order.order["quantity"])

                if remaining_quantity >= current_order_quantity:
                    total_cost += current_order_price * current_order_quantity

                    orderbook.get()

                    remaining_quantity -= current_order_quantity
                else:
                    total_cost += current_order_price * remaining_quantity

                    reduced_order_quantity = current_order_quantity - remaining_quantity
                    orderbook.update_min_quantity(new_quantity=reduced_order_quantity)

                    remaining_quantity = 0
        except Exception as e:
            print(f"An Error occurred while executing the order: {e}")
        finally:
            return (total_cost, remaining_quantity)
