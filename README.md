# stock｜Walk-forward Backtest Lab

這不是選股神器，也不預測「明天會不會漲」。

我想處理的是另一個更基本的問題：**一個策略回測，到底有沒有偷看到未來？**

這個 repo 用很少的依賴做一套可檢查的回測流程：訊號延後一個交易日才生效、換倉會扣成本、策略會跟 buy-and-hold 比較，參數選擇則用 walk-forward，而不是拿整段歷史資料挑到最好看的組合。

## 目前包含

- SMA crossover 訊號
- position shift，避免同日收盤訊號直接成交的 look-ahead bias
- transaction cost / turnover
- buy-and-hold benchmark
- total return、annualized return / volatility、Sharpe、max drawdown
- walk-forward parameter selection
- deterministic synthetic demo
- unit tests + GitHub Actions

## 快速執行

```bash
python -m unittest discover -s tests -v
python demo.py
```

也可以帶自己的日線 CSV：

```bash
python cli.py prices.csv --fast 20 --slow 60 --fee-bps 10
```

CSV 只需要：

```csv
date,close
2026-01-02,100.0
2026-01-05,101.2
```

## 回測假設

訊號在第 t 天收盤後才知道，因此第 t+1 天才持有新部位。這個簡化模型使用 close-to-close return，適合拿來示範偏誤控制與策略比較，不等於實際券商成交模擬。

Walk-forward 每個 fold 只用前面的 training window 選參數，再把選出的參數套到下一段 test window。沒有用 test 區間反過來挑參數。

## 限制

- 目前只有 long / cash，沒有放空
- 沒有處理滑價、稅、股利、除權息與流動性
- annualized metrics 對短樣本很敏感
- 範例資料是合成資料，不代表任何真實標的績效
- 沒有宣稱策略具未來獲利能力

我把這些限制留在 README，是因為一個「看起來很賺」但驗證方式有問題的回測，價值通常比一個普通但誠實的 baseline 更低。
