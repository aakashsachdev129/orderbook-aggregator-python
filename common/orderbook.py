"""Module representing an OrderBook"""

from queue import PriorityQueue


class OrderBook(PriorityQueue):
    """Class representing an OrderBook"""

    def update_min_quantity(self, new_quantity):
        """Function to update the quantity of the root element"""

        self.queue[0].order["quantity"] = new_quantity

    def get_min(self):
        """Function to get the value of the root element"""

        return self.queue[0]
