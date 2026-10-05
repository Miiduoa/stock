from .core import backtest, pct_returns


DEFAULT_CANDIDATES = ((5, 20), (10, 30), (20, 60))


def choose_parameters(train_closes, candidates=DEFAULT_CANDIDATES, fee_bps=10):
    ranked = []

    for fast, slow in candidates:
        if len(train_closes) < slow + 2:
            continue

        result = backtest(train_closes, fast=fast, slow=slow, fee_bps=fee_bps)
        ranked.append((result["metrics"]["sharpe"], fast, slow))

    if not ranked:
        raise ValueError("training window is too short for the candidate set")

    ranked.sort(reverse=True)
    _, fast, slow = ranked[0]
    return fast, slow


def walk_forward(
    closes,
    train_size=126,
    test_size=21,
    candidates=DEFAULT_CANDIDATES,
    fee_bps=10,
):
    if train_size <= 0 or test_size <= 0:
        raise ValueError("train_size and test_size must be positive")

    folds = []
    start = train_size

    while start < len(closes) - 1:
        end = min(start + test_size, len(closes))
        train = closes[start - train_size:start]
        fast, slow = choose_parameters(train, candidates, fee_bps)

        combined = closes[start - train_size:end]
        result = backtest(combined, fast=fast, slow=slow, fee_bps=fee_bps)

        test_returns = result["strategy_returns"][train_size:]
        benchmark_returns = pct_returns(combined)[train_size:]

        strategy_equity = 1.0
        benchmark_equity = 1.0

        for value in test_returns:
            strategy_equity *= 1 + value
        for value in benchmark_returns:
            benchmark_equity *= 1 + value

        folds.append({
            "start_index": start,
            "end_index": end - 1,
            "fast": fast,
            "slow": slow,
            "strategy_return": strategy_equity - 1,
            "benchmark_return": benchmark_equity - 1,
        })

        start = end

    return folds
