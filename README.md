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

### 🚀 <a href="https://financial-shock-propagation-recovery-engine.streamlit.app/">LIVE DEMO →</a>

</p>

---

## 🌐 Live Demo

### 🚀 Explore the deployed application

**[Financial Shock Propagation & Recovery Engine — Live Demo](https://financial-shock-propagation-recovery-engine.streamlit.app/)**

The application is deployed using **Streamlit** and provides an interactive environment for exploring:

* 📊 Financial market behavior
* 🚨 Shock detection
* 🤖 Anomaly detection
* 🌐 Correlation networks
* 💥 Shock propagation
* ⚠️ Systemic-risk analysis
* 🔄 Recovery simulation
* 📈 Interactive financial visualizations

> **Try the live application:**
> https://financial-shock-propagation-recovery-engine.streamlit.app/

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
* 🔄 Recovery simulation
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

---

# 💥 Shock Propagation

The propagation engine models how a shock can move through the financial network.

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

<a href="https://financial-shock-p
