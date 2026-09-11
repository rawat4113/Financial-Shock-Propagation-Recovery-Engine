"""
Realistic market shock and recovery simulation.
"""

from __future__ import annotations


def simulate_market_shock(
    base_return: float,
    shock_pct: float,
    days: int = 90,
    daily_recovery: float = 0.01,
) -> list[tuple[int, float]]:
    """
    Simulate a market shock followed by gradual mean-reverting recovery.

    The portfolio starts at 1.0, experiences the shock on day 0,
    and then gradually moves back toward 1.0.

    Parameters
    ----------
    base_return:
        Normal daily market return.
    shock_pct:
        Initial shock, e.g. -0.30 = -30%.
    days:
        Number of simulation days.
    daily_recovery:
        Fraction of the remaining gap recovered per day.

    Returns
    -------
    list[tuple[int, float]]
        Day/value pairs.
    """

    if days <= 0:
        raise ValueError("days must be greater than 0")

    if shock_pct < -1:
        raise ValueError("shock_pct cannot be less than -1")

    if daily_recovery <= 0 or daily_recovery > 1:
        raise ValueError("daily_recovery must be between 0 and 1")

    value = 1.0
    path: list[tuple[int, float]] = []

    for day in range(days):

        if day == 0:
            value *= 1.0 + shock_pct

        else:
            # Distance from the normal baseline.
            gap = 1.0 - value

            # Recover a fraction of the remaining gap.
            recovery = gap * daily_recovery

            # Small normal-market contribution.
            value += recovery + base_return

            # Do not allow the simulation to overshoot the baseline.
            if value > 1.0:
                value = 1.0

            value = max(0.0, value)

        path.append((day, value))

    return path