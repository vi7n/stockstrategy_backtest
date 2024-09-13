import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the ticker and period
ticker = "SMCI"
period = "5d"
interval = "1m"

# Fetch data from Yahoo Finance
data = yf.download(ticker, period=period, interval=interval)

# Define a sharp change threshold (e.g., 1% change within 5 minutes)
threshold = 0.01
window = 5

# Calculate percentage change over the specified window
data["Pct_Change"] = data["Close"].pct_change(periods=window)

# Initialize variables
initial_funds = 10000
cash = initial_funds
positions = []
actions = []
current_position = None

# Loop through data to apply the trading strategy
for i in range(window, len(data)):
    # Check for a sharp price increase
    if current_position is None:
        if data["Pct_Change"].iloc[i] >= threshold:
            # Buy call option
            buy_price = data["Close"].iloc[i]
            actions.append(("buy_call", data.index[i], buy_price))
            current_position = ("call", buy_price)

    # Check for a sharp price decrease to sell call option
    if current_position is not None and current_position[0] == "call":
        if data["Pct_Change"].iloc[i] <= -threshold:
            # Sell call option
            sell_price = data["Close"].iloc[i]
            profit = sell_price - current_position[1]
            cash += profit
            actions.append(("sell_call", data.index[i], sell_price))
            positions.append(profit)
            current_position = None

    # Check for a sharp price decrease
    if current_position is None:
        if data["Pct_Change"].iloc[i] <= -threshold:
            # Buy put option
            buy_price = data["Close"].iloc[i]
            actions.append(("buy_put", data.index[i], buy_price))
            current_position = ("put", buy_price)

    # Check for a sharp price increase to sell put option
    if current_position is not None and current_position[0] == "put":
        if data["Pct_Change"].iloc[i] >= threshold:
            # Sell put option
            sell_price = data["Close"].iloc[i]
            profit = current_position[1] - sell_price
            cash += profit
            actions.append(("sell_put", data.index[i], sell_price))
            positions.append(profit)
            current_position = None

# Calculate final profit/loss
total_profit_loss = sum(positions)
final_amount = cash

# Plotting the results
plt.figure(figsize=(14, 7))
plt.plot(data["Close"], label="SMCI Close Price", alpha=0.5)
for action in actions:
    if action[0] == "buy_call":
        plt.plot(action[1], action[2], "^", color="g", markersize=10, label="Buy Call")
    elif action[0] == "sell_call":
        plt.plot(action[1], action[2], "v", color="r", markersize=10, label="Sell Call")
    elif action[0] == "buy_put":
        plt.plot(action[1], action[2], "^", color="b", markersize=10, label="Buy Put")
    elif action[0] == "sell_put":
        plt.plot(action[1], action[2], "v", color="m", markersize=10, label="Sell Put")

plt.title(f"SMCI Options Trading Strategy - Final P/L: ${total_profit_loss:.2f}")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()

print(f"Final Profit/Loss: ${total_profit_loss:.2f}")
print(f"Final Amount: ${final_amount:.2f}")
