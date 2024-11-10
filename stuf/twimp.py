import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Define the stock symbols and the date range
stock_1 = "AAPL"  # Stock 1 (e.g., Apple)
stock_2 = "MSFT"  # Stock 2 (e.g., Microsoft)
start_date = "2020-01-01"
end_date = datetime.today().strftime("%Y-%m-%d")

# Download historical data for both stocks
data_1 = yf.download(stock_1, start=start_date, end=end_date)["Adj Close"]
data_2 = yf.download(stock_2, start=start_date, end=end_date)["Adj Close"]

# Merge the two dataframes on the date index
data = pd.DataFrame({"Stock_1": data_1, "Stock_2": data_2})
data = data.dropna()

# Calculate the spread (difference between the two stocks)
spread = data["Stock_1"] - data["Stock_2"]

# Plot the spread to visualize mean reversion
plt.figure(figsize=(12, 6))
plt.plot(data.index, spread, label="Spread (Stock_1 - Stock_2)", color="blue")
plt.axhline(spread.mean(), color="red", linestyle="--", label="Mean")
plt.title(f"Spread Between {stock_1} and {stock_2}")
plt.xlabel("Date")
plt.ylabel("Price Difference")
plt.legend()
plt.show()

# Calculate the z-score of the spread (for mean reversion)
z_score = (spread - spread.mean()) / spread.std()

# Plot the z-score
plt.figure(figsize=(12, 6))
plt.plot(data.index, z_score, label="Z-Score of the Spread", color="green")
plt.axhline(0, color="red", linestyle="--", label="Zero Line")
plt.title(f"Z-Score of the Spread Between {stock_1} and {stock_2}")
plt.xlabel("Date")
plt.ylabel("Z-Score")
plt.legend()
plt.show()

# Define entry and exit thresholds for trading
entry_threshold = 2  # Enter trade when the z-score exceeds 2 or -2
exit_threshold = 0  # Exit trade when the z-score returns to 0

# Create a column to store positions: +1 for long on Stock_1 and short on Stock_2, -1 for short on Stock_1 and long on Stock_2
data["Position"] = np.nan

# Entry logic: go long when z-score is below -2, short when above +2
data.loc[z_score < -entry_threshold, "Position"] = 1  # Long Stock_1, Short Stock_2
data.loc[z_score > entry_threshold, "Position"] = -1  # Short Stock_1, Long Stock_2

# Exit logic: close positions when z-score is near zero
data["Position"].ffill(inplace=True)  # Forward fill positions

# Filter positions when the z-score crosses the exit threshold
data.loc[z_score > -exit_threshold, "Position"] = 0
data.loc[z_score < exit_threshold, "Position"] = 0

# Calculate daily returns for each stock and portfolio
data["Stock_1_Return"] = data["Stock_1"].pct_change()
data["Stock_2_Return"] = data["Stock_2"].pct_change()
data["Portfolio_Return"] = data["Position"].shift(1) * (
    data["Stock_1_Return"] - data["Stock_2_Return"]
)

# Plot the cumulative returns of the strategy
data["Cumulative_Portfolio_Return"] = (1 + data["Portfolio_Return"]).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(
    data.index,
    data["Cumulative_Portfolio_Return"],
    label="Cumulative Strategy Return",
    color="purple",
)
plt.title(f"Cumulative Return of Pair Trading Strategy ({stock_1} vs {stock_2})")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.show()

# Display summary statistics for the strategy
print(data[["Stock_1_Return", "Stock_2_Return", "Portfolio_Return"]].mean())
print(data["Cumulative_Portfolio_Return"].tail(1))
