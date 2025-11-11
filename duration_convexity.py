"""
duration_convexity.py

Duration and Convexity Analysis
===============================

Includes:
- Macaulay duration
- Modified duration
- Effective duration (via shift in yield)
- Convexity (price curvature)
- Key rate duration (sensitivity to specific yield curve points)

Aligned with CFA Level II Fixed Income (Readings 34 and 35).

Author: Quantitative Financial Engineer
"""

import numpy as np

def macaulay_duration(face_value, coupon_rate, ytm, periods, freq=2):
    """
    Calculate Macaulay duration.

    Parameters:
    - face_value: Face value of the bond
    - coupon_rate: Annual coupon rate
    - ytm: Yield to maturity (annualized)
    - periods: Number of periods (e.g. years * freq)
    - freq: Coupon frequency (default: 2 for semiannual)

    Returns:
    - Macaulay duration (in years)
    """
    coupon = face_value * coupon_rate / freq
    duration = 0.0
    price = 0.0

    for t in range(1, periods + 1):
        time = t / freq
        df = (1 + ytm / freq) ** t
        cf = coupon if t < periods else (coupon + face_value)
        duration += time * cf / df
        price += cf / df

    return duration / price

def modified_duration(macaulay_dur, ytm, freq=2):
    """
    Compute modified duration from Macaulay duration.

    Parameters:
    - macaulay_dur: Macaulay duration
    - ytm: Yield to maturity
    - freq: Coupon frequency

    Returns:
    - Modified duration
    """
    return macaulay_dur / (1 + ytm / freq)

def effective_duration(bond_price_up, bond_price_down, bond_price, delta_y):
    """
    Estimate effective duration.

    Parameters:
    - bond_price_up: Price if yields go up by delta_y
    - bond_price_down: Price if yields go down by delta_y
    - bond_price: Current bond price
    - delta_y: Change in yield (as decimal, e.g., 0.01 for 100bps)

    Returns:
    - Effective duration
    """
    return (bond_price_down - bond_price_up) / (2 * bond_price * delta_y)

def convexity(face_value, coupon_rate, ytm, periods, freq=2):
    """
    Calculate bond convexity.

    Parameters:
    - face_value: Face value of the bond
    - coupon_rate: Annual coupon rate
    - ytm: Yield to maturity
    - periods: Number of periods (e.g. years * freq)
    - freq: Coupon frequency

    Returns:
    - Convexity measure
    """
    coupon = face_value * coupon_rate / freq
    conv = 0.0
    price = 0.0

    for t in range(1, periods + 1):
        time = t / freq
        df = (1 + ytm / freq) ** t
        cf = coupon if t < periods else (coupon + face_value)
        conv += cf * time * (time + 1 / freq) / df
        price += cf / df

    return conv / (price * (1 + ytm / freq) ** 2)

def bond_price_from_spot_curve(face_value, coupon_rate, maturity_years, spot_curve, freq=2):
    """
    Calculate bond price using a spot rate curve.
    
    Parameters:
    - face_value: Face value of the bond
    - coupon_rate: Annual coupon rate
    - maturity_years: Bond maturity in years
    - spot_curve: Dictionary mapping maturities (in years) to spot rates
    - freq: Coupon frequency (default: 2 for semiannual)
    
    Returns:
    - Bond price
    """
    coupon = face_value * coupon_rate / freq
    periods = int(maturity_years * freq)
    price = 0.0
    
    for t in range(1, periods + 1):
        time = t / freq
        # Interpolate spot rate for this maturity if not directly available
        spot_rate = _interpolate_spot_rate(spot_curve, time)
        df = (1 + spot_rate / freq) ** t
        
        # Cash flow: coupon for all periods, plus principal at maturity
        cf = coupon if t < periods else (coupon + face_value)
        price += cf / df
    
    return price

def _interpolate_spot_rate(spot_curve, target_maturity):
    """
    Interpolate spot rate for a given maturity using linear interpolation.
    
    Parameters:
    - spot_curve: Dictionary mapping maturities to spot rates
    - target_maturity: Target maturity in years
    
    Returns:
    - Interpolated spot rate
    """
    maturities = sorted(spot_curve.keys())
    
    # If exact match exists, return it
    if target_maturity in spot_curve:
        return spot_curve[target_maturity]
    
    # If target is beyond the longest maturity, use the longest rate (flat extrapolation)
    if target_maturity > maturities[-1]:
        return spot_curve[maturities[-1]]
    
    # If target is before the shortest maturity, use the shortest rate
    if target_maturity < maturities[0]:
        return spot_curve[maturities[0]]
    
    # Linear interpolation between two adjacent maturities
    for i in range(len(maturities) - 1):
        if maturities[i] <= target_maturity <= maturities[i + 1]:
            t1, t2 = maturities[i], maturities[i + 1]
            r1, r2 = spot_curve[t1], spot_curve[t2]
            # Linear interpolation
            weight = (target_maturity - t1) / (t2 - t1)
            return r1 + weight * (r2 - r1)
    
    return spot_curve[maturities[-1]]

def key_rate_duration(face_value, coupon_rate, maturity_years, spot_curve, 
                      key_rate_maturity, delta_y=0.0001, freq=2):
    """
    Calculate key rate duration for a specific maturity point on the yield curve.
    
    Key rate duration measures the sensitivity of a bond's price to a change in
    the spot rate at a specific maturity, holding all other rates constant.
    This is useful for understanding how bonds respond to non-parallel yield curve shifts.
    
    Parameters:
    - face_value: Face value of the bond
    - coupon_rate: Annual coupon rate
    - maturity_years: Bond maturity in years
    - spot_curve: Dictionary mapping maturities (in years) to spot rates (decimal)
    - key_rate_maturity: The specific maturity point to shock (in years)
    - delta_y: Yield shift size (default: 0.0001 = 1 basis point)
    - freq: Coupon frequency (default: 2 for semiannual)
    
    Returns:
    - Key rate duration for the specified maturity point
    
    Example:
    >>> spot_curve = {0.5: 0.03, 1: 0.035, 2: 0.04, 5: 0.045, 10: 0.05}
    >>> krd_2y = key_rate_duration(100, 0.04, 5, spot_curve, key_rate_maturity=2)
    >>> print(f"2-year key rate duration: {krd_2y:.4f}")
    """
    # Calculate base price with original spot curve
    base_price = bond_price_from_spot_curve(face_value, coupon_rate, 
                                            maturity_years, spot_curve, freq)
    
    # Create shifted spot curves (shift only the key rate maturity)
    spot_curve_up = spot_curve.copy()
    spot_curve_down = spot_curve.copy()
    
    # Shift the key rate up and down
    if key_rate_maturity in spot_curve_up:
        spot_curve_up[key_rate_maturity] += delta_y
        spot_curve_down[key_rate_maturity] -= delta_y
    else:
        # If the exact maturity doesn't exist, add it with interpolated value
        base_rate = _interpolate_spot_rate(spot_curve, key_rate_maturity)
        spot_curve_up[key_rate_maturity] = base_rate + delta_y
        spot_curve_down[key_rate_maturity] = base_rate - delta_y
    
    # Calculate prices with shifted curves
    price_up = bond_price_from_spot_curve(face_value, coupon_rate, 
                                         maturity_years, spot_curve_up, freq)
    price_down = bond_price_from_spot_curve(face_value, coupon_rate, 
                                           maturity_years, spot_curve_down, freq)
    
    # Calculate key rate duration using centered difference
    krd = (price_down - price_up) / (2 * base_price * delta_y)
    
    return krd

def calculate_all_key_rate_durations(face_value, coupon_rate, maturity_years, 
                                      spot_curve, key_rate_maturities=None, 
                                      delta_y=0.0001, freq=2):
    """
    Calculate key rate durations for multiple maturity points on the yield curve.
    
    Parameters:
    - face_value: Face value of the bond
    - coupon_rate: Annual coupon rate
    - maturity_years: Bond maturity in years
    - spot_curve: Dictionary mapping maturities (in years) to spot rates
    - key_rate_maturities: List of maturities to calculate KRD for 
                          (default: [0.5, 1, 2, 5, 10, 20, 30])
    - delta_y: Yield shift size (default: 0.0001 = 1 basis point)
    - freq: Coupon frequency (default: 2 for semiannual)
    
    Returns:
    - Dictionary mapping key rate maturities to their durations
    
    Example:
    >>> spot_curve = {0.5: 0.03, 1: 0.035, 2: 0.04, 5: 0.045, 10: 0.05}
    >>> krds = calculate_all_key_rate_durations(100, 0.04, 10, spot_curve)
    >>> for maturity, krd in sorted(krds.items()):
    ...     print(f"{maturity}Y KRD: {krd:.4f}")
    """
    # Default key rate maturities (standard buckets used in practice)
    if key_rate_maturities is None:
        key_rate_maturities = [0.5, 1, 2, 5, 10, 20, 30]
    
    # Only calculate KRD for maturities up to the bond's maturity
    relevant_maturities = [m for m in key_rate_maturities if m <= maturity_years]
    
    krds = {}
    for key_mat in relevant_maturities:
        krd = key_rate_duration(face_value, coupon_rate, maturity_years, 
                               spot_curve, key_mat, delta_y, freq)
        krds[key_mat] = krd
    
    return krds
