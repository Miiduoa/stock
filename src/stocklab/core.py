from math import sqrt
from statistics import fmean, pstdev


def sma(values, window):
    if window <= 0:
        raise ValueError("window must be positive")

    result = [None] * len(values)
    running = 0.0

    for index, value in enumerate(values):
        running += value
        if index >= window:
            running -= values[index - window]
        if index >= window - 1:
            result[index] = running / window

    return result


def moving_average_signal(closes, fast=20, slow=60):
    if fast >= slow:
        raise ValueError("fast must be smaller than slow")

    fast_ma = sma(closes, fast)
    slow_ma = sma(closes, slow)

    return [
        1 if a is not None and b is not None and a > b else 0
        for a, b in zip(fast_ma, slow_ma)
    ]


def pct_returns(closes):
    returns = [0.0]
    for index in range(1, len(closes)):
        returns.append(closes[index] / closes[index - 1] - 1)
    return returns


def max_drawdown(equity):
    peak = equity[0]
    worst = 0.0

    for value in equity:
        peak = max(peak, value)
        worst = min(worst, value / peak - 1)

    return worst


def backtest(closes, fast=20, slow=60, fee_bps=10):
    if len(closes) < 2:
        raise ValueError("need at least two prices")

    signal = moving_average_signal(closes, fast, slow)

    # Signal based on close[t] can only affect the next day's position.
    positions = [0] + signal[:-1]
    market_returns = pct_returns(closes)
    fee = fee_bps / 10_000

    strategy_returns = []
    equity = [1.0]
    benchmark = [1.0]
    previous_position = 0

    for position, market_return in zip(positions, market_returns):
        turnover = abs(position - previous_position)
        strategy_return = position * market_return - turnover * fee

        strategy_returns.append(strategy_return)
        equity.append(equity[-1] * (1 + strategy_return))
        benchmark.append(benchmark[-1] * (1 + market_return))
        previous_position = position

    realized = strategy_returns[1:]
    volatility = pstdev(realized) * sqrt(252) if len(realized) > 1 else 0.0
    annualized_return = equity[-1] ** (252 / max(len(closes) - 1, 1)) - 1

    if len(realized) > 1 and pstdev(realized) > 0:
        sharpe = fmean(realized) / pstdev(realized) * sqrt(252)
    else:
        sharpe = 0.0

    return {
        "positions": positions,
        "strategy_returns": strategy_returns,
        "equity": equity,
        "benchmark": benchmark,
        "metrics": {
            "total_return": equity[-1] - 1,
            "benchmark_return": benchmark[-1] - 1,
            "annualized_return": annualized_return,
            "annualized_volatility": volatility,
            "sharpe": sharpe,
            "max_drawdown": max_drawdown(equity),
        },
    }
