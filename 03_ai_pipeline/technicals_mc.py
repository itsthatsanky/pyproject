import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def main():
    root_dir = Path(__file__).resolve().parent.parent
    config_path = root_dir / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    core_tickers_map = {
        k: v for k, v in config["tickers"].items() if k != "Benchmark"
    }
    core_tickers = list(core_tickers_map.values())

    prices_path = root_dir / "01_data" / "raw" / "market_prices" / "daily_prices.csv"
    log_ret_path = root_dir / "01_data" / "cleaned" / "daily_log_returns.csv"
    cleaned_dir = root_dir / "01_data" / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    prices = pd.read_csv(prices_path, index_col="Date", parse_dates=True)
    log_returns = pd.read_csv(log_ret_path, index_col="Date", parse_dates=True)

    tech_frames = []
    summary_data = {}

    # Set random seed for reproducibility across the Monte Carlo simulation
    np.random.seed(42)
    n_days = 252
    n_paths = 1000
    dt = 1.0 / 252.0

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.8), dpi=300)
    colors = {
        "ICICIBANK.NS": "#1f4e78",
        "RELIANCE.NS": "#2e75b6",
        "TCS.NS": "#008080",
    }

    print("\n--- Technical Indicators & 1-Year GBM Monte Carlo Summary ---")
    for idx, (name, ticker) in enumerate(core_tickers_map.items()):
        s = prices[ticker].dropna()
        r = log_returns[ticker].dropna()

        dma_50 = s.rolling(window=50).mean()
        dma_200 = s.rolling(window=200).mean()
        rsi_14 = compute_rsi(s, period=14)

        ema_12 = s.ewm(span=12, adjust=False).mean()
        ema_26 = s.ewm(span=26, adjust=False).mean()
        macd_line = ema_12 - ema_26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        macd_hist = macd_line - signal_line

        df_tech = pd.DataFrame({
            "Date": s.index,
            "Ticker": ticker,
            "Name": name,
            "Close": s.values,
            "DMA_50": dma_50.values,
            "DMA_200": dma_200.values,
            "RSI_14": rsi_14.values,
            "MACD": macd_line.values,
            "MACD_Signal": signal_line.values,
            "MACD_Hist": macd_hist.values,
        }).tail(252)
        tech_frames.append(df_tech)

        latest_close = float(s.iloc[-1])
        latest_dma50 = float(dma_50.iloc[-1])
        latest_dma200 = float(dma_200.iloc[-1])
        latest_rsi = float(rsi_14.iloc[-1])
        latest_macd = float(macd_line.iloc[-1])
        latest_signal = float(signal_line.iloc[-1])
        latest_hist = float(macd_hist.iloc[-1])

        if latest_rsi >= 70:
            rsi_regime = "Overbought (>=70)"
        elif latest_rsi <= 30:
            rsi_regime = "Oversold (<=30)"
        elif latest_rsi >= 55:
            rsi_regime = "Bullish Momentum (55-70)"
        elif latest_rsi <= 45:
            rsi_regime = "Bearish/Weak Momentum (30-45)"
        else:
            rsi_regime = "Neutral (45-55)"

        macd_regime = "Bullish Crossover (MACD > Signal)" if latest_hist > 0 else "Bearish Crossover (MACD < Signal)"
        if latest_close > latest_dma50 > latest_dma200:
            trend_regime = "Strong Uptrend (Price > 50-DMA > 200-DMA)"
        elif latest_close < latest_dma50 < latest_dma200:
            trend_regime = "Downtrend (Price < 50-DMA < 200-DMA)"
        elif latest_close > latest_dma200:
            trend_regime = "Long-Term Uptrend, Near-Term Consolidation"
        else:
            trend_regime = "Below 200-DMA Support"

        # Annualized drift (mu) and volatility (sigma)
        mu = float(r.mean() * 252.0)
        sigma = float(r.std(ddof=1) * np.sqrt(252.0))

        # 1,000-path, 252-day GBM simulation:
        # S_t = S_{t-1} * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z)
        Z = np.random.standard_normal((n_days, n_paths))
        daily_Factors = np.exp((mu - 0.5 * (sigma ** 2)) * dt + sigma * np.sqrt(dt) * Z)

        paths = np.zeros((n_days, n_paths), dtype=float)
        paths[0, :] = latest_close * daily_Factors[0, :]
        for t in range(1, n_days):
            paths[t, :] = paths[t - 1, :] * daily_Factors[t, :]

        p10 = np.percentile(paths, 10, axis=1)
        p25 = np.percentile(paths, 25, axis=1)
        p50 = np.percentile(paths, 50, axis=1)
        p75 = np.percentile(paths, 75, axis=1)
        p90 = np.percentile(paths, 90, axis=1)

        terminal_prices = paths[-1, :]
        prob_above_spot = float(np.mean(terminal_prices > latest_close))

        summary_data[ticker] = {
            "name": name,
            "ticker": ticker,
            "cutoff_date": s.index[-1].strftime("%Y-%m-%d"),
            "latest_close": round(latest_close, 2),
            "technicals": {
                "dma_50": round(latest_dma50, 2),
                "dma_200": round(latest_dma200, 2),
                "price_vs_dma50_pct": round((latest_close / latest_dma50 - 1.0) * 100, 2),
                "price_vs_dma200_pct": round((latest_close / latest_dma200 - 1.0) * 100, 2),
                "rsi_14": round(latest_rsi, 2),
                "macd": round(latest_macd, 2),
                "macd_signal": round(latest_signal, 2),
                "macd_histogram": round(latest_hist, 2),
                "rsi_signal": rsi_regime,
                "macd_crossover_signal": macd_regime,
                "trend_regime": trend_regime,
            },
            "monte_carlo": {
                "n_paths": n_paths,
                "horizon_days": n_days,
                "annualized_drift_mu": round(mu, 4),
                "annualized_volatility_sigma": round(sigma, 4),
                "spot_price": round(latest_close, 2),
                "terminal_percentiles": {
                    "p10": round(float(p10[-1]), 2),
                    "p25": round(float(p25[-1]), 2),
                    "p50_median": round(float(p50[-1]), 2),
                    "p75": round(float(p75[-1]), 2),
                    "p90": round(float(p90[-1]), 2),
                    "mean": round(float(np.mean(terminal_prices)), 2),
                },
                "expected_median_return_pct": round(float((p50[-1] / latest_close - 1.0) * 100), 2),
                "prob_terminal_above_spot": round(prob_above_spot, 4),
                "trajectories": {
                    "day": list(range(1, n_days + 1)),
                    "p10": [round(float(x), 2) for x in p10],
                    "p25": [round(float(x), 2) for x in p25],
                    "p50": [round(float(x), 2) for x in p50],
                    "p75": [round(float(x), 2) for x in p75],
                    "p90": [round(float(x), 2) for x in p90],
                },
            },
        }

        print(
            f"{ticker:14s} | Close: {latest_close:8.2f} | 50-DMA: {latest_dma50:8.2f} | 200-DMA: {latest_dma200:8.2f} | "
            f"RSI(14): {latest_rsi:5.2f} ({rsi_regime}) | MACD: {latest_macd:6.2f} vs Sig: {latest_signal:6.2f} (Hist: {latest_hist:+6.2f})\n"
            f"               | MC 1Y Targets -> P10: {p10[-1]:8.2f} | P25: {p25[-1]:8.2f} | "
            f"Median (P50): {p50[-1]:8.2f} ({(p50[-1]/latest_close - 1)*100:+.2f}%) | P75: {p75[-1]:8.2f} | P90: {p90[-1]:8.2f}"
        )

        # Plot fan chart panel
        ax = axes[idx]
        days_axis = np.arange(0, n_days + 1)
        p10_plot = np.insert(p10, 0, latest_close)
        p25_plot = np.insert(p25, 0, latest_close)
        p50_plot = np.insert(p50, 0, latest_close)
        p75_plot = np.insert(p75, 0, latest_close)
        p90_plot = np.insert(p90, 0, latest_close)

        c = colors.get(ticker, "#1f4e78")
        ax.fill_between(days_axis, p10_plot, p90_plot, color=c, alpha=0.18, label="10th-90th Percentile Band")
        ax.fill_between(days_axis, p25_plot, p75_plot, color=c, alpha=0.35, label="25th-75th Percentile Band")
        ax.plot(days_axis, p50_plot, color=c, linewidth=2.2, label=f"Median (P50): INR {p50[-1]:,.0f}")
        ax.axhline(latest_close, color="#444444", linestyle="--", linewidth=1.2, label=f"Spot: INR {latest_close:,.0f}")

        ax.set_title(
            f"{name.replace('_', ' ')} ({ticker})\n1-Yr GBM Monte Carlo (1,000 Paths)",
            fontsize=11.5,
            fontweight="bold",
        )
        ax.set_xlabel("Future Trading Days (1 Year = 252 Days)", fontsize=10)
        if idx == 0:
            ax.set_ylabel("Simulated Share Price (INR)", fontsize=10)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="upper left", fontsize=8.5, frameon=True)

    tech_all_df = pd.concat(tech_frames, ignore_index=True)
    tech_csv_path = cleaned_dir / "technical_series.csv"
    tech_all_df.to_csv(tech_csv_path, index=False)
    print(f"\nSaved last 252 trading days of technical indicators ({len(tech_all_df)} rows) to {tech_csv_path}")

    summary_json_path = cleaned_dir / "technicals_mc_summary.json"
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved technicals & Monte Carlo summary JSON to {summary_json_path}")

    plt.suptitle(
        "1-Year Geometric Brownian Motion (GBM) Monte Carlo Price Trajectories (Seed = 42)",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    fan_chart_path = cleaned_dir / "mc_fan_charts.png"
    plt.savefig(fan_chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved 3-panel Monte Carlo fan charts to {fan_chart_path}")


if __name__ == "__main__":
    main()
