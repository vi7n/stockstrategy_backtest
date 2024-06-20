"""
back test the buy and sell for simple ema crossover strategy
WORKS!
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set the end date to today and start date to 5 years before
end_date = datetime.now()
start_date = end_date - timedelta(days=5 * 365)

# Download historical data for NVDA stock
data = yf.download(
    "NVDA", start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d")
)

# Calculate the short and long Exponential Moving Averages (EMAs)
data["20_EMA"] = data["Close"].ewm(span=20, adjust=False).mean()
data["50_EMA"] = data["Close"].ewm(span=50, adjust=False).mean()

# Generate buy/sell signals
data["Signal"] = 0
data["Signal"][20:] = np.where(data["20_EMA"][20:] > data["50_EMA"][20:], 1, 0)
data["Position"] = data["Signal"].diff()

# Filter the buy and sell signals
buy_signals = data[data["Position"] == 1]
sell_signals = data[data["Position"] == -1]

# Calculate and print the performance
initial_balance = 10000
balance = initial_balance
shares = 0

for index, row in data.iterrows():
    if row["Position"] == 1:  # Buy signal
        shares = balance / row["Close"]
        balance = 0
        print(f"Buying on {index.date()} at {row['Close']:.2f}")
    elif row["Position"] == -1 and shares > 0:  # Sell signal
        balance = shares * row["Close"]
        shares = 0
        print(f"Selling on {index.date()} at {row['Close']:.2f}")

final_balance = balance + (shares * data.iloc[-1]["Close"])
print(f"Initial balance: {initial_balance:.2f}")
print(f"Final balance: {final_balance:.2f}")

# Plot the closing price, EMAs, and buy/sell signals
plt.figure(figsize=(14, 7))
plt.plot(data["Close"], label="Close Price", alpha=0.5)
plt.plot(data["20_EMA"], label="20-Day EMA", alpha=0.9)
plt.plot(data["50_EMA"], label="50-Day EMA", alpha=0.9)
plt.scatter(
    buy_signals.index,
    buy_signals["Close"],
    label="Buy Signal",
    marker="^",
    color="green",
    s=100,
)
plt.scatter(
    sell_signals.index,
    sell_signals["Close"],
    label="Sell Signal",
    marker="v",
    color="red",
    s=100,
)
plt.title("EMA Crossover Strategy Backtest")
plt.legend()
plt.show()
