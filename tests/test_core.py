import unittest

from src.stocklab.core import backtest, moving_average_signal


class BacktestTests(unittest.TestCase):
    def test_signal_is_shifted_before_position_is_used(self):
        closes = [100, 101, 102, 103, 104, 105]
        signal = moving_average_signal(closes, fast=2, slow=3)
        result = backtest(closes, fast=2, slow=3, fee_bps=0)

        self.assertEqual(result["positions"][0], 0)
        self.assertEqual(result["positions"][1:], signal[:-1])

    def test_fees_reduce_strategy_return(self):
        closes = [100, 101, 102, 103, 104, 105, 104, 103, 106, 108]
        free = backtest(closes, fast=2, slow=3, fee_bps=0)
        paid = backtest(closes, fast=2, slow=3, fee_bps=25)

        self.assertLess(
            paid["metrics"]["total_return"],
            free["metrics"]["total_return"],
        )

    def test_benchmark_matches_price_change(self):
        closes = [100, 105, 110]
        result = backtest(closes, fast=1, slow=2, fee_bps=0)
        self.assertAlmostEqual(result["metrics"]["benchmark_return"], 0.10)

    def test_rejects_invalid_ma_order(self):
        with self.assertRaises(ValueError):
            backtest([100, 101, 102], fast=5, slow=5)


if __name__ == "__main__":
    unittest.main()
