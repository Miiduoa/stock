import argparse

from src.stocklab import backtest, load_closes


parser = argparse.ArgumentParser(description="Bias-aware moving-average backtest")
parser.add_argument("csv")
parser.add_argument("--fast", type=int, default=20)
parser.add_argument("--slow", type=int, default=60)
parser.add_argument("--fee-bps", type=float, default=10)
args = parser.parse_args()

result = backtest(
    load_closes(args.csv),
    fast=args.fast,
    slow=args.slow,
    fee_bps=args.fee_bps,
)

for key, value in result["metrics"].items():
    print(f"{key}: {value:.6f}")
