from __future__ import annotations

import networkx as nx


def propagate_shock(
    G: nx.Graph,
    initial_shocks: dict[str, float],
    recovery: float = 0.15,
    transmission: float = 0.15,
    steps: int = 10,
) -> list[dict[str, float]]:
    """
    Propagate financial shocks through a weighted network.

    Shock transmission is normalized by the total absolute
    exposure of each node so that highly connected nodes do
    not automatically receive unlimited accumulated shock.
    """

    if steps < 0:
        raise ValueError("steps must be >= 0")

    if not 0 <= recovery <= 1:
        raise ValueError("recovery must be between 0 and 1")

    if not 0 <= transmission <= 1:
        raise ValueError("transmission must be between 0 and 1")

    shock = {
        node: max(
            0.0,
            min(
                1.0,
                float(initial_shocks.get(node, 0.0)),
            ),
        )
        for node in G.nodes
    }

    history = [shock.copy()]

    for _ in range(steps):

        nxt = {}

        for node in G.nodes:

            current = shock[node]

            # Natural recovery of the existing shock.
            retained = current * (1.0 - recovery)

            # Calculate total network exposure.
            total_exposure = sum(
                abs(float(G[node][nbr].get("weight", 0.0)))
                for nbr in G.neighbors(node)
            )

            incoming = 0.0

            if total_exposure > 0:

                for nbr in G.neighbors(node):

                    neighbour_shock = shock.get(nbr, 0.0)

                    weight = abs(
                        float(
                            G[node][nbr].get(
                                "weight",
                                0.0,
                            )
                        )
                    )

                    # Normalize exposure so multiple edges
                    # cannot endlessly amplify the shock.
                    normalized_weight = (
                        weight / total_exposure
                    )

                    incoming += (
                        neighbour_shock
                        * normalized_weight
                        * transmission
                    )

            new_shock = retained + incoming

            nxt[node] = max(
                0.0,
                min(1.0, new_shock),
            )

        shock = nxt
        history.append(shock.copy())

    return history