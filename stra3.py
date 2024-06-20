# IC with fixed stop loss

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


def ichimoku_fixed_stoploss(stock):

    # Set the end date to today and start date to 5 years before
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5 * 365)

    # Download historical data for TSLA stock
    data = yf.download(
        stock, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d")
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
    data["Signal"][26:] = np.where(
        data["Tenkan_sen"][26:] > data["Kijun_sen"][26:], 1, 0
    )
    data["Position"] = data["Signal"].diff()

    # # Filter the buy and sell signals
    # buy_signals = data[data["Position"] == 1]
    # sell_signals = data[data["Position"] == -1]

    # Initialize the stop loss and balance
    stop_loss = 0.85  # 15% stop loss
    initial_balance = 10000
    balance = initial_balance
    shares = 0
    buy_price = 0

    for index, row in data.iterrows():
        if row["Position"] == 1 and balance > 0:  # Buy signal
            shares = balance / row["Close"]
            buy_price = row["Close"]
            balance = 0
            print(f"Buying on {index.date()} at {row['Close']:.2f}")
        elif shares > 0 and (
            row["Close"] <= buy_price * stop_loss or row["Position"] == -1
        ):  # Stop loss or sell signal
            balance = shares * row["Close"]
            shares = 0
            buy_price = 0  # Reset buy price
            print(f"Selling on {index.date()} at {row['Close']:.2f}")

    final_balance = balance + (shares * data.iloc[-1]["Close"])
    profit_loss = final_balance - initial_balance
    return profit_loss
