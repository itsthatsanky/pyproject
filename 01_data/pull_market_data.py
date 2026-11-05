import json
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    root_dir = Path(__file__).resolve().parent.parent
    config_path = root_dir / "config.json"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    core_tickers_map = {
        k: v for k, v in config["tickers"].items() if k != "Benchmark"
    }
    core_tickers = list(core_tickers_map.values())  # ['ICICIBANK.NS', 'RELIANCE.NS', 'TCS.NS']
    benchmark_ticker = config["tickers"]["Benchmark"]  # '^NSEI'
    peer_tickers = config["context_peers"]  # 7 peers

    all_tickers = core_tickers + [benchmark_ticker] + peer_tickers
    start_date = "2021-10-31"
    end_date = config.get("price_cutoff_date", "2026-10-31")

    print(f"Downloading 5-year daily adjusted close prices ({start_date} to {end_date}) for {len(all_tickers)} tickers...")
    raw_df = yf.download(
        tickers=all_tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    # Handle MultiIndex columns cleanly so each ticker maps to a flat column of daily close prices
    if isinstance(raw_df.columns, pd.MultiIndex):
        if "Close" in raw_df.columns.get_level_values(0):
            prices = raw_df["Close"].copy()
        elif "Close" in raw_df.columns.get_level_values(1):
            prices = raw_df.xs("Close", axis=1, level=1).copy()
        else:
            prices = raw_df.iloc[:, :len(all_tickers)].copy()
            prices.columns = [col[-1] for col in prices.columns]
    else:
        prices = raw_df.copy()

    # Ensure deterministic column order
    available_cols = [t for t in all_tickers if t in prices.columns]
    prices = prices[available_cols]
    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    prices.index.name = "Date"

    # Forward-fill missing trading days and drop leading NaNs
    prices = prices.sort_index().ffill().dropna(how="any")

    raw_prices_path = root_dir / "01_data" / "raw" / "market_prices" / "daily_prices.csv"
    raw_prices_path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(raw_prices_path)
    print(f"Saved clean daily price table ({prices.shape[0]} trading days x {prices.shape[1]} tickers) to {raw_prices_path}")

    # Compute daily log returns
    log_returns = np.log(prices / prices.shift(1)).dropna()
    cleaned_dir = root_dir / "01_data" / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    log_returns_path = cleaned_dir / "daily_log_returns.csv"
    log_returns.to_csv(log_returns_path)
    print(f"Saved daily log returns ({log_returns.shape[0]} rows) to {log_returns_path}")

    # Compute 10-stock correlation matrix across the 3 core stocks and 7 Nifty peers
    ten_stocks = core_tickers + peer_tickers
    corr_matrix = log_returns[ten_stocks].corr()
    corr_csv_path = cleaned_dir / "correlation_matrix.csv"
    corr_matrix.to_csv(corr_csv_path)
    print(f"Saved 10-stock correlation matrix to {corr_csv_path}")

    # Render high-resolution correlation heatmap
    plt.figure(figsize=(11, 9), dpi=300)
    sns.set_theme(style="white")
    short_labels = [t.replace(".NS", "") for t in ten_stocks]
    ax = sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdYlBu_r",
        vmin=-0.2,
        vmax=1.0,
        xticklabels=short_labels,
        yticklabels=short_labels,
        linewidths=0.8,
        cbar_kws={"label": "5-Year Daily Log-Return Correlation"},
    )
    ax.set_title(
        "10-Stock Return Correlation Matrix: Core Portfolio (3) & Nifty 50 Context Peers (7)",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    plt.xticks(rotation=35, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    heatmap_path = cleaned_dir / "correlation_heatmap.png"
    plt.savefig(heatmap_path, dpi=300)
    plt.close()
    print(f"Saved correlation heatmap to {heatmap_path}")

    # Compute 5-year regression Betas (cov/var against ^NSEI), annualized volatility, and latest cutoff closing prices
    mkt_ret = log_returns[benchmark_ticker]
    mkt_var = float(np.var(mkt_ret, ddof=1))
    mkt_ann_vol = float(np.std(mkt_ret, ddof=1) * np.sqrt(252))
    mkt_ann_ret = float(np.mean(mkt_ret) * 252)

    blend_w = float(config.get("capm_blend_weight", 0.50))
    rf_dcf = float(config.get("rf_dcf_10y_gsec", 0.0685))
    erp = float(config.get("equity_risk_premium", 0.0600))
    cutoff_actual_date = prices.index[-1].strftime("%Y-%m-%d")

    market_betas = {}
    print("\n--- 5-Year Market Metrics Summary (Cutoff Date: " + cutoff_actual_date + ") ---")
    for name, ticker in core_tickers_map.items():
        stock_ret = log_returns[ticker]
        cov_im = float(np.cov(stock_ret, mkt_ret, ddof=1)[0, 1])
        raw_beta = cov_im / mkt_var
        blended_beta = blend_w * raw_beta + (1.0 - blend_w) * 1.0
        ann_vol = float(np.std(stock_ret, ddof=1) * np.sqrt(252))
        ann_ret = float(np.mean(stock_ret) * 252)
        corr_im = float(np.corrcoef(stock_ret, mkt_ret)[0, 1])
        r_squared = corr_im ** 2
        latest_close = float(prices[ticker].iloc[-1])

        ke_raw = rf_dcf + raw_beta * erp
        ke_blended = rf_dcf + blended_beta * erp

        market_betas[ticker] = {
            "name": name,
            "ticker": ticker,
            "beta": round(raw_beta, 4),
            "raw_beta": round(raw_beta, 4),
            "blended_beta": round(blended_beta, 4),
            "r_squared": round(r_squared, 4),
            "correlation_with_nifty": round(corr_im, 4),
            "annualized_volatility": round(ann_vol, 4),
            "annualized_log_return": round(ann_ret, 4),
            "latest_close": round(latest_close, 2),
            "cutoff_price": round(latest_close, 2),
            "cutoff_date": cutoff_actual_date,
            "capm_ke_raw": round(ke_raw, 4),
            "capm_ke_blended": round(ke_blended, 4),
            "benchmark_ticker": benchmark_ticker,
            "benchmark_annualized_volatility": round(mkt_ann_vol, 4),
            "benchmark_annualized_log_return": round(mkt_ann_ret, 4),
            "benchmark_latest_close": round(float(prices[benchmark_ticker].iloc[-1]), 2),
            "observations": int(len(stock_ret)),
        }
        print(
            f"{ticker:14s} | Latest Close: INR {latest_close:8.2f} | "
            f"5Y Beta: {raw_beta:.4f} (Blended: {blended_beta:.4f}) | "
            f"Ann. Vol: {ann_vol*100:.2f}% | Ann. Mean Log Ret: {ann_ret*100:.2f}%"
        )

    betas_path = cleaned_dir / "market_betas.json"
    with open(betas_path, "w", encoding="utf-8") as f:
        json.dump(market_betas, f, indent=2)
    print(f"Saved market betas and summary metrics to {betas_path}")


if __name__ == "__main__":
    main()
