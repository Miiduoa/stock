import random

from src.stocklab import backtest, walk_forward


def synthetic_prices(days=320, seed=42):
    rng = random.Random(seed)
    prices = [100.0]

    for day in range(1, days):
        regime = 0.0008 if day < 110 or day >= 230 else -0.00025
        shock = rng.gauss(0, 0.011)
        prices.append(prices[-1] * (1 + regime + shock))

    return prices


prices = synthetic_prices()
result = backtest(prices, fast=10, slow=30, fee_bps=10)

print("Single backtest")
for key, value in result["metrics"].items():
    print(f"{key:24s} {value: .4f}")

print("\nWalk-forward folds")
for fold in walk_forward(prices, train_size=126, test_size=21, fee_bps=10):
    print(fold)
