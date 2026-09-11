"""
Financial Shock Propagation & Recovery Engine
==============================================

End-to-end pipeline:

1. Load market data
2. Preprocess dates
3. Generate market features
4. Detect financial shocks
5. Extract shock events
6. Build correlation network
7. Propagate a selected shock
8. Calculate systemic risk
9. Simulate recovery
10. Generate visualizations
11. Save results
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import pandas as pd

from src.data.preprocess import standardize_dates
from src.features.market_features import add_market_features
from src.features.risk_features import rolling_zscore

from src.shock_detection.shock_score import shock_score
from src.shock_detection.anomaly_detection import fit_isolation_forest
from src.shock_detection.shock_detector import classify_shock
from src.shock_detection.shock_events import extract_shock_events

from src.network.correlation_network import build_correlation_network

from src.propagation.shock_propagation import propagate_shock
from src.propagation.systemic_risk import systemic_risk

from src.recovery.scenario_simulator import simulate_market_shock
from src.recovery.recovery_prediction import recovery_days

from src.visualization.shock_plot import plot_shock
from src.visualization.network_plot import plot_network
from src.visualization.recovery_plot import plot_recovery


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DATA_PATH = Path("data/raw/market_data/indian_stocks.csv")
OUTPUT_DIR = Path("outputs")

ORIGIN = "PNB"

CORRELATION_THRESHOLD = 0.60

PROPAGATION_RECOVERY = 0.15
PROPAGATION_TRANSMISSION = 0.15
PROPAGATION_STEPS = 10

RECOVERY_DAYS = 180
DAILY_RECOVERY = 0.10
RECOVERY_TARGET = 0.99


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def ensure_output_directory() -> None:
    """Create output directory if it does not exist."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def print_header(title: str) -> None:
    """Print a formatted section header."""

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------

def main() -> None:

    ensure_output_directory()

    # ================================================================
    # 1. LOAD DATA
    # ================================================================

    print_header("FINANCIAL SHOCK PROPAGATION & RECOVERY ENGINE")

    print("Loading market data...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Market data not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    df = standardize_dates(df)

    if "ticker" not in df.columns:
        raise KeyError(
            "Expected 'ticker' column in market dataset."
        )

    df = df.sort_values(["ticker", "Date"]).reset_index(drop=True)

    print(f"Trading days: {df['Date'].nunique()}")
    print(f"Stocks: {df['ticker'].nunique()}")
    print(f"Daily rows: {len(df):,}")

    # ================================================================
    # 2. FEATURE ENGINEERING
    # ================================================================

    print_header("FEATURE ENGINEERING")

    print("Generating market features...")

    df = add_market_features(df)

    # Rolling return z-score for each company.
    df["return_zscore"] = (
        df.groupby("ticker")["return_1d"]
        .transform(
            lambda x: rolling_zscore(x, 60)
        )
    )

    # ================================================================
    # 3. SHOCK SCORE
    # ================================================================

    print("Calculating shock scores...")

    df["shock_score"] = shock_score(
        df["return_zscore"],
        df["volatility_20d"],
        df["drawdown"],
    )

    # ================================================================
    # 4. ANOMALY DETECTION
    # ================================================================

    print("Running Isolation Forest anomaly detection...")

    feature_columns = [
        "return_zscore",
        "volatility_20d",
        "drawdown",
    ]

    valid_features = (
        df[feature_columns]
        .replace([float("inf"), float("-inf")], pd.NA)
        .dropna()
    )

    df["anomaly"] = 1.0

    if len(valid_features) > 0:

        model = fit_isolation_forest(valid_features)

        df.loc[
            valid_features.index,
            "anomaly",
        ] = model.predict(valid_features)

    # ================================================================
    # 5. SHOCK CLASSIFICATION
    # ================================================================

    print("Classifying observations...")

    df["classification"] = [
        classify_shock(score, anomaly)
        for score, anomaly in zip(
            df["shock_score"],
            df["anomaly"],
        )
    ]

    print()
    print("Classification distribution:")
    print(
        df["classification"]
        .value_counts()
        .to_string()
    )

    # ================================================================
    # 6. SHOCK EVENTS
    # ================================================================

    print_header("SHOCK EVENT DETECTION")

    events = extract_shock_events(df)

    print(f"Shock events detected: {len(events):,}")

    if not events.empty:

        print()
        print("Event severity:")
        print(
            events["severity"]
            .value_counts()
            .to_string()
        )

        print()
        print("Top persistent events:")

        columns = [
            "event_id",
            "ticker",
            "start_date",
            "end_date",
            "duration",
            "peak_date",
            "peak_score",
            "severity",
        ]

        print(
            events
            .nlargest(10, "duration")[columns]
            .to_string(index=False)
        )

    # ================================================================
    # 7. BUILD RETURN MATRIX
    # ================================================================

    print_header("CORRELATION NETWORK")

    returns = df.pivot_table(
        index="Date",
        columns="ticker",
        values="return_1d",
    )

    print(f"Return matrix: {returns.shape}")

    G, correlation_matrix = build_correlation_network(
        returns,
        threshold=CORRELATION_THRESHOLD,
    )

    print(f"Network nodes: {G.number_of_nodes()}")
    print(f"Network edges: {G.number_of_edges()}")

    if G.number_of_nodes() > 1:
        print(
            f"Network density: "
            f"{nx.density(G):.6f}"
        )

    # ================================================================
    # 8. SHOCK ORIGIN
    # ================================================================

    print_header("SHOCK PROPAGATION")

    if ORIGIN not in G:
        raise ValueError(
            f"Origin ticker '{ORIGIN}' "
            f"is not present in the network."
        )

    # Find strongest historical shock for origin.
    origin_rows = df[
        df["ticker"] == ORIGIN
    ].dropna(subset=["shock_score"])

    if origin_rows.empty:
        raise ValueError(
            f"No valid shock data found for {ORIGIN}."
        )

    origin_row = origin_rows.loc[
        origin_rows["shock_score"].idxmax()
    ]

    initial_shock = float(
        origin_row["shock_score"]
    ) / 100.0

    initial_shock = max(
        0.0,
        min(1.0, initial_shock),
    )

    print(f"Origin: {ORIGIN}")
    print(
        f"Shock date: "
        f"{origin_row['Date'].date()}"
    )
    print(
        f"Initial shock score: "
        f"{origin_row['shock_score']:.4f}"
    )
    print(
        f"Initial shock level: "
        f"{initial_shock:.4f}"
    )

    # ================================================================
    # 9. PROPAGATION
    # ================================================================

    initial = {
        node: 0.0
        for node in G.nodes
    }

    initial[ORIGIN] = initial_shock

    history = propagate_shock(
        G,
        initial,
        recovery=PROPAGATION_RECOVERY,
        transmission=PROPAGATION_TRANSMISSION,
        steps=PROPAGATION_STEPS,
    )

    systemic_values = []
    affected_counts = []
    maximum_shocks = []

    for state in history:

        systemic_values.append(
            systemic_risk(state)
        )

        affected_counts.append(
            sum(
                1
                for value in state.values()
                if value > 0.001
            )
        )

        maximum_shocks.append(
            max(state.values())
            if state
            else 0.0
        )

    propagation_results = pd.DataFrame(
        {
            "step": range(len(history)),
            "systemic_risk": systemic_values,
            "affected_nodes": affected_counts,
            "maximum_shock": maximum_shocks,
        }
    )

    print()
    print("Systemic Risk:")
    print(
        propagation_results
        .to_string(index=False)
    )

    # ================================================================
    # 10. TOP AFFECTED COMPANIES
    # ================================================================

    final_shocks = (
        pd.Series(history[-1])
        .sort_values(ascending=False)
    )

    print()
    print("Top affected companies:")

    print(
        final_shocks[
            final_shocks > 0.001
        ]
        .head(20)
        .to_string()
    )

    # ================================================================
    # 11. RECOVERY SIMULATION
    # ================================================================

    print_header("RECOVERY SIMULATION")

    recovery_path = simulate_market_shock(
        base_return=0.0,
        shock_pct=-initial_shock,
        days=RECOVERY_DAYS,
        daily_recovery=DAILY_RECOVERY,
    )

    recovery_day = recovery_days(
        recovery_path,
        target=RECOVERY_TARGET,
    )

    recovery_results = pd.DataFrame(
        recovery_path,
        columns=[
            "day",
            "portfolio_value",
        ],
    )

    print(
        f"Initial portfolio value: "
        f"{recovery_path[0][1]:.6f}"
    )

    print(
        f"Final portfolio value: "
        f"{recovery_path[-1][1]:.6f}"
    )

    if recovery_day is not None:
        print(
            f"Recovery to {RECOVERY_TARGET:.0%}: "
            f"Day {recovery_day}"
        )
    else:
        print(
            f"Recovery target of "
            f"{RECOVERY_TARGET:.0%} not reached."
        )

    # ================================================================
    # 12. SAVE DATA RESULTS
    # ================================================================

    print_header("SAVING RESULTS")

    df.to_csv(
        OUTPUT_DIR / "processed_market_data.csv",
        index=False,
    )

    events.to_csv(
        OUTPUT_DIR / "shock_events.csv",
        index=False,
    )

    correlation_matrix.to_csv(
        OUTPUT_DIR / "correlation_matrix.csv"
    )

    propagation_results.to_csv(
        OUTPUT_DIR / "propagation_results.csv",
        index=False,
    )

    recovery_results.to_csv(
        OUTPUT_DIR / "recovery_results.csv",
        index=False,
    )

    # ================================================================
    # 13. VISUALIZATIONS
    # ================================================================

    print("Generating visualizations...")

    # Shock plot for selected origin.
    origin_plot = df[
        df["ticker"] == ORIGIN
    ].dropna(subset=["shock_score"])

    if not origin_plot.empty:

        plot_shock(
            origin_plot["Date"],
            origin_plot["shock_score"],
        )

        import matplotlib.pyplot as plt

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR / "shock_timeline.png",
            dpi=150,
            bbox_inches="tight",
        )

        plt.close()

    # Network graph.
    plot_network(G)

    import matplotlib.pyplot as plt

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "correlation_network.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    # Recovery curve.
    plot_recovery(
        recovery_results["day"],
        recovery_results["portfolio_value"],
    )

    plt.axhline(
        RECOVERY_TARGET,
        linestyle="--",
        linewidth=1,
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "recovery_curve.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    # ================================================================
    # 14. FINAL SUMMARY
    # ================================================================

    print_header("ENGINE COMPLETE")

    print(f"Market stocks:          {df['ticker'].nunique()}")
    print(f"Trading days:           {df['Date'].nunique():,}")
    print(f"Daily observations:     {len(df):,}")
    print(f"Shock events:           {len(events):,}")
    print(f"Network nodes:          {G.number_of_nodes()}")
    print(f"Network edges:          {G.number_of_edges()}")
    print(f"Shock origin:           {ORIGIN}")
    print(f"Initial shock:          {initial_shock:.4f}")
    print(
        f"Final systemic risk:   "
        f"{systemic_values[-1]:.4f}"
    )
    print(
        f"Final maximum shock:   "
        f"{maximum_shocks[-1]:.4f}"
    )

    if recovery_day is not None:
        print(
            f"Recovery day:          "
            f"{recovery_day}"
        )
    else:
        print("Recovery day:          Not reached")

    print()
    print("Output files:")
    print("  ✓ outputs/processed_market_data.csv")
    print("  ✓ outputs/shock_events.csv")
    print("  ✓ outputs/correlation_matrix.csv")
    print("  ✓ outputs/propagation_results.csv")
    print("  ✓ outputs/recovery_results.csv")
    print("  ✓ outputs/shock_timeline.png")
    print("  ✓ outputs/correlation_network.png")
    print("  ✓ outputs/recovery_curve.png")


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()