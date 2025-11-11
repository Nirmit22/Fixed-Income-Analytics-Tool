"""
yield_curve.py

Yield Curve Construction Module
===============================

This module includes functionality to:
- Bootstrap zero-coupon (spot) rates from a series of bonds
- Calculate forward rates
- Plot yield curves

CFA Level II-aligned (Reading 35): Understanding the term structure of interest rates.

Author: Quantitative Financial Engineer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def bootstrap_spot_rates(bond_data, freq=2):
    """
    Bootstraps spot rates from coupon bond prices.

    Parameters:
    - bond_data: List of dicts with keys: 'price', 'coupon_rate', 'maturity'
    - freq: Compounding frequency (default: 2 for semi-annual)

    Returns:
    - spot_rates: Dictionary of {maturity: spot_rate}
    """
    spot_rates = {}
    for bond in bond_data:
        price = bond['price']
        coupon_rate = bond['coupon_rate']
        maturity = bond['maturity']
        periods = int(maturity * freq)
        coupon = coupon_rate / freq
        pv = 0.0

        for t in range(1, periods):
            if t / freq in spot_rates:
                pv += coupon / (1 + spot_rates[t / freq] / freq) ** t

        remaining = price - pv
        rate = (coupon + 1) / remaining
        spot_rate = (rate ** (1 / periods) - 1) * freq
        spot_rates[maturity] = spot_rate

    return spot_rates

def forward_rate(r1, r2, t1, t2):
    """
    Compute 1-period forward rate between t1 and t2 given spot rates r1 and r2.

    Parameters:
    - r1: spot rate for t1
    - r2: spot rate for t2
    - t1: shorter maturity
    - t2: longer maturity

    Returns:
    - forward rate f(t1, t2)
    """
    return ((1 + r2) ** t2 / (1 + r1) ** t1) ** (1 / (t2 - t1)) - 1

def plot_yield_curve(spot_rates):
    """
    Plot the spot rate yield curve.

    Parameters:
    - spot_rates: Dictionary of {maturity: spot_rate}
    """
    maturities = sorted(spot_rates.keys())
    rates = [spot_rates[m] for m in maturities]

    plt.figure()
    plt.plot(maturities, rates, marker='o')
    plt.title('Spot Rate Yield Curve')
    plt.xlabel('Maturity (Years)')
    plt.ylabel('Spot Rate')
    plt.grid(True)
    plt.show()
