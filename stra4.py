# IC with trailing stop loss

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


def ichimoku_strategy_traling_SL(stock):
    # Set the end date to today and start date to 5 years before
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5 * 365)

    # Download historical data for the given stock
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
        elif shares > 0:
            highest_price = max(highest_price, row["Close"])
            if (
                row["Close"] <= highest_price * trailing_stop_loss
                or row["Position"] == -1
            ):
                balance = shares * row["Close"]
                shares = 0
                highest_price = 0  # Reset highest price
                buy_price = 0  # Reset buy price

    final_balance = balance + (shares * data.iloc[-1]["Close"])
    profit_loss = final_balance - initial_balance
    return profit_loss
