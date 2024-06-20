from stra1 import simple_ema
from stra2 import simple_ema_stoploss
from stra3 import ichimoku_fixed_stoploss
from stra4 import ichimoku_strategy_traling_SL


# Import other strategy functions similarly
# from strategy1 import strategy1
# from strategy2 import strategy2
# from strategy3 import strategy3


def main(stock):
    # Run each strategy
    simp1_result = simple_ema(stock)
    simp2_result = simple_ema_stoploss(stock)
    ichimoku1_result = ichimoku_fixed_stoploss(stock)
    ichimoku2_result = ichimoku_strategy_traling_SL(stock)
    # strategy1_result = strategy1(stock)
    # strategy2_result = strategy2(stock)
    # strategy3_result = strategy3(stock)

    # Print results
    print(f"EMA crossover result for {stock}: ${simp1_result:.2f}")
    print(f"EMA crossover Fixed SL result for {stock}: ${simp2_result:.2f}")
    print(f"Ichimoku Strategy Fixed SL result for {stock}: ${ichimoku1_result:.2f}")
    print(f"Ichimoku Strategy Trailing SL result for {stock}: ${ichimoku2_result:.2f}")
    # print(f"Strategy 1 result for {stock}: ${strategy1_result:.2f}")
    # print(f"Strategy 2 result for {stock}: ${strategy2_result:.2f}")
    # print(f"Strategy 3 result for {stock}: ${strategy3_result:.2f}")


if __name__ == "__main__":
    stock = "TSM"
    main(stock)
