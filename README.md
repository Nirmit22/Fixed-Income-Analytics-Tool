# Fixed Income Analytics Tool

A Python-based analytics engine to model and analyze straight (option-free) bonds, in alignment with **CFA Level II Fixed Income** curriculum.

---

## 🎯 Project Objective

This project demonstrates practical implementation of core fixed income concepts. It focuses exclusively on:

- **Straight bond pricing**
- **Yield curve construction**
- **Spread analysis**
- **Duration & convexity**
- **Credit risk estimation**

---

## 📦 Features

| Module                  | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `bond_pricing.py`       | Clean/dirty price, accrued interest, yield-to-maturity                     |
| `yield_curve.py`        | Bootstrapping spot rates, forward rates, and yield curve plotting          |
| `spreads.py`            | G-spread, I-spread, Z-spread calculations                                  |
| `duration_convexity.py` | Macaulay, Modified, Effective Duration and Convexity                       |
| `credit_risk.py`        | Expected loss = PD × LGD × EAD based on credit rating                     |

---

## 🧪 Demo Notebook

The file [`fixed_income_demo.ipynb`](./fixed_income_demo.ipynb) shows a complete walk-through:

- Price a 5-year bond with 5% coupon
- Bootstrap spot rates from zero-coupon bonds
- Calculate spreads over benchmark rates
- Estimate duration, convexity
- Model expected credit loss from rating

---

## ⚙️ How to Run

```bash
# Clone repo or extract files
cd fixed_income_analytics

# Install requirements (if any)
pip install numpy pandas matplotlib scipy

# Open the notebook
jupyter notebook fixed_income_demo.ipynb
```

---

## 🎓 CFA Curriculum Mapping

| Topic                         | CFA Level II Reading |
|------------------------------|----------------------|
| Bond Pricing                  | Reading 34           |
| Yield Curves                  | Reading 35           |
| Credit Spreads                | Reading 36           |
| Duration & Convexity          | Reading 34, 35       |
| Credit Risk & Expected Loss   | Reading 36           |

---

