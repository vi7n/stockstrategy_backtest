"""
back test the buy and sell for simple ema crossover strategy
WORKS!
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


def simple_ema(stock):
    # Set the end date to today and start date to 5 years before
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5 * 365)

    # Download historical data for NVDA stock
    data = yf.download(
        stock, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d")
    )

    # Calculate the short and long Exponential Moving Averages (EMAs)
    data["20_EMA"] = data["Close"].ewm(span=20, adjust=False).mean()
    data["50_EMA"] = data["Close"].ewm(span=50, adjust=False).mean()

    # Generate buy/sell signals
    data["Signal"] = 0
    data["Signal"][20:] = np.where(data["20_EMA"][20:] > data["50_EMA"][20:], 1, 0)
    data["Position"] = data["Signal"].diff()

    # # Filter the buy and sell signals
    # buy_signals = data[data["Position"] == 1]
    # sell_signals = data[data["Position"] == -1]

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
    profit_loss = final_balance - initial_balance
    return profit_loss
