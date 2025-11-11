"""
bond_pricing.py

Straight Bond Pricing Module
============================

This module provides functions to price straight (option-free) fixed-rate bonds.
It includes:
- Clean and dirty price calculation
- Yield to maturity (YTM)
- Accrued interest

Aligned with CFA Level II Fixed Income curriculum (Reading 34).

Author: Quantitative Financial Engineer
"""

import numpy as np

def bond_price(face_value, coupon_rate, periods, ytm, freq=2):
    """
    Calculate the price of a straight bond.

    Parameters:
    - face_value: Face value of the bond (e.g., 1000)
    - coupon_rate: Annual coupon rate (e.g., 0.05 for 5%)
    - periods: Total number of periods until maturity (e.g., 10 years * 2 = 20 semiannual)
    - ytm: Yield to maturity as a decimal (e.g., 0.06 for 6%)
    - freq: Coupon frequency (default is 2 for semi-annual)

    Returns:
    - price: Present value of bond (clean price)
    """
    coupon = face_value * coupon_rate / freq
    discount_factors = [(1 + ytm / freq) ** -(t + 1) for t in range(periods)]
    pv_coupons = sum([coupon * df for df in discount_factors])
    pv_face = face_value * discount_factors[-1]
    return pv_coupons + pv_face

def accrued_interest(face_value, coupon_rate, days_since_last, days_in_period, freq=2):
    """
    Calculate accrued interest using 30/360 day count.

    Parameters:
    - face_value: Face value of bond
    - coupon_rate: Annual coupon rate
    - days_since_last: Days since last coupon payment
    - days_in_period: Total days in the period (typically 180 for semi-annual)
    - freq: Frequency of coupon payments

    Returns:
    - accrued_interest: Interest earned but not yet paid
    """
    coupon = face_value * coupon_rate / freq
    return coupon * days_since_last / days_in_period

def dirty_price(clean_price, accrued_interest):
    """
    Calculate dirty price = clean price + accrued interest.
    """
    return clean_price + accrued_interest
