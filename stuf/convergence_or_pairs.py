import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the ticker symbols
smci_symbol = "SMCI"
nvda_symbol = "NVDA"

# Download historical data for SMCI and NVDA (excluding after-hours)
smci_data = yf.download(
    smci_symbol, start="2024-01-17", end="2024-07-17", prepost=False
)["Adj Close"]
nvda_data = yf.download(
    nvda_symbol, start="2024-01-17", end="2024-07-17", prepost=False
)["Adj Close"]

# Calculate the spread between SMCI and NVDA
spread = smci_data - nvda_data
# Convert values to percentage scale
smci_pct = (smci_data / smci_data.iloc[0] - 1) * 100
nvda_pct = (nvda_data / nvda_data.iloc[0] - 1) * 100

# Initialize positions
initial_investment = 10000
smci_position = 0
nvda_position = 0
cash = initial_investment


for i in range(len(spread)):
    if spread.iloc[i] < 0:
        # Go long on SMCI and short on NVDA
        smci_position += cash // smci_data.iloc[i]
        nvda_position -= cash // nvda_data.iloc[i]
        cash = initial_investment - (
            smci_position * smci_data.iloc[i] + nvda_position * nvda_data.iloc[i]
        )
    elif spread.iloc[i] > 0:
        # Go long on NVDA and short on SMCI
        nvda_position += cash // nvda_data.iloc[i]
        smci_position -= cash // smci_data.iloc[i]
        cash = initial_investment - (
            smci_position * smci_data.iloc[i] + nvda_position * nvda_data.iloc[i]
        )

# Calculates final portfolio value
final_value = (
    cash + smci_position * smci_data.iloc[-1] + nvda_position * nvda_data.iloc[-1]
)

# Plot stock prices
plt.figure(figsize=(10, 6))
plt.plot(smci_pct, label="SMCI")
plt.plot(nvda_pct, label="NVDA")
plt.title("SMCI vs. NVDA Stock Prices (Percentage Scale)")
plt.xlabel("Date")
plt.ylabel("Percentage Change")
plt.legend()
plt.show()

# Print final profit/loss
profit_loss = final_value - initial_investment
print(f"Final Portfolio Value: ${final_value:.2f}")
print(f"Profit/Loss: ${profit_loss:.2f}")
