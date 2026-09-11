import pandas as pd


def classify_shock(
    shock_score,
    anomaly,
    severe_threshold=40.0,
):
    """
    Classify an observation using shock score and anomaly detection.

    Parameters
    ----------
    shock_score : float
        Composite financial shock score from 0 to 100.

    anomaly : int
        Isolation Forest prediction:
        1  = normal
        -1 = anomaly

    severe_threshold : float
        Score threshold for a severe shock.

    Returns
    -------
    str
        Shock classification.
    """

    if pd.isna(shock_score):
        return "insufficient_data"

    if shock_score >= 50:
        return "extreme_shock"

    if shock_score >= severe_threshold:
        return "severe_shock"

    if shock_score >= 30:
        return "high_stress"

    if shock_score >= 20:
        return "elevated_stress"

    if anomaly == -1:
        return "anomaly"

    return "normal"