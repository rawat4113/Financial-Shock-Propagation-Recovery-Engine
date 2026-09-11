from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Financial Shock Propagation & Recovery Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📈 Financial Shock Propagation & Recovery Engine</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Interactive dashboard for financial shock detection, "
    "propagation, systemic risk and recovery analysis."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(filename):
    path = OUTPUT_DIR / filename

    if not path.exists():
        return None

    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return None


@st.cache_data
def load_correlation_matrix():
    path = OUTPUT_DIR / "correlation_matrix.csv"

    if not path.exists():
        return None

    try:
        matrix = pd.read_csv(
            path,
            index_col=0,
        )

        matrix = matrix.apply(
            pd.to_numeric,
            errors="coerce",
        )

        return matrix

    except Exception as e:
        st.error(
            f"Error loading correlation matrix: {e}"
        )
        return None


def find_column(df, names):

    if df is None:
        return None

    column_map = {
        str(column).lower(): column
        for column in df.columns
    }

    for name in names:

        if name.lower() in column_map:
            return column_map[name.lower()]

    return None


def format_number(value, decimals=2):

    if value is None:
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"

    except Exception:
        return str(value)


# ============================================================
# LOAD DATA
# ============================================================

market_df = load_csv(
    "processed_market_data.csv"
)

events_df = load_csv(
    "shock_events.csv"
)

correlation_matrix = load_correlation_matrix()

propagation_df = load_csv(
    "propagation_results.csv"
)

recovery_df = load_csv(
    "recovery_results.csv"
)


# ============================================================
# REQUIRED FILE CHECK
# ============================================================

missing = []

if market_df is None:
    missing.append(
        "processed_market_data.csv"
    )

if events_df is None:
    missing.append(
        "shock_events.csv"
    )

if correlation_matrix is None:
    missing.append(
        "correlation_matrix.csv"
    )

if propagation_df is None:
    missing.append(
        "propagation_results.csv"
    )

if recovery_df is None:
    missing.append(
        "recovery_results.csv"
    )


if missing:

    st.warning(
        "Some engine output files are missing."
    )

    st.write("Missing files:")

    for filename in missing:
        st.write(
            f"- `{filename}`"
        )

    st.info(
        "Run the engine first:"
    )

    st.code(
        "python .\\run_engine.py",
        language="powershell",
    )

    st.stop()


# ============================================================
# GLOBAL MARKET INFORMATION
# ============================================================

if "ticker" in market_df.columns:

    total_stocks = (
        market_df["ticker"]
        .nunique()
    )

else:

    total_stocks = 0


if "Date" in market_df.columns:

    dates = pd.to_datetime(
        market_df["Date"],
        errors="coerce",
    )

    trading_days = dates.nunique()

else:

    trading_days = 0


daily_rows = len(market_df)

total_events = len(events_df)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚙️ Dashboard"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Section",
    [
        "🏠 Overview",
        "🚨 Shock Events",
        "🌐 Correlation Network",
        "💥 Shock Propagation",
        "🔄 Recovery Analysis",
        "📊 Market Data",
    ],
)

st.sidebar.markdown("---")

st.sidebar.success(
    "Engine outputs loaded successfully."
)

st.sidebar.markdown(
    """
### Pipeline

Market Data

↓

Feature Engineering

↓

Shock Detection

↓

Shock Events

↓

Correlation Network

↓

Shock Propagation

↓

Recovery Simulation
"""
)


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">'
        "System Overview"
        "</div>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # MAIN METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Market Stocks",
        f"{total_stocks:,}",
    )

    c2.metric(
        "Trading Days",
        f"{trading_days:,}",
    )

    c3.metric(
        "Daily Observations",
        f"{daily_rows:,}",
    )

    c4.metric(
        "Shock Events",
        f"{total_events:,}",
    )

    c5.metric(
        "Network Nodes",
        f"{len(correlation_matrix.columns):,}",
    )

    st.markdown("---")

    # --------------------------------------------------------
    # ENGINE STATUS
    # --------------------------------------------------------

    st.subheader(
        "✅ Engine Status"
    )

    status1, status2, status3, status4 = st.columns(4)

    status1.success(
        "Market Data Loaded"
    )

    status2.success(
        "Shock Detection Complete"
    )

    status3.success(
        "Network Analysis Complete"
    )

    status4.success(
        "Recovery Analysis Complete"
    )

    # --------------------------------------------------------
    # CLASSIFICATION DISTRIBUTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        "Shock Classification"
        "</div>",
        unsafe_allow_html=True,
    )

    classification_col = find_column(
        market_df,
        ["classification"],
    )

    if classification_col:

        counts = (
            market_df[
                classification_col
            ]
            .value_counts()
            .rename_axis(
                "classification"
            )
            .reset_index(
                name="count"
            )
        )

        left, right = st.columns(
            [1, 2]
        )

        with left:

            st.dataframe(
                counts,
                use_container_width=True,
                hide_index=True,
            )

        with right:

            chart_data = (
                counts
                .set_index(
                    "classification"
                )
            )

            st.bar_chart(
                chart_data
            )

    # --------------------------------------------------------
    # TOP EVENTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        "🔥 Top Persistent Shock Events"
        "</div>",
        unsafe_allow_html=True,
    )

    if "duration" in events_df.columns:

        top_events = (
            events_df
            .sort_values(
                "duration",
                ascending=False,
            )
            .head(10)
        )

        st.dataframe(
            top_events,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# PAGE 2 — SHOCK EVENTS
# ============================================================

elif page == "🚨 Shock Events":

    st.markdown(
        '<div class="section-title">'
        "🚨 Shock Event Detection"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Detected financial stress and shock events "
        "across the 50-stock market."
    )

    # --------------------------------------------------------
    # SEVERITY
    # --------------------------------------------------------

    if "severity" in events_df.columns:

        severity_counts = (
            events_df[
                "severity"
            ]
            .value_counts()
            .rename_axis(
                "severity"
            )
            .reset_index(
                name="events"
            )
        )

        left, right = st.columns(2)

        with left:

            st.subheader(
                "Event Severity"
            )

            st.dataframe(
                severity_counts,
                use_container_width=True,
                hide_index=True,
            )

        with right:

            st.subheader(
                "Severity Distribution"
            )

            st.bar_chart(
                severity_counts.set_index(
                    "severity"
                )
            )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.subheader(
        "🔎 Event Explorer"
    )

    filtered_events = (
        events_df.copy()
    )

    if "severity" in events_df.columns:

        severity_options = sorted(
            events_df[
                "severity"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_severity = st.multiselect(
            "Severity",
            severity_options,
            default=severity_options,
        )

        filtered_events = (
            filtered_events[
                filtered_events[
                    "severity"
                ].isin(
                    selected_severity
                )
            ]
        )

    if "ticker" in events_df.columns:

        ticker_options = sorted(
            events_df[
                "ticker"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_tickers = st.multiselect(
            "Companies",
            ticker_options,
            default=[],
            placeholder="All companies",
        )

        if selected_tickers:

            filtered_events = (
                filtered_events[
                    filtered_events[
                        "ticker"
                    ].isin(
                        selected_tickers
                    )
                ]
            )

    st.write(
        f"Showing **{len(filtered_events):,}** events."
    )

    st.dataframe(
        filtered_events.sort_values(
            "duration",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 3 — CORRELATION NETWORK
# ============================================================

elif page == "🌐 Correlation Network":

    st.markdown(
        '<div class="section-title">'
        "🌐 Financial Correlation Network"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "This section shows how companies move together "
        "based on their historical daily returns."
    )

    # --------------------------------------------------------
    # MATRIX INFORMATION
    # --------------------------------------------------------

    number_of_stocks = (
        len(correlation_matrix.columns)
    )

    # --------------------------------------------------------
    # THRESHOLD
    # --------------------------------------------------------

    threshold = st.slider(
        "Correlation threshold",
        min_value=0.30,
        max_value=0.90,
        value=0.60,
        step=0.05,
    )

    # --------------------------------------------------------
    # BUILD PAIRS
    # --------------------------------------------------------

    pairs = []

    tickers = (
        correlation_matrix.columns.tolist()
    )

    for i, ticker_a in enumerate(
        tickers
    ):

        for ticker_b in tickers[
            i + 1:
        ]:

            value = (
                correlation_matrix.loc[
                    ticker_a,
                    ticker_b,
                ]
            )

            if pd.notna(value):

                pairs.append(
                    {
                        "ticker_a": ticker_a,
                        "ticker_b": ticker_b,
                        "correlation": float(
                            value
                        ),
                    }
                )

    pairs_df = pd.DataFrame(
        pairs
    )

    # --------------------------------------------------------
    # STRONG EDGES
    # --------------------------------------------------------

    strong_pairs = (
        pairs_df[
            pairs_df[
                "correlation"
            ].abs()
            >= threshold
        ]
        .copy()
    )

    network_edges = len(
        strong_pairs
    )

    if number_of_stocks > 1:

        density = (
            2 * network_edges
            / (
                number_of_stocks
                * (
                    number_of_stocks - 1
                )
            )
        )

    else:

        density = 0

    # --------------------------------------------------------
    # NETWORK METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Network Nodes",
        number_of_stocks,
    )

    c2.metric(
        "Network Edges",
        network_edges,
    )

    c3.metric(
        "Network Density",
        f"{density:.6f}",
    )

    c4.metric(
        "Threshold",
        f"±{threshold:.2f}",
    )

    st.markdown("---")

    # --------------------------------------------------------
    # NETWORK IMAGE
    # --------------------------------------------------------

    network_image = (
        OUTPUT_DIR
        / "correlation_network.png"
    )

    if network_image.exists():

        st.subheader(
            "🕸️ Correlation Network Graph"
        )

        st.image(
            str(network_image),
            use_container_width=True,
        )

    # --------------------------------------------------------
    # FULL MATRIX
    # --------------------------------------------------------

    st.subheader(
        "📊 Full 50 × 50 Correlation Matrix"
    )

    st.write(
        "Each cell represents the correlation "
        "between two stocks."
    )

    st.dataframe(
        correlation_matrix.style.format(
            "{:.3f}",
            na_rep="—",
        ),
        use_container_width=True,
        height=650,
    )

    # --------------------------------------------------------
    # STRONGEST CORRELATIONS
    # --------------------------------------------------------

    st.subheader(
        "🔥 Strongest Stock Correlations"
    )

    strongest = (
        pairs_df
        .assign(
            absolute_correlation=
            pairs_df[
                "correlation"
            ].abs()
        )
        .sort_values(
            "absolute_correlation",
            ascending=False,
        )
        .drop(
            columns=[
                "absolute_correlation"
            ]
        )
        .head(30)
    )

    st.dataframe(
        strongest,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # THRESHOLD FILTER
    # --------------------------------------------------------

    st.subheader(
        f"🔗 Correlations Above ±{threshold:.2f}"
    )

    if strong_pairs.empty:

        st.warning(
            "No correlations found at this threshold."
        )

    else:

        strong_pairs = (
            strong_pairs
            .sort_values(
                "correlation",
                key=lambda x: x.abs(),
                ascending=False,
            )
        )

        st.dataframe(
            strong_pairs,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # COMPANY EXPLORER
    # --------------------------------------------------------

    st.subheader(
        "🔎 Company Correlation Explorer"
    )

    selected_company = st.selectbox(
        "Select company",
        tickers,
    )

    company_correlations = (
        correlation_matrix[
            selected_company
        ]
        .drop(
            selected_company,
            errors="ignore",
        )
        .dropna()
        .sort_values(
            key=lambda x: x.abs(),
            ascending=False,
        )
    )

    company_corr_df = (
        company_correlations
        .rename(
            "correlation"
        )
        .reset_index()
    )

    company_corr_df.columns = [
        "company",
        "correlation",
    ]

    st.write(
        f"Strongest correlations with "
        f"**{selected_company}**:"
    )

    st.dataframe(
        company_corr_df.head(20),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 4 — SHOCK PROPAGATION
# ============================================================

elif page == "💥 Shock Propagation":

    st.markdown(
        '<div class="section-title">'
        "💥 Shock Propagation Analysis"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Observe how the initial shock propagates "
        "through interconnected companies."
    )

    # --------------------------------------------------------
    # FIND COLUMNS
    # --------------------------------------------------------

    step_col = find_column(
        propagation_df,
        ["step"],
    )

    risk_col = find_column(
        propagation_df,
        ["systemic_risk"],
    )

    affected_col = find_column(
        propagation_df,
        ["affected_nodes"],
    )

    maximum_col = find_column(
        propagation_df,
        ["maximum_shock"],
    )

    # --------------------------------------------------------
    # FINAL VALUES
    # --------------------------------------------------------

    final_risk = None
    final_affected = None
    final_maximum = None

    if risk_col:

        final_risk = (
            propagation_df[
                risk_col
            ].iloc[-1]
        )

    if affected_col:

        final_affected = (
            propagation_df[
                affected_col
            ].iloc[-1]
        )

    if maximum_col:

        final_maximum = (
            propagation_df[
                maximum_col
            ].iloc[-1]
        )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Final Systemic Risk",
        format_number(
            final_risk,
            4,
        ),
    )

    c2.metric(
        "Final Maximum Shock",
        format_number(
            final_maximum,
            4,
        ),
    )

    c3.metric(
        "Affected Nodes",
        format_number(
            final_affected,
            0,
        ),
    )

    st.markdown("---")

    # --------------------------------------------------------
    # SYSTEMIC RISK
    # --------------------------------------------------------

    if step_col and risk_col:

        st.subheader(
            "📈 Systemic Risk Over Time"
        )

        risk_chart = (
            propagation_df[
                [
                    step_col,
                    risk_col,
                ]
            ]
            .set_index(
                step_col
            )
        )

        st.line_chart(
            risk_chart
        )

    # --------------------------------------------------------
    # AFFECTED NODES
    # --------------------------------------------------------

    if (
        step_col
        and affected_col
    ):

        st.subheader(
            "🏢 Affected Companies"
        )

        affected_chart = (
            propagation_df[
                [
                    step_col,
                    affected_col,
                ]
            ]
            .set_index(
                step_col
            )
        )

        st.line_chart(
            affected_chart
        )

    # --------------------------------------------------------
    # MAXIMUM SHOCK
    # --------------------------------------------------------

    if (
        step_col
        and maximum_col
    ):

        st.subheader(
            "💥 Maximum Propagated Shock"
        )

        maximum_chart = (
            propagation_df[
                [
                    step_col,
                    maximum_col,
                ]
            ]
            .set_index(
                step_col
            )
        )

        st.line_chart(
            maximum_chart
        )

    # --------------------------------------------------------
    # RAW DATA
    # --------------------------------------------------------

    st.subheader(
        "Propagation Results"
    )

    st.dataframe(
        propagation_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 5 — RECOVERY ANALYSIS
# ============================================================

elif page == "🔄 Recovery Analysis":

    st.markdown(
        '<div class="section-title">'
        "🔄 Recovery Simulation"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Simulation of portfolio recovery following "
        "a financial shock."
    )

    # --------------------------------------------------------
    # FIND COLUMNS
    # --------------------------------------------------------

    day_col = find_column(
        recovery_df,
        [
            "day",
            "days",
        ],
    )

    value_col = find_column(
        recovery_df,
        [
            "value",
            "portfolio_value",
            "recovery_value",
        ],
    )

    # --------------------------------------------------------
    # VALUES
    # --------------------------------------------------------

    initial_value = None
    final_value = None
    recovery_day = None

    if value_col:

        initial_value = (
            recovery_df[
                value_col
            ].iloc[0]
        )

        final_value = (
            recovery_df[
                value_col
            ].iloc[-1]
        )

    if (
        value_col
        and day_col
    ):

        recovered = (
            recovery_df[
                recovery_df[
                    value_col
                ] >= 0.99
            ]
        )

        if not recovered.empty:

            recovery_day = int(
                recovered.iloc[0][
                    day_col
                ]
            )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Initial Portfolio Value",
        format_number(
            initial_value,
            4,
        ),
    )

    c2.metric(
        "Final Portfolio Value",
        format_number(
            final_value,
            4,
        ),
    )

    c3.metric(
        "Recovery to 99%",
        (
            f"Day {recovery_day}"
            if recovery_day is not None
            else "Not reached"
        ),
    )

    st.markdown("---")

    # --------------------------------------------------------
    # RECOVERY IMAGE
    # --------------------------------------------------------

    recovery_image = (
        OUTPUT_DIR
        / "recovery_curve.png"
    )

    if recovery_image.exists():

        st.subheader(
            "📈 Recovery Curve"
        )

        st.image(
            str(recovery_image),
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RECOVERY CHART
    # --------------------------------------------------------

    if (
        day_col
        and value_col
    ):

        st.subheader(
            "Interactive Recovery Curve"
        )

        recovery_chart = (
            recovery_df[
                [
                    day_col,
                    value_col,
                ]
            ]
            .set_index(
                day_col
            )
        )

        st.line_chart(
            recovery_chart
        )

    # --------------------------------------------------------
    # RECOVERY DATA
    # --------------------------------------------------------

    st.subheader(
        "Recovery Simulation Data"
    )

    st.dataframe(
        recovery_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 6 — MARKET DATA
# ============================================================

elif page == "📊 Market Data":

    st.markdown(
        '<div class="section-title">'
        "📊 Processed Market Data"
        "</div>",
        unsafe_allow_html=True,
    )

    filtered_market = (
        market_df.copy()
    )

    # --------------------------------------------------------
    # COMPANY FILTER
    # --------------------------------------------------------

    if "ticker" in market_df.columns:

        ticker_list = sorted(
            market_df[
                "ticker"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_ticker = st.selectbox(
            "Select company",
            ["All"] + ticker_list,
        )

        if selected_ticker != "All":

            filtered_market = (
                filtered_market[
                    filtered_market[
                        "ticker"
                    ]
                    == selected_ticker
                ]
            )

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    if "Date" in filtered_market.columns:

        filtered_market[
            "Date"
        ] = pd.to_datetime(
            filtered_market[
                "Date"
            ],
            errors="coerce",
        )

        valid_dates = (
            filtered_market[
                "Date"
            ]
            .dropna()
        )

        if not valid_dates.empty:

            minimum_date = (
                valid_dates
                .min()
                .date()
            )

            maximum_date = (
                valid_dates
                .max()
                .date()
            )

            selected_dates = st.date_input(
                "Date range",
                value=(
                    minimum_date,
                    maximum_date,
                ),
                min_value=minimum_date,
                max_value=maximum_date,
            )

            if (
                isinstance(
                    selected_dates,
                    tuple,
                )
                and len(
                    selected_dates
                ) == 2
            ):

                start_date = (
                    selected_dates[0]
                )

                end_date = (
                    selected_dates[1]
                )

                filtered_market = (
                    filtered_market[
                        (
                            filtered_market[
                                "Date"
                            ].dt.date
                            >= start_date
                        )
                        &
                        (
                            filtered_market[
                                "Date"
                            ].dt.date
                            <= end_date
                        )
                    ]
                )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.write(
        f"Showing **{len(filtered_market):,}** rows."
    )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    st.dataframe(
        filtered_market.tail(5000),
        use_container_width=True,
        height=600,
        hide_index=True,
    )

    if len(filtered_market) > 5000:

        st.caption(
            "Showing the latest 5,000 rows."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Financial Shock Propagation & Recovery Engine | "
    "Python • Pandas • Scikit-Learn • NetworkX • Streamlit"
)