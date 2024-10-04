"""Main Module"""

from decimal import Decimal
import argparse

from aggregator import Aggregator

parser = argparse.ArgumentParser()
parser.add_argument("--buy_quantity", type=Decimal, default=10)
parser.add_argument("--sell_quantity", type=Decimal, default=10)
parser.add_argument("--add_kraken", choices=["y", "n"], default="n")
args = parser.parse_args()


def print_buy_summary(
    _buy_quantity: Decimal, _total_buy_cost: Decimal, _pending_buy_quantity: Decimal
):
    """Function to print the BTC buy summary"""
    print()
    print(f"quantity to buy: {_buy_quantity}")

    print()

    _bought_quantity = _buy_quantity - _pending_buy_quantity
    print(f"quantity bought: {_bought_quantity}")

    if _pending_buy_quantity > 0:
        print(f"pending buy quantity: {_pending_buy_quantity}")

    print()

    print(f"total cost of buying: {_total_buy_cost}")

    _average_buy_price = _total_buy_cost / _bought_quantity
    print(f"average buying price: {_average_buy_price}")


def print_sell_summary(
    _sell_quantity: Decimal, _total_sell_cost: Decimal, _pending_sell_quantity: Decimal
):
    """Function to print the BTC sell summary"""
    print()
    print(f"quantity to sell: {_sell_quantity}")

    print()

    _sold_quantity = _sell_quantity - _pending_sell_quantity
    print(f"quantity sold: {_sold_quantity}")

    if _pending_sell_quantity > 0:
        print(f"pending sell quantity: {_pending_sell_quantity}")

    print()

    print(f"total cost of selling: {_total_sell_cost}")

    _average_sell_price = _total_sell_cost / _sold_quantity
    print(f"average selling price: {_average_sell_price}")


if __name__ == "__main__":

    buy_quantity = args.buy_quantity
    sell_quantity = args.sell_quantity
    add_kraken = args.add_kraken

    # ---------------------------------------------------
    # ===================Get Orderbook===================
    # ---------------------------------------------------

    aggregator = Aggregator()

    aggregator.get_orderbooks(add_kraken=add_kraken)

    # ---------------------------------------------
    # ===================Buy BTC===================
    # ---------------------------------------------

    (total_buy_cost, pending_buy_quantity) = aggregator.market_order(
        quantity=args.buy_quantity, is_buy=True
    )

    print_buy_summary(
        _buy_quantity=buy_quantity,
        _total_buy_cost=total_buy_cost,
        _pending_buy_quantity=pending_buy_quantity,
    )

    # ----------------------------------------------
    # ===================Sell BTC===================
    # ----------------------------------------------

    (total_sell_cost, pending_sell_quantity) = aggregator.market_order(
        quantity=args.sell_quantity, is_buy=False
    )

    print_sell_summary(
        _sell_quantity=sell_quantity,
        _total_sell_cost=total_sell_cost,
        _pending_sell_quantity=pending_sell_quantity,
    )
