
from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.propagation.shock_propagation import propagate_shock
from src.propagation.systemic_risk import systemic_risk
from src.recovery.scenario_simulator import simulate_market_shock
from src.recovery.recovery_prediction import recovery_days

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data" / "raw" / "market_data"

st.set_page_config(
    page_title="Financial Shock Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# PREMIUM 2.5D / LAYERED UI
# -----------------------------------------------------------------------------

st.markdown(
    r"""
    <style>
    :root {
        --bg: #050812;
        --panel: rgba(13, 19, 31, .82);
        --panel-2: rgba(18, 26, 42, .78);
        --line: rgba(153, 177, 219, .16);
        --muted: #8fa1bb;
        --text: #f4f7fb;
        --accent: #78a9ff;
        --accent-2: #8f7cff;
        --success: #57d18c;
        --danger: #ff6376;
    }

    .stApp {
        background:
            radial-gradient(900px 500px at 12% -10%, rgba(55, 119, 203, .18), transparent 60%),
            radial-gradient(700px 500px at 92% 4%, rgba(135, 76, 184, .16), transparent 60%),
            linear-gradient(180deg, #070b14 0%, #050812 70%, #04060d 100%);
        color: var(--text);
    }

    /* Remove Streamlit navigation chrome / left pane */
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stHeader"] { background: transparent; }
    header { background: transparent !important; }

    .block-container {
        max-width: 1480px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .topbar {
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding: 4px 0 18px 0;
        border-bottom: 1px solid rgba(255,255,255,.07);
        margin-bottom: 18px;
    }

    .brand { font-size: 15px; font-weight: 800; letter-spacing: -.01em; }
    .brand span { color: #78a9ff; }
    .status {
        display:inline-flex; align-items:center; gap:7px;
        color:#74e6a0; font-size:11px; font-weight:800; letter-spacing:.08em;
        padding:7px 10px; border-radius:999px;
        border:1px solid rgba(87,209,140,.25); background:rgba(87,209,140,.07);
    }
    .dot { width:7px; height:7px; border-radius:50%; background:#57d18c; box-shadow:0 0 12px rgba(87,209,140,.75); }

    .hero-wrap { position:relative; padding: 28px 0 26px; overflow:hidden; }
    .eyebrow { color:var(--accent); font-size:12px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }
    .hero-title { font-size:clamp(42px, 6vw, 82px); line-height:.97; letter-spacing:-.055em; max-width:980px; margin:10px 0 15px; color:#f7f9fc; }
    .hero-sub { max-width:850px; color:#9eacc0; font-size:17px; line-height:1.65; }
    .hero-orbit {
        position:absolute; right:-120px; top:-120px; width:520px; height:520px; border-radius:50%;
        border:1px solid rgba(120,169,255,.15); box-shadow:0 0 100px rgba(120,169,255,.08);
        transform:rotate(-14deg);
    }
    .hero-orbit::before, .hero-orbit::after { content:""; position:absolute; inset:38px; border-radius:50%; border:1px solid rgba(143,124,255,.14); }
    .hero-orbit::after { inset:100px; border-color:rgba(87,209,140,.12); }

    .layer-rail {
        display:grid; grid-template-columns:repeat(6, 1fr); gap:7px; margin: 5px 0 22px;
    }
    .layer-track {
        height:4px; border-radius:999px; background:rgba(255,255,255,.07); overflow:hidden;
    }
    .layer-track.active { background:linear-gradient(90deg, var(--accent), var(--accent-2)); box-shadow:0 0 18px rgba(120,169,255,.2); }
    .layer-label { margin-top:7px; color:#72819a; font-size:10px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; text-align:center; }
    .layer-label.active { color:#dce8ff; }

    .glass {
        background:linear-gradient(180deg, rgba(18,26,42,.78), rgba(9,14,24,.76));
        border:1px solid var(--line); border-radius:20px; padding:18px;
        box-shadow:0 18px 50px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.03);
        backdrop-filter:blur(12px);
    }
    .glass:hover { border-color:rgba(120,169,255,.26); box-shadow:0 24px 70px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.05); }
    .card-kicker { color:#7796c6; font-size:10px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
    .card-title { font-size:18px; font-weight:800; margin-top:6px; color:#eef3fb; }
    .card-copy { color:#8f9db2; font-size:13px; line-height:1.55; margin-top:6px; }

    [data-testid="stMetric"] {
        background:linear-gradient(180deg, rgba(18,26,42,.82), rgba(9,14,24,.82));
        border:1px solid rgba(153,177,219,.13); border-radius:16px; padding:15px 17px;
        box-shadow:0 12px 35px rgba(0,0,0,.16); min-height:96px;
    }
    [data-testid="stMetricLabel"] { color:#8596af; }
    [data-testid="stMetricValue"] { color:#f4f7fb; font-weight:800; }

    .stButton > button {
        width:100%; border-radius:12px !important; border:1px solid rgba(120,169,255,.18) !important;
        background:linear-gradient(180deg, rgba(28,44,70,.85), rgba(15,24,40,.85)) !important;
        color:#eff5ff !important; font-weight:750 !important; min-height:42px;
        transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }
    .stButton > button:hover { transform:translateY(-2px); border-color:rgba(120,169,255,.42) !important; box-shadow:0 10px 24px rgba(0,0,0,.24); }

    div[data-baseweb="select"] > div, .stSlider { border-radius:12px; }
    .section-title { font-size:26px; font-weight:800; letter-spacing:-.025em; margin:10px 0 2px; }
    .section-copy { color:#8c9ab0; margin:0 0 16px; }

    .next-banner {
        margin-top:22px; padding:16px 18px; border-radius:18px;
        border:1px solid rgba(120,169,255,.16); background:linear-gradient(90deg, rgba(30,54,91,.36), rgba(25,22,50,.28));
        color:#cdd9ec; font-size:13px;
    }

    .tiny { color:#72819a; font-size:11px; }
    footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# DATA
# -----------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_csv(filename: str):
    path = OUTPUT_DIR / filename
    return pd.read_csv(path) if path.exists() else None

@st.cache_data(show_spinner=False)
def load_correlation_matrix():
    path = OUTPUT_DIR / "correlation_matrix.csv"
    if not path.exists():
        return None
    matrix = pd.read_csv(path, index_col=0)
    matrix.index = matrix.index.astype(str)
    matrix.columns = matrix.columns.astype(str)
    return matrix.apply(pd.to_numeric, errors="coerce")

@st.cache_data(show_spinner=False)
def load_market_raw():
    path = DATA_DIR / "indian_stocks.csv"
    return pd.read_csv(path) if path.exists() else None

@st.cache_data(show_spinner=False)
def build_network_from_matrix(matrix: pd.DataFrame, threshold: float):
    G = nx.Graph()
    nodes = matrix.columns.tolist()
    G.add_nodes_from(nodes)
    for i, a in enumerate(nodes):
        for b in nodes[i+1:]:
            value = matrix.loc[a, b]
            if pd.notna(value) and abs(float(value)) >= threshold:
                G.add_edge(a, b, weight=float(value))
    return G

def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default

def plotly_dark_layout(fig, height=430, title=None):
    fig.update_layout(
        height=height,
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe4ef"),
        margin=dict(l=8, r=8, t=44 if title else 10, b=8),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#aebbd0")),
        hoverlabel=dict(bgcolor="#101827", font_color="#eef3fb", bordercolor="#30415c"),
    )
    return fig

def build_network_figure(G: nx.Graph, shock_state=None, selected_node=None):
    nodes = list(G.nodes())
    if not nodes:
        return go.Figure()
    pos = nx.spring_layout(G, seed=42, k=0.55, iterations=120)
    edges = []
    for a, b, attrs in G.edges(data=True):
        edges.append((a, b, attrs.get("weight", 0.0)))
    edge_x=[]; edge_y=[]; edge_width=[]
    for a,b,w in edges:
        edge_x += [pos[a][0], pos[b][0], None]
        edge_y += [pos[a][1], pos[b][1], None]
        edge_width.append(0.8 + 3.0*abs(w))
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1.1, color="rgba(111,143,190,.23)"), hoverinfo="none", showlegend=False)
    shocks={n:safe_float((shock_state or {}).get(n,0.0)) for n in nodes}
    marker_sizes=[10 + 20*min(1.0, shocks[n]) + (10 if n==selected_node else 0) for n in nodes]
    node_trace=go.Scatter(
        x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes], mode="markers+text", text=nodes,
        textposition="top center", textfont=dict(size=9, color="#cad7e9"),
        customdata=nodes,
        hovertemplate="<b>%{customdata}</b><br>Connections: %{marker.size}<extra></extra>",
        marker=dict(size=marker_sizes, color=[shocks[n] for n in nodes], colorscale=[[0,"#6fb5ff"],[.35,"#6fe0a1"],[.7,"#ffbf69"],[1,"#ff5f76"]], cmin=0, cmax=1, opacity=.95, line=dict(width=.6,color="rgba(255,255,255,.28)")),
        showlegend=False,
    )
    fig=go.Figure([edge_trace,node_trace])
    fig.update_layout(height=560, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), hovermode="closest")
    return fig

market_df=load_csv("processed_market_data.csv")
events_df=load_csv("shock_events.csv")
correlation_matrix=load_correlation_matrix()
propagation_df=load_csv("propagation_results.csv")
recovery_df=load_csv("recovery_results.csv")
raw_df=load_market_raw()

required={"processed_market_data.csv":market_df,"shock_events.csv":events_df,"correlation_matrix.csv":correlation_matrix,"propagation_results.csv":propagation_df,"recovery_results.csv":recovery_df}
missing=[k for k,v in required.items() if v is None]
if missing:
    st.error("Some engine outputs are missing.")
    st.code("python run_engine.py", language="powershell")
    st.write("Missing:", ", ".join(missing))
    st.stop()

# -----------------------------------------------------------------------------
# GLOBAL STATE / METRICS
# -----------------------------------------------------------------------------

layers=["Command Center","Shock Intelligence","Network Map","Shock Simulator","Recovery Lab","Market Explorer"]
if "layer" not in st.session_state:
    st.session_state.layer=0

# Navigation can be done by clicking a layer or with previous / next buttons.

def go_to(index:int):
    st.session_state.layer=max(0,min(len(layers)-1,index))

# -----------------------------------------------------------------------------
# HEADER + LAYER NAVIGATION
# -----------------------------------------------------------------------------

st.markdown(
    '<div class="topbar"><div class="brand">◈ <span>FINANCIAL SHOCK</span> / INTELLIGENCE ENGINE</div><div class="status"><span class="dot"></span> ENGINE ONLINE</div></div>',
    unsafe_allow_html=True,
)

rail_cols=st.columns(len(layers))
for i,(col,name) in enumerate(zip(rail_cols,layers)):
    with col:
        active="active" if i==st.session_state.layer else ""
        st.markdown(f'<div class="layer-track {active}"></div><div class="layer-label {active}">{i+1:02d} · {name}</div>', unsafe_allow_html=True)
        if st.button(f"Open {i+1:02d}", key=f"layer_btn_{i}"):
            go_to(i)
            st.rerun()

st.markdown('<div class="tiny">One dashboard · six interactive layers · use the chapter controls or Next to move through the system.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE RENDERERS
# -----------------------------------------------------------------------------

tickers=correlation_matrix.columns.tolist()
total_stocks=len(tickers)
trading_days=pd.to_datetime(market_df["Date"],errors="coerce").nunique() if "Date" in market_df.columns else 0
daily_rows=len(market_df)
total_events=len(events_df)
sector_map={}
if "ticker" in market_df.columns and "sector" in market_df.columns:
    tmp=market_df[["ticker","sector"]].dropna().drop_duplicates("ticker")
    sector_map=dict(zip(tmp["ticker"],tmp["sector"]))

def render_command_center():
    st.markdown('<div class="hero-wrap"><div class="hero-orbit"></div><div class="eyebrow">SYSTEMIC RISK INTELLIGENCE · LAYER 01</div><div class="hero-title">See the shock.<br>Track the contagion.<br>Measure the recovery.</div><div class="hero-sub">A network-based financial risk engine that detects abnormal market behavior, maps relationships between companies, simulates shock propagation, and estimates recovery trajectories.</div></div>', unsafe_allow_html=True)
    m1,m2,m3,m4,m5=st.columns(5)
    m1.metric("Stocks",f"{total_stocks:,}")
    m2.metric("Trading Days",f"{trading_days:,}")
    m3.metric("Observations",f"{daily_rows:,}")
    m4.metric("Shock Events",f"{total_events:,}")
    m5.metric("Network Nodes",f"{total_stocks:,}")
    st.markdown('<div class="section-title">System posture</div><div class="section-copy">A compact read of what the engine sees before you enter the deeper layers.</div>',unsafe_allow_html=True)
    left,right=st.columns([1.4,1])
    with left:
        if "shock_score" in market_df.columns:
            ts=market_df.groupby("Date",as_index=False)["shock_score"].mean().dropna()
            fig=go.Figure(go.Scatter(x=ts["Date"],y=ts["shock_score"],mode="lines",line=dict(width=2.6),fill="tozeroy",fillcolor="rgba(120,169,255,.08)"))
            plotly_dark_layout(fig,390,"Market Shock Intensity")
            fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="rgba(255,255,255,.05)")
            st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False,"scrollZoom":True})
    with right:
        latest=propagation_df.iloc[-1]
        st.markdown(f'<div class="glass"><div class="card-kicker">Propagation snapshot</div><div class="card-title">System state after the latest run</div><div class="card-copy">Final systemic risk <b>{latest["systemic_risk"]:.2f}</b><br>Affected nodes <b>{int(latest["affected_nodes"])}</b><br>Maximum shock <b>{latest["maximum_shock"]:.3f}</b></div></div>',unsafe_allow_html=True)
        top=events_df.nlargest(5,"peak_score")[["ticker","peak_date","peak_score","severity"]]
        st.dataframe(top,use_container_width=True,hide_index=True)
    flow=st.columns(6)
    for i,(col,label) in enumerate(zip(flow,["Market Data","Features","Shock Detection","Network","Propagation","Recovery"])):
        with col:
            st.markdown(f'<div class="glass"><div class="card-kicker">0{i+1}</div><div class="card-title">{label}</div><div class="card-copy">Layered engine stage</div></div>',unsafe_allow_html=True)

def render_shock_intelligence():
    st.markdown('<div class="section-title">Shock intelligence</div><div class="section-copy">Explore anomalies, event duration, and the strongest historical stress signals.</div>',unsafe_allow_html=True)
    c1,c2=st.columns([1,1.6])
    if "classification" in market_df.columns:
        counts=market_df["classification"].value_counts().rename_axis("classification").reset_index(name="count")
        with c1: st.dataframe(counts,use_container_width=True,hide_index=True)
        with c2:
            fig=go.Figure(go.Bar(x=counts["classification"],y=counts["count"],text=counts["count"],textposition="outside"))
            plotly_dark_layout(fig,370,"Event composition")
            fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="rgba(255,255,255,.05)")
            st.plotly_chart(fig,use_container_width=True)
    a,b,c=st.columns(3)
    sev=sorted(events_df["severity"].dropna().unique().tolist())
    selected_sev=a.multiselect("Severity",sev,default=sev)
    companies=sorted(events_df["ticker"].dropna().unique().tolist())
    selected_companies=b.multiselect("Companies",companies)
    dr=c.slider("Duration (days)",int(events_df["duration"].min()),int(events_df["duration"].max()),(int(events_df["duration"].min()),int(events_df["duration"].max())))
    filtered=events_df[events_df["severity"].isin(selected_sev)&events_df["duration"].between(dr[0],dr[1])].copy()
    if selected_companies: filtered=filtered[filtered["ticker"].isin(selected_companies)]
    st.markdown(f'<div class="tiny">Showing <b>{len(filtered):,}</b> events after filters.</div>',unsafe_allow_html=True)
    st.dataframe(filtered.sort_values(["peak_score","duration"],ascending=False),use_container_width=True,hide_index=True)

def render_network_map():
    st.markdown('<div class="section-title">Network map</div><div class="section-copy">A layered 2D network with depth cues — not a literal 3D scene. Hover, drag, zoom, and focus on a company.</div>',unsafe_allow_html=True)
    threshold=st.slider("Correlation threshold",0.30,0.90,0.60,0.05,key="network_threshold")
    G=build_network_from_matrix(correlation_matrix,threshold)
    a,b,c,d=st.columns(4)
    a.metric("Nodes",G.number_of_nodes()); b.metric("Edges",G.number_of_edges()); c.metric("Density",f"{nx.density(G):.4f}"); d.metric("Threshold",f"±{threshold:.2f}")
    selected=st.selectbox("Focus node",["None"]+sorted(G.nodes()),key="network_focus")
    selected_node=None if selected=="None" else selected
    max_degree=max(G.degree,key=lambda x:x[1]) if G.nodes else ("—",0)
    st.markdown(f'<div class="glass"><div class="card-kicker">Network reading</div><div class="card-title">{max_degree[0]} is the current hub</div><div class="card-copy">At this threshold it has <b>{max_degree[1]}</b> connections. Stronger thresholds make the network sparser and emphasize the tightest relationships.</div></div>',unsafe_allow_html=True)
    fig=build_network_figure(G,selected_node=selected_node)
    st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False,"scrollZoom":True})
    pairs=[]
    nodes=correlation_matrix.columns.tolist()
    for i,a1 in enumerate(nodes):
        for b1 in nodes[i+1:]:
            v=correlation_matrix.loc[a1,b1]
            if pd.notna(v): pairs.append({"Company A":a1,"Company B":b1,"Correlation":float(v)})
    pair_df=pd.DataFrame(pairs); pair_df["abs_c"]=pair_df["Correlation"].abs(); pair_df=pair_df.sort_values("abs_c",ascending=False).drop(columns="abs_c")
    st.dataframe(pair_df.head(20),use_container_width=True,hide_index=True)

def render_shock_simulator():
    st.markdown('<div class="section-title">Shock simulator</div><div class="section-copy">Inject a scenario, then inspect the cascade as a sequence of states rather than a disconnected collection of charts.</div>',unsafe_allow_html=True)
    t=st.slider("Network correlation threshold",0.30,0.90,0.60,0.05,key="sim_threshold")
    G=build_network_from_matrix(correlation_matrix,t)
    controls=st.columns(4)
    options=sorted(G.nodes())
    origin=controls[0].selectbox("Shock origin",options,index=options.index("PNB") if "PNB" in options else 0)
    severity=controls[1].slider("Initial shock",0.05,1.00,0.6767,0.01,format="%.2f")
    transmission=controls[2].slider("Transmission",0.01,0.80,0.15,0.01)
    recovery_rate=controls[3].slider("Natural recovery",0.01,0.80,0.15,0.01)
    steps=st.slider("Propagation steps",1,25,10)
    initial={n:0.0 for n in G.nodes()}; initial[origin]=severity
    history=propagate_shock(G,initial,recovery=recovery_rate,transmission=transmission,steps=steps)
    rows=[{"step":i,"systemic_risk":systemic_risk(state),"affected_nodes":sum(v>0.001 for v in state.values()),"maximum_shock":max(state.values()) if state else 0.0} for i,state in enumerate(history)]
    sim=pd.DataFrame(rows); final_state=history[-1]
    a,b,c,d=st.columns(4); a.metric("Origin",origin); b.metric("Final systemic risk",f"{sim.iloc[-1]["systemic_risk"]:.2f}"); c.metric("Affected nodes",int(sim.iloc[-1]["affected_nodes"])); d.metric("Max shock",f"{sim.iloc[-1]["maximum_shock"]:.3f}")
    fig=go.Figure(); fig.add_trace(go.Scatter(x=sim["step"],y=sim["systemic_risk"],mode="lines+markers",name="Systemic risk",line=dict(width=2.5))); fig.add_trace(go.Scatter(x=sim["step"],y=sim["affected_nodes"],mode="lines+markers",name="Affected nodes",yaxis="y2",line=dict(width=2,dash="dot"))); fig.update_layout(yaxis=dict(title="Systemic risk"),yaxis2=dict(title="Affected nodes",overlaying="y",side="right",showgrid=False)); plotly_dark_layout(fig,390,"Propagation timeline"); st.plotly_chart(fig,use_container_width=True)
    left,right=st.columns([1.2,1])
    with left:
        st.plotly_chart(build_network_figure(G,shock_state=final_state,selected_node=origin),use_container_width=True,config={"displaylogo":False,"scrollZoom":True})
    with right:
        ranked=pd.Series(final_state,name="shock").sort_values(ascending=False).head(12).reset_index().rename(columns={"index":"ticker"}); ranked["shock"]=ranked["shock"].round(4); st.dataframe(ranked,use_container_width=True,hide_index=True)

def render_recovery_lab():
    st.markdown('<div class="section-title">Recovery lab</div><div class="section-copy">Change the size of the shock and recovery speed to see how the trajectory bends over time.</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3); shock_pct=a.slider("Shock size",-0.90,-0.05,-0.6767,0.01,format="%.2f"); days=b.slider("Simulation days",30,365,180); daily_recovery=c.slider("Daily recovery rate",0.01,0.40,0.10,0.01)
    path=simulate_market_shock(base_return=0.0,shock_pct=shock_pct,days=days,daily_recovery=daily_recovery); rec=pd.DataFrame(path,columns=["day","portfolio_value"]); rday=recovery_days(rec.itertuples(index=False,name=None),target=0.99)
    m1,m2,m3=st.columns(3); m1.metric("Initial value",f"{rec.iloc[0]['portfolio_value']:.3f}"); m2.metric("Final value",f"{rec.iloc[-1]['portfolio_value']:.3f}"); m3.metric("Recovery to 99%",f"Day {rday}" if rday is not None else "Not reached")
    fig=go.Figure(go.Scatter(x=rec["day"],y=rec["portfolio_value"],mode="lines",line=dict(width=3),name="Portfolio value")); fig.add_hline(y=.99,line_dash="dash",annotation_text="99% recovery target"); plotly_dark_layout(fig,470,"Recovery curve"); fig.update_xaxes(title="Day",showgrid=False); fig.update_yaxes(title="Normalized value",gridcolor="rgba(255,255,255,.05)"); st.plotly_chart(fig,use_container_width=True)

def render_market_explorer():
    st.markdown('<div class="section-title">Market explorer</div><div class="section-copy">Move from the system view to one company and inspect its stress profile and strongest relationships.</div>',unsafe_allow_html=True)
    company=st.selectbox("Company",sorted(tickers),key="market_company")
    if "Date" in market_df.columns and "shock_score" in market_df.columns:
        company_df=market_df[market_df["ticker"]==company].copy().sort_values("Date")
        fig=go.Figure(go.Scatter(x=company_df["Date"],y=company_df["shock_score"],mode="lines",line=dict(width=2.5),name="Shock score")); plotly_dark_layout(fig,390,f"{company} · shock timeline"); fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="rgba(255,255,255,.05)"); st.plotly_chart(fig,use_container_width=True)
        clean=company_df.dropna(subset=["shock_score"])
        if not clean.empty:
            last=clean.iloc[-1]; a,b,c=st.columns(3); a.metric("Latest shock score",f"{last['shock_score']:.2f}"); b.metric("Classification",str(last["classification"])); c.metric("Sector",str(last.get("sector","Unknown")))
    st.markdown('<div class="section-title" style="font-size:20px">Correlation profile</div>',unsafe_allow_html=True)
    corr=correlation_matrix[company].drop(labels=[company],errors="ignore").sort_values(key=lambda s:s.abs(),ascending=False).head(15).reset_index(); corr.columns=["Company","Correlation"]; st.dataframe(corr,use_container_width=True,hide_index=True)
    st.markdown('<div class="section-title" style="font-size:20px">Relevant shock events</div>',unsafe_allow_html=True)
    st.dataframe(events_df[events_df["ticker"]==company].sort_values("peak_score",ascending=False).head(20),use_container_width=True,hide_index=True)

renderers=[render_command_center,render_shock_intelligence,render_network_map,render_shock_simulator,render_recovery_lab,render_market_explorer]
renderers[st.session_state.layer]()

# -----------------------------------------------------------------------------
# STORY NAVIGATION
# -----------------------------------------------------------------------------

current=st.session_state.layer
st.markdown('<div class="next-banner">Layered website mode: the interface uses depth, gradients, soft glass panels, perspective cues, and scroll-like chapter progression — the visual language of modern 3D web design without turning the financial dashboard into a literal 3D scene.</div>',unsafe_allow_html=True)
prev_col,next_col=st.columns([1,1])
with prev_col:
    if st.button("← Previous layer",disabled=current==0,key="prev_layer"):
        go_to(current-1); st.rerun()
with next_col:
    if st.button("Next layer →",disabled=current==len(layers)-1,key="next_layer"):
        go_to(current+1); st.rerun()

st.markdown('<div class="tiny" style="text-align:center;margin-top:10px">Educational / research system · Historical simulation only · Not financial advice</div>',unsafe_allow_html=True)
