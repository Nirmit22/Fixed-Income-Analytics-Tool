"""
credit_risk.py

Credit Risk Estimation
======================

Includes basic credit risk analysis:
- Expected Loss (EL) = PD × LGD × EAD
- Support for rating-based inputs (using mapping)

Aligned with CFA Level II Fixed Income (Reading 36).

Author: Quantitative Financial Engineer
"""

# Example mapping from rating to probability of default (PD)
rating_pd_map = {
    'AAA': 0.0001,
    'AA':  0.0002,
    'A':   0.0005,
    'BBB': 0.002,
    'BB':  0.01,
    'B':   0.05,
    'CCC': 0.2
}

def expected_loss(pd, lgd, ead):
    """
    Compute expected credit loss.

    Parameters:
    - pd: Probability of default (as decimal)
    - lgd: Loss given default (percentage loss, as decimal)
    - ead: Exposure at default (monetary amount)

    Returns:
    - Expected loss (same units as EAD)
    """
    return pd * lgd * ead

def get_pd_from_rating(rating):
    """
    Get probability of default from credit rating.

    Parameters:
    - rating: Credit rating as string (e.g. 'BBB')

    Returns:
    - PD as decimal
    """
    return rating_pd_map.get(rating.upper(), None)

def credit_risk_analysis(rating, lgd, ead):
    """
    Compute expected loss using credit rating.

    Parameters:
    - rating: Credit rating (e.g., 'BB')
    - lgd: Loss given default (e.g., 0.6 for 60%)
    - ead: Exposure at default (e.g., bond face value)

    Returns:
    - Tuple (pd, expected_loss)
    """
    pd = get_pd_from_rating(rating)
    if pd is None:
        raise ValueError("Unknown rating. Accepted: " + ", ".join(rating_pd_map.keys()))
    el = expected_loss(pd, lgd, ead)
    return pd, el
