import pandas as pd

from src.data.preprocess import standardize_dates
from src.features.market_features import add_market_features
from src.network.correlation_network import build_correlation_network
from src.propagation.shock_propagation import propagate_shock
from src.propagation.systemic_risk import systemic_risk


DATA_PATH = "data/raw/market_data/indian_stocks.csv"

ORIGIN = "PNB"
INITIAL_SHOCK = 0.6313

RECOVERY = 0.15
TRANSMISSION = 0.15
STEPS = 10


def main():

    print("Loading market data...")

    df = pd.read_csv(DATA_PATH)

    df = standardize_dates(df)

    df = df.sort_values(
        ["ticker", "Date"]
    )

    df = add_market_features(df)

    returns = df.pivot_table(
        index="Date",
        columns="ticker",
        values="return_1d",
    )

    print(f"Trading days: {returns.shape[0]}")
    print(f"Stocks: {returns.shape[1]}")

    print("\nBuilding correlation network...")

    G, corr = build_correlation_network(
        returns,
        threshold=0.60,
    )

    print(f"Network nodes: {G.number_of_nodes()}")
    print(f"Network edges: {G.number_of_edges()}")

    initial = {
        node: 0.0
        for node in G.nodes
    }

    if ORIGIN not in G:
        raise ValueError(
            f"{ORIGIN} is not present in the network."
        )

    initial[ORIGIN] = INITIAL_SHOCK

    print("\n--------------------------------")
    print("SHOCK PROPAGATION")
    print("--------------------------------")

    print(f"Origin: {ORIGIN}")
    print(
        f"Initial shock: {INITIAL_SHOCK:.4f}"
    )

    history = propagate_shock(
        G,
        initial,
        recovery=RECOVERY,
        transmission=TRANSMISSION,
        steps=STEPS,
    )

    rows = []

    for step, shocks in enumerate(history):

        rows.append(
            {
                "step": step,
                "systemic_risk": systemic_risk(
                    shocks
                ),
                "affected_nodes": sum(
                    value > 0.001
                    for value in shocks.values()
                ),
                "maximum_shock": max(
                    shocks.values()
                ),
            }
        )

    results = pd.DataFrame(rows)

    print("\nSystemic Risk:")

    print(
        results.to_string(
            index=False
        )
    )

    final = pd.Series(
        history[-1]
    ).sort_values(
        ascending=False
    )

    print("\nTop affected companies:")

    print(
        final[
            final > 0.001
        ].head(15).to_string()
    )


if __name__ == "__main__":
    main()