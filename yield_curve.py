"""
yield_curve.py

Yield Curve Construction Module
===============================

This module includes functionality to:
- Bootstrap zero-coupon (spot) rates from a series of bonds, using linear
  interpolation for coupon dates that fall between solved maturities
- Calculate forward rates
- Plot yield curves

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq


def _interpolate(curve, t):
    """
    Linearly interpolate a zero rate at time t from {maturity: rate}.
    Rates are held flat beyond the shortest and longest maturities.
    """
    maturities = sorted(curve)
    return float(np.interp(t, maturities, [curve[m] for m in maturities]))


def bootstrap_spot_rates(bond_data, freq=2, face=100.0):
    """
    Bootstraps spot (zero) rates from bond prices, shortest maturity first.

    For each bond, earlier cash flows are discounted at the zero rates already
    solved. Coupon dates between the last solved maturity and the bond's own
    maturity get a rate linearly interpolated between the last solved rate and
    the unknown rate at the bond's maturity, so the unknown appears in several
    discount factors. It is solved with Brent's root-finder, which raises an
    error rather than returning a misleading value if no solution exists.

    Parameters:
    - bond_data: List of dicts with keys: 'price', 'coupon_rate', 'maturity'
                 (price quoted per `face`, e.g. 99.5 per 100)
    - freq: Coupon and compounding frequency (default: 2 for semi-annual)
    - face: Face value the prices are quoted against (default: 100)

    Returns:
    - spot_rates: Dictionary of {maturity: spot_rate}
    """
    spot_rates = {}
    for bond in sorted(bond_data, key=lambda b: b['maturity']):
        price = bond['price']
        maturity = bond['maturity']
        periods = int(round(maturity * freq))
        coupon = face * bond['coupon_rate'] / freq

        def pricing_error(spot_at_maturity):
            # Candidate curve including the new node; dates in between are
            # interpolated, so they depend on the unknown rate.
            trial_curve = {**spot_rates, maturity: spot_at_maturity}
            pv = 0.0
            for t in range(1, periods + 1):
                cash_flow = coupon + (face if t == periods else 0.0)
                rate = _interpolate(trial_curve, t / freq)
                pv += cash_flow / (1 + rate / freq) ** t
            return pv - price

        spot_rates[maturity] = brentq(pricing_error, -0.05, 0.50)

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
