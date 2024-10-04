"""Main Module"""

from decimal import Decimal
import argparse

from aggregator import Aggregator

parser = argparse.ArgumentParser()
parser.add_argument("--buy_quantity", type=Decimal, default=10)
parser.add_argument("--sell_quantity", type=Decimal, default=10)
parser.add_argument("--add_kraken", choices=["y", "n"], default="n")
args = parser.parse_args()

if __name__ == "__main__":

    buy_quantity = args.buy_quantity
    sell_quantity = args.sell_quantity

    # ---------------------------------------------------
    # ===================Get Orderbook===================
    # ---------------------------------------------------

    aggregator = Aggregator()

    aggregator.get_orderbooks(add_kraken=args.add_kraken)

    # ---------------------------------------------
    # ===================Buy BTC===================
    # ---------------------------------------------

    print(f"quantity to buy: {buy_quantity}")

    (total_buy_cost, pending_buy_quantity) = aggregator.market_order(
        quantity=args.buy_quantity, is_buy=True
    )

    print()

    bought_quantity = buy_quantity - pending_buy_quantity
    print(f"quantity bought: {bought_quantity}")

    if pending_buy_quantity > 0:
        print(f"pending buy quantity: {pending_buy_quantity}")

    print()

    print(f"total cost of buying: {total_buy_cost}")

    average_buy_price = total_buy_cost / bought_quantity
    print(f"average buying price: {average_buy_price}")

    # ----------------------------------------------
    # ===================Sell BTC===================
    # ----------------------------------------------

    print()

    print(f"quantity to sell: {sell_quantity}")

    (total_sell_cost, pending_sell_quantity) = aggregator.market_order(
        quantity=args.sell_quantity, is_buy=False
    )

    print()

    sold_quantity = sell_quantity - pending_sell_quantity
    print(f"quantity sold: {sold_quantity}")

    if pending_sell_quantity > 0:
        print(f"pending sell quantity: {pending_sell_quantity}")

    print()

    print(f"total cost of selling: {total_sell_cost}")

    average_sell_price = total_sell_cost / sold_quantity
    print(f"average selling price: {average_sell_price}")
