import math
from decimal import Decimal


PRICES = {
    (-math.inf, 0): Decimal('0'),
    (1, 5000): Decimal('0.247'),
    (5001, 10000): Decimal('0.247'),
    (10001, 30000): Decimal('0.246'),
    (30001, 50000): Decimal('0.245'),
    (50001, 100000): Decimal('0.242'),
    (100001, 1000000): Decimal('0.240'),
    (1000001, 2000000): Decimal('0.229'),
    (2000001, math.inf): Decimal('0.219'),
}


def get_price_for(amount):
    for (min_val, max_val), price in PRICES.items():
        if min_val <= amount <= max_val:
            return price


def calculate_price_for(amount, msg_length):
    price_per_msg = get_price_for(amount)
    return amount * msg_length * price_per_msg
