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
# PATHS
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
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .metric-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 700;
    }

    .metric-label {
        font-size: 14px;
        color: #777;
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
        st.error(f"Could not load {filename}: {e}")
        return None


def find_column(df, possible_names):
    """
    Find a column using case-insensitive matching.
    """
    if df is None:
        return None

    lower_map = {
        str(col).lower(): col
        for col in df.columns
    }

    for name in possible_names:
        if name.lower() in lower_map:
            return lower_map[name.lower()]

    return None


def format_number(value, decimals=2):
    if value is None:
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"
    except Exception:
        return str(value)


# ============================================================
# LOAD OUTPUT DATA
# ============================================================

market_df = load_csv("processed_market_data.csv")
events_df = load_csv("shock_events.csv")
correlation_df = load_csv("correlation_matrix.csv")
propagation_df = load_csv("propagation_results.csv")
recovery_df = load_csv("recovery_results.csv")


# ============================================================
# CHECK OUTPUTS
# ============================================================

missing_files = []

for filename, dataframe in [
    ("processed_market_data.csv", market_df),
    ("shock_events.csv", events_df),
    ("correlation_matrix.csv", correlation_df),
    ("propagation_results.csv", propagation_df),
    ("recovery_results.csv", recovery_df),
]:
    if dataframe is None:
        missing_files.append(filename)


if missing_files:

    st.warning(
        "Some engine output files are missing."
    )

    st.write("Missing files:")

    for file in missing_files:
        st.write(f"- `{file}`")

    st.info(
        "Run `python .\\run_engine.py` first, then refresh this dashboard."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Dashboard Controls")

st.sidebar.markdown("---")

st.sidebar.subheader("Navigation")

page = st.sidebar.radio(
    "Select View",
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

st.sidebar.info(
    """
    **Financial Shock Propagation & Recovery Engine**

    Pipeline:

    Market Data
    ↓
    Feature Engineering
    ↓
    Shock Detection
    ↓
    Event Detection
    ↓
    Correlation Network
    ↓
    Shock Propagation
    ↓
    Recovery Simulation
    """
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">System Overview</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # BASIC METRICS
    # --------------------------------------------------------

    daily_rows = len(market_df)

    if "ticker" in market_df.columns:
        stocks = market_df["ticker"].nunique()
    else:
        stocks = "N/A"

    if "Date" in market_df.columns:
        dates = pd.to_datetime(
            market_df["Date"],
            errors="coerce",
        )

        trading_days = dates.nunique()
    else:
        trading_days = "N/A"

    shock_events = len(events_df)

    network_nodes = stocks

    if propagation_df is not None:
        if "ticker" in propagation_df.columns:
            network_nodes = propagation_df["ticker"].nunique()
        elif "node" in propagation_df.columns:
            network_nodes = propagation_df["node"].nunique()

    # --------------------------------------------------------
    # METRIC ROW
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Market Stocks",
        stocks,
    )

    col2.metric(
        "Trading Days",
        f"{trading_days:,}"
        if isinstance(trading_days, int)
        else trading_days,
    )

    col3.metric(
        "Daily Observations",
        f"{daily_rows:,}",
    )

    col4.metric(
        "Shock Events",
        f"{shock_events:,}",
    )

    col5.metric(
        "Network Nodes",
        network_nodes,
    )

    st.markdown("---")

    # --------------------------------------------------------
    # ENGINE STATUS
    # --------------------------------------------------------

    st.subheader("✅ Engine Status")

    status_cols = st.columns(4)

    status_cols[0].success("Market Data Loaded")

    status_cols[1].success("Shock Detection Complete")

    status_cols[2].success("Network Analysis Complete")

    status_cols[3].success("Recovery Analysis Complete")

    # --------------------------------------------------------
    # SHOCK DISTRIBUTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Shock Classification</div>',
        unsafe_allow_html=True,
    )

    classification_col = find_column(
        market_df,
        ["classification"],
    )

    if classification_col:

        classification_counts = (
            market_df[classification_col]
            .value_counts()
            .rename_axis("classification")
            .reset_index(name="count")
        )

        c1, c2 = st.columns([1, 2])

        with c1:
            st.dataframe(
                classification_counts,
                use_container_width=True,
                hide_index=True,
            )

        with c2:
            st.bar_chart(
                classification_counts.set_index(
                    "classification"
                )
            )

    # --------------------------------------------------------
    # TOP SHOCK EVENTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Top Persistent Shock Events</div>',
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
# SHOCK EVENTS
# ============================================================

elif page == "🚨 Shock Events":

    st.markdown(
        '<div class="section-title">🚨 Shock Event Detection</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Detected financial stress and shock events across the market."
    )

    # --------------------------------------------------------
    # SEVERITY DISTRIBUTION
    # --------------------------------------------------------

    if "severity" in events_df.columns:

        severity_counts = (
            events_df["severity"]
            .value_counts()
            .rename_axis("severity")
            .reset_index(name="events")
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Event Severity")

            st.dataframe(
                severity_counts,
                use_container_width=True,
                hide_index=True,
            )

        with col2:

            st.subheader("Severity Chart")

            st.bar_chart(
                severity_counts.set_index(
                    "severity"
                )
            )

    # --------------------------------------------------------
    # EVENT FILTER
    # --------------------------------------------------------

    st.subheader("Event Explorer")

    filtered_events = events_df.copy()

    if "severity" in events_df.columns:

        severities = sorted(
            events_df["severity"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_severity = st.multiselect(
            "Filter by severity",
            severities,
            default=severities,
        )

        filtered_events = filtered_events[
            filtered_events["severity"].isin(
                selected_severity
            )
        ]

    if "ticker" in events_df.columns:

        tickers = sorted(
            events_df["ticker"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_tickers = st.multiselect(
            "Filter by company",
            tickers,
            default=[],
            placeholder="All companies",
        )

        if selected_tickers:

            filtered_events = filtered_events[
                filtered_events["ticker"].isin(
                    selected_tickers
                )
            ]

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
# CORRELATION NETWORK
# ============================================================

elif page == "🌐 Correlation Network":

    st.markdown(
        '<div class="section-title">🌐 Financial Correlation Network</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "The correlation network identifies companies whose "
        "daily returns move together."
    )

    # --------------------------------------------------------
    # NETWORK METRICS
    # --------------------------------------------------------

    network_edges = 10

    if correlation_df is not None:

        if {
            "ticker_a",
            "ticker_b",
        }.issubset(correlation_df.columns):

            network_edges = len(correlation_df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Network Nodes",
        stocks,
    )

    col2.metric(
        "Network Edges",
        network_edges,
    )

    if stocks and isinstance(stocks, int) and stocks > 1:

        density = (
            2 * network_edges
            / (stocks * (stocks - 1))
        )

    else:
        density = 0

    col3.metric(
        "Network Density",
        f"{density:.6f}",
    )

    # --------------------------------------------------------
    # NETWORK IMAGE
    # --------------------------------------------------------

    network_image = (
        OUTPUT_DIR / "correlation_network.png"
    )

    if network_image.exists():

        st.subheader("Correlation Network")

        st.image(
            str(network_image),
            use_container_width=True,
        )

    # --------------------------------------------------------
    # CORRELATION TABLE
    # --------------------------------------------------------

    st.subheader("Strongest Correlations")

    if {
        "ticker_a",
        "ticker_b",
        "correlation",
    }.issubset(correlation_df.columns):

        correlations = correlation_df.copy()

        correlations["abs_corr"] = (
            correlations["correlation"]
            .abs()
        )

        correlations = (
            correlations
            .sort_values(
                "abs_corr",
                ascending=False,
            )
            .drop(
                columns=["abs_corr"]
            )
            .head(30)
        )

        st.dataframe(
            correlations,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.dataframe(
            correlation_df.head(50),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# SHOCK PROPAGATION
# ============================================================

elif page == "💥 Shock Propagation":

    st.markdown(
        '<div class="section-title">💥 Shock Propagation Analysis</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "This section shows how a financial shock propagates "
        "through the correlation network."
    )

    # --------------------------------------------------------
    # PROPAGATION IMAGE
    # --------------------------------------------------------

    propagation_image = (
        OUTPUT_DIR / "propagation_results.png"
    )

    # --------------------------------------------------------
    # DETECT COLUMNS
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
    # METRICS
    # --------------------------------------------------------

    if risk_col:

        final_risk = propagation_df[
            risk_col
        ].iloc[-1]

    else:

        final_risk = None

    if maximum_col:

        final_maximum = propagation_df[
            maximum_col
        ].iloc[-1]

    else:

        final_maximum = None

    if affected_col:

        final_affected = propagation_df[
            affected_col
        ].iloc[-1]

    else:

        final_affected = None

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Final Systemic Risk",
        format_number(final_risk, 4),
    )

    c2.metric(
        "Final Maximum Shock",
        format_number(final_maximum, 4),
    )

    c3.metric(
        "Affected Nodes",
        format_number(final_affected, 0),
    )

    # --------------------------------------------------------
    # SYSTEMIC RISK CHART
    # --------------------------------------------------------

    if step_col and risk_col:

        st.subheader("Systemic Risk Over Time")

        chart_df = propagation_df[
            [step_col, risk_col]
        ].copy()

        chart_df = chart_df.set_index(
            step_col
        )

        st.line_chart(
            chart_df
        )

    # --------------------------------------------------------
    # AFFECTED NODES
    # --------------------------------------------------------

    if step_col and affected_col:

        st.subheader(
            "Number of Affected Companies"
        )

        affected_df = propagation_df[
            [step_col, affected_col]
        ].copy()

        affected_df = affected_df.set_index(
            step_col
        )

        st.line_chart(
            affected_df
        )

    # --------------------------------------------------------
    # MAXIMUM SHOCK
    # --------------------------------------------------------

    if step_col and maximum_col:

        st.subheader(
            "Maximum Propagated Shock"
        )

        max_df = propagation_df[
            [step_col, maximum_col]
        ].copy()

        max_df = max_df.set_index(
            step_col
        )

        st.line_chart(
            max_df
        )

    # --------------------------------------------------------
    # RAW PROPAGATION DATA
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
# RECOVERY ANALYSIS
# ============================================================

elif page == "🔄 Recovery Analysis":

    st.markdown(
        '<div class="section-title">🔄 Recovery Simulation</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Portfolio recovery following a financial shock."
    )

    # --------------------------------------------------------
    # RECOVERY COLUMNS
    # --------------------------------------------------------

    day_col = find_column(
        recovery_df,
        ["day", "days"],
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
    # METRICS
    # --------------------------------------------------------

    if value_col:

        initial_value = recovery_df[
            value_col
        ].iloc[0]

        final_value = recovery_df[
            value_col
        ].iloc[-1]

    else:

        initial_value = None
        final_value = None

    recovery_day = None

    if value_col and day_col:

        recovered = recovery_df[
            recovery_df[value_col] >= 0.99
        ]

        if not recovered.empty:

            recovery_day = int(
                recovered.iloc[0][day_col]
            )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Initial Portfolio Value",
        format_number(initial_value, 4),
    )

    c2.metric(
        "Final Portfolio Value",
        format_number(final_value, 4),
    )

    c3.metric(
        "Recovery to 99%",
        f"Day {recovery_day}"
        if recovery_day is not None
        else "Not reached",
    )

    # --------------------------------------------------------
    # RECOVERY CURVE
    # --------------------------------------------------------

    recovery_image = (
        OUTPUT_DIR / "recovery_curve.png"
    )

    if recovery_image.exists():

        st.subheader(
            "Recovery Curve"
        )

        st.image(
            str(recovery_image),
            use_container_width=True,
        )

    elif day_col and value_col:

        st.subheader(
            "Recovery Curve"
        )

        chart_df = recovery_df[
            [day_col, value_col]
        ].copy()

        chart_df = chart_df.set_index(
            day_col
        )

        st.line_chart(
            chart_df
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
# MARKET DATA
# ============================================================

elif page == "📊 Market Data":

    st.markdown(
        '<div class="section-title">📊 Processed Market Data</div>',
        unsafe_allow_html=True,
    )

    st.write(
        f"Total observations: **{len(market_df):,}**"
    )

    # --------------------------------------------------------
    # COMPANY FILTER
    # --------------------------------------------------------

    filtered_market = market_df.copy()

    if "ticker" in market_df.columns:

        tickers = sorted(
            market_df["ticker"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_ticker = st.selectbox(
            "Select company",
            ["All"] + tickers,
        )

        if selected_ticker != "All":

            filtered_market = market_df[
                market_df["ticker"]
                == selected_ticker
            ]

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    if "Date" in filtered_market.columns:

        filtered_market = filtered_market.copy()

        filtered_market["Date"] = pd.to_datetime(
            filtered_market["Date"],
            errors="coerce",
        )

        valid_dates = filtered_market[
            "Date"
        ].dropna()

        if not valid_dates.empty:

            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            date_range = st.date_input(
                "Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )

            if (
                isinstance(date_range, tuple)
                and len(date_range) == 2
            ):

                start_date, end_date = date_range

                filtered_market = filtered_market[
                    (
                        filtered_market["Date"].dt.date
                        >= start_date
                    )
                    &
                    (
                        filtered_market["Date"].dt.date
                        <= end_date
                    )
                ]

    # --------------------------------------------------------
    # DATA TABLE
    # --------------------------------------------------------

    st.write(
        f"Showing **{len(filtered_market):,}** rows."
    )

    st.dataframe(
        filtered_market.tail(5000),
        use_container_width=True,
        height=600,
        hide_index=True,
    )

    st.caption(
        "Showing the latest 5,000 rows when the filtered dataset is larger."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Financial Shock Propagation & Recovery Engine • "
    "Built with Python, Pandas, Scikit-Learn, NetworkX and Streamlit"
)