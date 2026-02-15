"""
spreads.py

Credit Spread Analysis Module
=============================

Includes:
- G-spread (spread over government yield)
- I-spread (spread over swap curve)
- Z-spread (zero-volatility spread)

"""

import numpy as np
from scipy.optimize import minimize_scalar

def g_spread(bond_ytm, gov_ytm):
    """
    Calculate G-spread.

    Parameters:
    - bond_ytm: Yield to maturity of the corporate bond
    - gov_ytm: Yield to maturity of a benchmark government bond of same maturity

    Returns:
    - G-spread in basis points (bps)
    """
    return (bond_ytm - gov_ytm) * 10000

def i_spread(bond_ytm, swap_ytm):
    """
    Calculate I-spread.

    Parameters:
    - bond_ytm: Corporate bond yield
    - swap_ytm: Interpolated swap curve yield of same maturity

    Returns:
    - I-spread in basis points (bps)
    """
    return (bond_ytm - swap_ytm) * 10000

def z_spread(bond_price, face_value, coupon_rate, spot_rates, freq=2):
    """
    Estimate Z-spread (zero-volatility spread).

    Parameters:
    - bond_price: Clean price of the bond
    - face_value: Face value of the bond
    - coupon_rate: Annual coupon rate
    - spot_rates: Dictionary of {maturity: spot_rate}
    - freq: Frequency of coupon payments (default=2)

    Returns:
    - z_spread in basis points (bps)
    """
    periods = int(max(spot_rates.keys()) * freq)
    coupon = face_value * coupon_rate / freq

    def present_value(z):
        total_pv = 0
        for t in range(1, periods + 1):
            time = t / freq
            r = spot_rates.get(time, list(spot_rates.values())[-1])
            df = (1 + (r + z) / freq) ** -t
            if t < periods:
                total_pv += coupon * df
            else:
                total_pv += (coupon + face_value) * df
        return abs(total_pv - bond_price)

    res = minimize_scalar(present_value, bounds=(0, 0.1), method='bounded')
    return res.x * 10000  # return in basis points
