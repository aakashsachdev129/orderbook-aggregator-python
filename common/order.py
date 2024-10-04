"""Module representing an Order"""


class Order:
    """Class representing the Order"""

    def __init__(self, order, is_bid: bool):
        """Order Constructor"""

        self.order = order
        self.is_bid = is_bid

    def __lt__(self, other):
        return (
            self.order["price"] > other.order["price"]
            if self.is_bid
            else self.order["price"] < other.order["price"]
        )

    def __eq__(self, other):
        return self.order["price"] == other.order["price"]
