# ⚡ Financial Shock Propagation & Recovery Engine

### AI-Powered Systemic Risk Detection, Propagation Analysis & Recovery Simulation

<p align="center">

**Detect financial shocks. Measure their severity. Understand how they propagate. Simulate recovery.**

</p>

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikit-learn\&logoColor=white)](https://scikit-learn.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Network%20Analysis-4C78A8)](https://networkx.org/)
[![Tests](https://img.shields.io/badge/Tests-4%2F4%20Passing-2EA44F)](#testing)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

</p>

<p align="center">

### 🚀 <a href="YOUR_DEPLOYED_APP_LINK">LIVE DEMO →</a>

</p>

---

## 🧠 What Is This?

Financial markets are not isolated systems.

A major shock affecting one company, sector, or asset can spread through correlations and interconnected market relationships, creating a chain reaction across the financial system.

The **Financial Shock Propagation & Recovery Engine** is an AI/ML-powered analytical platform designed to study this process.

Instead of simply asking:

> **"Which stocks are falling?"**

the system asks:

> **"How severe is the shock, where can it propagate, which assets are most exposed, and how might the system recover?"**

The platform combines:

* 📊 Financial time-series analysis
* 🤖 Machine learning
* 🚨 Anomaly detection
* 🌐 Financial correlation networks
* 💥 Shock propagation simulation
* 📈 Systemic-risk analysis
* 🔮 Recovery simulation
* 🖥️ Interactive analytics dashboard

---

# 🎯 Core Intelligence Pipeline

```text
                 ┌─────────────────────┐
                 │   Financial Data    │
                 │  Market Time Series │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Feature Engineering │
                 │ Returns / Volatility│
                 │ Drawdown / Momentum │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Shock Detection   │
                 │   ML + Statistical  │
                 │      Analysis       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Shock Measurement  │
                 │ Severity / Exposure │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Correlation Network │
                 │  Asset Connections  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Shock Propagation   │
                 │   Simulation Engine  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Systemic Risk       │
                 │   Assessment        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Recovery Simulation │
                 │ Scenario Analysis   │
                 └─────────────────────┘
```

---

# 🔥 The Problem

Traditional market dashboards mainly provide:

* Stock prices
* Returns
* Charts
* Technical indicators
* Basic volatility measurements

But systemic financial risk requires understanding **relationships between assets**, not just individual price movements.

A shock can:

1. Begin in one asset.
2. Affect strongly correlated assets.
3. Spread across sectors.
4. Increase market-wide volatility.
5. Create secondary shocks.
6. Increase systemic risk.

This project attempts to model that chain.

---

# 💡 Our Approach

The system follows a six-stage intelligence framework:

## 1️⃣ Detect

Identify unusual financial behavior using statistical analysis and machine-learning-based anomaly detection.

## 2️⃣ Measure

Quantify the intensity of the detected shock using market features such as:

* Returns
* Volatility
* Drawdown
* Momentum
* Anomaly score

## 3️⃣ Connect

Construct a financial network where:

```text
Nodes  → Financial assets
Edges  → Significant relationships
Weights → Strength of correlation
```

This allows the system to understand how assets are interconnected.

## 4️⃣ Propagate

Simulate how a shock originating from one asset could influence connected assets.

The propagation process considers:

* Relationship strength
* Shock intensity
* Network connectivity
* Exposure to affected nodes

## 5️⃣ Assess

Estimate the broader systemic impact using network-level risk indicators.

The system helps identify:

* Highly exposed assets
* Highly connected nodes
* Potential contagion paths
* Systemically important positions

## 6️⃣ Recover

Simulate possible recovery trajectories after the shock.

This allows users to explore:

> **What could happen after the initial financial shock?**

---

# 🤖 Machine Learning

The project incorporates machine learning into the financial-risk pipeline.

### Anomaly Detection

**Isolation Forest** is used to identify observations that behave differently from normal market conditions.

Conceptually:

```text
Normal Market Behavior
        │
        ├── Normal
        ├── Normal
        ├── Normal
        │
        └── 🚨 Anomalous Event
```

Anomalies can then be investigated as potential shock events.

---

# 🌐 Financial Network Engine

One of the major components of the project is the **financial correlation network**.

Each asset becomes a node:

```text
        Asset A
        /     \
       /       \
   Asset B ─── Asset C
      |           |
      |           |
   Asset D ─── Asset E
```

Strong relationships create stronger edges.

This transforms financial data from a simple table into an interconnected system.

### Why this matters

Two assets may appear relatively stable individually while being highly connected to a shocked asset.

Network analysis makes those relationships visible.

---

# 💥 Shock Propagation

The propagation engine models how a shock can move through the financial network.

Example:

```text
Initial Shock
     │
     ▼
  Asset A
   /   \
  ▼     ▼
 B       C
 │       │
 ▼       ▼
 D ───── E
     │
     ▼
Systemic Impact
```

The engine can be used to investigate:

* Initial shock source
* Propagation paths
* Exposure levels
* Secondary affected assets
* Network-wide impact

---

# 🔄 Recovery Simulation

The system does not stop at identifying damage.

It also models the **recovery phase**.

```text
Shock
  │
  ▼
Impact
  │
  ▼
Maximum Stress
  │
  ▼
Recovery
  │
  ▼
Stabilization
```

Recovery analysis can help visualize how different assets or network states behave after a shock.

---

# 📊 Dataset

The current analysis pipeline works with a large historical market dataset covering:

| Metric             |       Value |
| ------------------ | ----------: |
| Assets             |      **50** |
| Trading Days       |   **4,111** |
| Daily Observations | **199,820** |

The dataset is transformed into machine-learning and network-analysis features before entering the intelligence pipeline.

---

# 🖥️ Interactive Dashboard

The project includes an interactive **Streamlit dashboard** designed to make complex financial-risk analysis understandable.

### Dashboard capabilities

* 📊 Market overview
* 🚨 Shock detection
* 📈 Asset-level analysis
* 🌐 Correlation network visualization
* 💥 Shock propagation
* ⚠️ Systemic-risk analysis
* 🔄 Recovery simulation
* 📉 Historical market behavior
* 🔍 Interactive filtering

### 🚀 Try It Live

<p align="center">

<a href="YOUR_DEPLOYED_APP_LINK">

<img src="https://img.shields.io/badge/🚀%20OPEN%20LIVE%20DASHBOARD-FF4B4B?style=for-the-badge" />

</a>

</p>

---

# 🏗️ Project Architecture

```text
Financial-Shock-Propagation-Recovery-Engine/
│
├── 📁 data/
│   ├── raw/
│   └── processed/
│
├── 📁 models/
│   └── trained_models/
│
├── 📁 src/
│   ├── data_processing/
│   ├── feature_engineering/
│   ├── anomaly_detection/
│   ├── shock_detection/
│   ├── network_analysis/
│   ├── propagation/
│   └── recovery/
│
├── 📁 tests/
│
├── 📄 dashboard.py
├── 📄 requirements.txt
├── 📄 README.md
└── 📄 LICENSE
```

> Folder names may differ slightly from the current implementation; update this tree if your repository structure has changed.

---

# 🧩 Technology Stack

| Technology             | Purpose                    |
| ---------------------- | -------------------------- |
| 🐍 Python              | Core development           |
| 🧠 Scikit-learn        | Machine learning           |
| 🌲 NetworkX            | Financial network analysis |
| 📊 Pandas              | Data processing            |
| 🔢 NumPy               | Numerical computation      |
| 📈 Matplotlib / Plotly | Visualization              |
| 🖥️ Streamlit          | Interactive dashboard      |
| 🧪 Pytest              | Testing                    |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/rawat4113/Financial-Shock-Propagation-Recovery-Engine.git
```

```bash
cd Financial-Shock-Propagation-Recovery-Engine
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Dashboard

```bash
streamlit run dashboard.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🧪 Testing

The project includes automated tests for validating important components of the analytical pipeline.

Run:

```bash
pytest
```

Current test status:

```text
4 / 4 Tests Passing ✅
```

---

# 📈 Example Analytical Workflow

A typical analysis can follow this sequence:

### Step 1 — Select a market period

Choose the historical period to analyze.

### Step 2 — Detect abnormal behavior

The anomaly-detection layer identifies unusual observations.

### Step 3 — Quantify the shock

Calculate the severity and characteristics of the event.

### Step 4 — Build the network

Generate relationships between assets.

### Step 5 — Simulate propagation

Select a shocked asset and analyze possible propagation through connected assets.

### Step 6 — Examine systemic impact

Identify highly exposed or highly connected nodes.

### Step 7 — Simulate recovery

Analyze potential stabilization and recovery behavior.

---

# 🧠 Key Concepts

The project combines several important concepts from modern financial analytics:

### Time-Series Analysis

Understanding how financial variables evolve over time.

### Anomaly Detection

Identifying observations that deviate significantly from normal behavior.

### Graph Theory

Representing financial relationships as networks.

### Network Contagion

Studying how disturbances can spread through connected systems.

### Systemic Risk

Understanding risk that emerges from interactions across the entire network rather than from one asset alone.

### Scenario Simulation

Testing hypothetical shock and recovery situations.

---

# 🎯 Why This Project Is Different

Most beginner financial projects stop at:

```text
Data → Prediction → Price
```

This project goes further:

```text
Data
 ↓
Detect
 ↓
Measure
 ↓
Connect
 ↓
Propagate
 ↓
Assess
 ↓
Recover
```

The objective is therefore not simply to predict whether a stock price will rise or fall.

It is to understand the **structure and dynamics of financial shocks**.

---

# 🔬 Potential Applications

The framework can potentially support research and analysis in areas such as:

* Financial risk management
* Portfolio stress testing
* Systemic-risk research
* Market surveillance
* Contagion analysis
* Financial scenario planning
* Academic research
* Quantitative finance

The outputs are analytical simulations and should not be interpreted as guaranteed predictions of future market behavior.

---

# 🚧 Limitations

Financial markets are complex adaptive systems, and historical relationships do not guarantee future behavior.

Important limitations include:

* Correlation does not necessarily imply causation.
* Historical patterns may change during extreme events.
* Simulated propagation is dependent on model assumptions.
* Recovery behavior is scenario-dependent.
* Market data can contain noise and structural breaks.
* The system is intended for analytical and research purposes, not financial advice.

---

# 🔮 Future Roadmap

The project can be extended toward a more advanced real-time financial-risk platform.

### Phase 1 — Advanced ML

* XGBoost / LightGBM
* Temporal models
* LSTM / Transformer architectures
* Ensemble anomaly detection

### Phase 2 — Real-Time Intelligence

```text
Live Market Data
       ↓
Streaming Feature Engine
       ↓
Real-Time Shock Detection
       ↓
Dynamic Network Update
       ↓
Propagation Engine
       ↓
Risk Alerts
```

### Phase 3 — Advanced Network Intelligence

* Dynamic correlation networks
* Community detection
* Centrality-based systemic-risk analysis
* Temporal graph analysis
* Graph Neural Networks

### Phase 4 — Decision Intelligence

Potential future capabilities:

* Automated risk alerts
* Scenario comparison
* Portfolio stress testing
* Explainable AI
* Risk reports
* API-based integration

---

# 📚 Research Direction

This project provides a foundation for exploring the intersection of:

```text
Artificial Intelligence
        +
Financial Markets
        +
Graph Theory
        +
Anomaly Detection
        +
Systemic Risk
        +
Simulation
```

It can therefore serve as a foundation for further research into **AI-driven financial contagion and systemic-risk modeling**.

---

# 👨‍💻 Author

### Ritesh Rawat

B.Tech Information Technology
AI / Data Science / Machine Learning Enthusiast

GitHub:
https://github.com/rawat4113

---

# ⭐ Support the Project

If you find this project useful or interesting:

⭐ Star the repository
🍴 Fork the project
🐛 Report issues
💡 Suggest improvements
🤝 Contribute

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

<p align="center">

## ⚡ Detect. Measure. Propagate. Recover.

### Building AI systems for understanding financial shocks.

</p>
