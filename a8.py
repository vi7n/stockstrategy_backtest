"""
back test the buy and sell for Ichimoku Cloud strategy with trailing stop loss

"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set the end date to today and start date to 5 years before
end_date = datetime.now()
start_date = end_date - timedelta(days=5 * 365)

# Download historical data for TSLA stock
data = yf.download(
    "TSLA", start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d")
)

# Calculate the Ichimoku Cloud components
high_9 = data["High"].rolling(window=9).max()
low_9 = data["Low"].rolling(window=9).min()
data["Tenkan_sen"] = (high_9 + low_9) / 2

high_26 = data["High"].rolling(window=26).max()
low_26 = data["Low"].rolling(window=26).min()
data["Kijun_sen"] = (high_26 + low_26) / 2

high_52 = data["High"].rolling(window=52).max()
low_52 = data["Low"].rolling(window=52).min()
data["Senkou_span_A"] = ((data["Tenkan_sen"] + data["Kijun_sen"]) / 2).shift(26)
data["Senkou_span_B"] = ((high_52 + low_52) / 2).shift(26)
data["Chikou_span"] = data["Close"].shift(-26)

# Generate buy/sell signals based on Golden Cross and Death Cross
data["Signal"] = 0
data["Signal"][26:] = np.where(data["Tenkan_sen"][26:] > data["Kijun_sen"][26:], 1, 0)
data["Position"] = data["Signal"].diff()

# Filter the buy and sell signals
buy_signals = data[data["Position"] == 1]
sell_signals = data[data["Position"] == -1]

# Initialize the trailing stop loss and balance
trailing_stop_loss = 0.85  # 15% trailing stop loss
initial_balance = 10000
balance = initial_balance
shares = 0
buy_price = 0
highest_price = 0

for index, row in data.iterrows():
    if row["Position"] == 1 and balance > 0:  # Buy signal
        shares = balance / row["Close"]
        buy_price = row["Close"]
        highest_price = row["Close"]
        balance = 0
        print(f"Buying on {index.date()} at {row['Close']:.2f}")
    elif shares > 0:
        highest_price = max(highest_price, row["Close"])
        if row["Close"] <= highest_price * trailing_stop_loss or row["Position"] == -1:
            balance = shares * row["Close"]
            shares = 0
            highest_price = 0  # Reset highest price
            buy_price = 0  # Reset buy price
            print(f"Selling on {index.date()} at {row['Close']:.2f}")

final_balance = balance + (shares * data.iloc[-1]["Close"])
print(f"Initial balance: {initial_balance:.2f}")
print(f"Final balance: {final_balance:.2f}")

# Plot the closing price, Ichimoku Cloud components, and buy/sell signals
plt.figure(figsize=(14, 7))
plt.plot(data["Close"], label="Close Price", alpha=0.5)
plt.plot(data["Tenkan_sen"], label="Tenkan-sen", alpha=0.9)
plt.plot(data["Kijun_sen"], label="Kijun-sen", alpha=0.9)
plt.plot(data["Senkou_span_A"], label="Senkou Span A", alpha=0.5)
plt.plot(data["Senkou_span_B"], label="Senkou Span B", alpha=0.5)
plt.fill_between(
    data.index,
    data["Senkou_span_A"],
    data["Senkou_span_B"],
    where=data["Senkou_span_A"] >= data["Senkou_span_B"],
    facecolor="lightgreen",
    interpolate=True,
    alpha=0.3,
)
plt.fill_between(
    data.index,
    data["Senkou_span_A"],
    data["Senkou_span_B"],
    where=data["Senkou_span_A"] < data["Senkou_span_B"],
    facecolor="lightcoral",
    interpolate=True,
    alpha=0.3,
)
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
plt.title("Ichimoku Cloud Strategy Backtest with Trailing Stop Loss")
plt.legend()
plt.show()
