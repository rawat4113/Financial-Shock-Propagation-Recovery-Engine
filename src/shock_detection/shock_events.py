from __future__ import annotations

import pandas as pd


# ---------------------------------------------------------
# Event configuration
# ---------------------------------------------------------

TRIGGER_LEVELS = {
    "severe_shock",
    "extreme_shock",
    "anomaly",
}


STRONG_CONTINUATION_LEVELS = {
    "high_stress",
    "severe_shock",
    "extreme_shock",
    "anomaly",
}


# Maximum consecutive elevated-stress observations
# allowed inside one event.
MAX_ELEVATED_GAP = 3


# Maximum consecutive normal/insufficient observations
# allowed inside one event.
MAX_NORMAL_GAP = 3


def extract_shock_events(
    df: pd.DataFrame,
    ticker_col: str = "ticker",
    date_col: str = "Date",
    classification_col: str = "classification",
    score_col: str = "shock_score",
) -> pd.DataFrame:
    """
    Extract persistent financial shock events.

    Event starts:
        severe_shock
        extreme_shock
        anomaly

    Strong continuation:
        high_stress
        severe_shock
        extreme_shock
        anomaly

    Temporary bridge:
        elevated_stress

    Recovery:
        normal
        insufficient_data

    Elevated stress cannot keep an event alive indefinitely.
    """

    # ---------------------------------------------------------
    # Validate input
    # ---------------------------------------------------------

    required = {
        ticker_col,
        date_col,
        classification_col,
        score_col,
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # ---------------------------------------------------------
    # Prepare data
    # ---------------------------------------------------------

    data = df.copy()

    data[date_col] = pd.to_datetime(
        data[date_col],
        errors="coerce",
    )

    data[score_col] = pd.to_numeric(
        data[score_col],
        errors="coerce",
    )

    data = data.dropna(
        subset=[
            ticker_col,
            date_col,
        ]
    )

    data = data.sort_values(
        [
            ticker_col,
            date_col,
        ]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # Event storage
    # ---------------------------------------------------------

    events = []

    # ---------------------------------------------------------
    # Process each ticker separately
    # ---------------------------------------------------------

    for ticker, group in data.groupby(
        ticker_col,
        sort=False,
    ):

        group = group.reset_index(drop=True)

        active = False

        normal_gap = 0
        elevated_gap = 0

        event_rows = []

        event_number = 0

        # -----------------------------------------------------
        # Close event helper
        # -----------------------------------------------------

        def close_event():

            nonlocal event_rows
            nonlocal active
            nonlocal normal_gap
            nonlocal elevated_gap
            nonlocal event_number

            if not event_rows:
                return

            event_df = pd.DataFrame(
                event_rows
            )

            event_df[score_col] = pd.to_numeric(
                event_df[score_col],
                errors="coerce",
            )

            # ---------------------------------------------
            # Find peak shock
            # ---------------------------------------------

            valid_scores = event_df[
                score_col
            ].notna()

            if valid_scores.any():

                peak_idx = event_df[
                    score_col
                ].idxmax()

                peak_row = event_df.loc[
                    peak_idx
                ]

            else:

                peak_row = event_df.iloc[0]

            # ---------------------------------------------
            # Event number
            # ---------------------------------------------

            event_number += 1

            # ---------------------------------------------
            # Store event
            # ---------------------------------------------

            events.append(
                {
                    "event_id": (
                        f"{ticker}_{event_number}"
                    ),
                    "ticker": ticker,
                    "start_date": event_df[
                        date_col
                    ].min(),
                    "end_date": event_df[
                        date_col
                    ].max(),
                    "duration": len(event_df),
                    "peak_date": peak_row[
                        date_col
                    ],
                    "peak_score": peak_row[
                        score_col
                    ],
                    "severity": peak_row[
                        classification_col
                    ],
                }
            )

            # ---------------------------------------------
            # Reset state
            # ---------------------------------------------

            event_rows = []

            active = False

            normal_gap = 0

            elevated_gap = 0

        # -----------------------------------------------------
        # Daily processing
        # -----------------------------------------------------

        for _, row in group.iterrows():

            classification = row[
                classification_col
            ]

            # =================================================
            # NO ACTIVE EVENT
            # =================================================

            if not active:

                if classification in TRIGGER_LEVELS:

                    active = True

                    normal_gap = 0

                    elevated_gap = 0

                    event_rows = [
                        row.to_dict()
                    ]

                continue

            # =================================================
            # STRONG SHOCK / STRESS
            # =================================================

            if (
                classification
                in STRONG_CONTINUATION_LEVELS
            ):

                event_rows.append(
                    row.to_dict()
                )

                normal_gap = 0

                elevated_gap = 0

                continue

            # =================================================
            # ELEVATED STRESS
            # =================================================

            if classification == "elevated_stress":

                elevated_gap += 1

                normal_gap = 0

                # Keep elevated-stress observations
                # while they remain within the bridge.
                if (
                    elevated_gap
                    <= MAX_ELEVATED_GAP
                ):

                    event_rows.append(
                        row.to_dict()
                    )

                else:

                    close_event()

                continue

            # =================================================
            # NORMAL / INSUFFICIENT DATA
            # =================================================

            normal_gap += 1

            elevated_gap = 0

            if normal_gap <= MAX_NORMAL_GAP:

                event_rows.append(
                    row.to_dict()
                )

            else:

                close_event()

        # -----------------------------------------------------
        # Close event at end of ticker
        # -----------------------------------------------------

        if active:

            close_event()

    # ---------------------------------------------------------
    # No events
    # ---------------------------------------------------------

    if not events:

        return pd.DataFrame(
            columns=[
                "event_id",
                "ticker",
                "start_date",
                "end_date",
                "duration",
                "peak_date",
                "peak_score",
                "severity",
            ]
        )

    # ---------------------------------------------------------
    # Result DataFrame
    # ---------------------------------------------------------

    result = pd.DataFrame(events)

    result["start_date"] = pd.to_datetime(
        result["start_date"],
        errors="coerce",
    )

    result["end_date"] = pd.to_datetime(
        result["end_date"],
        errors="coerce",
    )

    result["peak_date"] = pd.to_datetime(
        result["peak_date"],
        errors="coerce",
    )

    result["duration"] = pd.to_numeric(
        result["duration"],
        errors="coerce",
    ).astype(int)

    result["peak_score"] = pd.to_numeric(
        result["peak_score"],
        errors="coerce",
    )

    # ---------------------------------------------------------
    # Sort
    # ---------------------------------------------------------

    result = result.sort_values(
        [
            "start_date",
            "peak_score",
        ],
        ascending=[
            True,
            False,
        ],
    ).reset_index(drop=True)

    return result