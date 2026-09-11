import numpy as np


def shock_score(z_score, volatility_score, drawdown_score):
    z = np.clip(np.abs(z_score) / 5, 0, 1)
    v = np.clip(volatility_score, 0, 1)
    d = np.clip(np.abs(drawdown_score), 0, 1)

    return 100 * (
        0.4 * z +
        0.3 * v +
        0.3 * d
    )