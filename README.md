# 📈 Financial Shock Propagation & Recovery Engine

> An end-to-end financial intelligence system for detecting market shocks, identifying anomalies, modeling financial contagion across correlated companies, measuring systemic risk, and simulating recovery scenarios.

---

## 🏆 Hackathon Project

**Project:** Financial Shock Propagation & Recovery Engine  
**Domain:** Financial Intelligence / Data Science / Machine Learning / Network Analysis  
**Built With:** Python, Pandas, NumPy, Scikit-learn, NetworkX, Matplotlib, Streamlit  
**Dataset:** Indian stock market historical data  
**Stocks Analyzed:** 50  
**Trading Days:** 4,111  
**Daily Observations:** 199,820

---

## 🎯 Problem Statement

Traditional financial analysis often evaluates companies independently.

However, financial shocks rarely remain isolated.

A major shock affecting one company or sector can spread through correlated companies and create broader systemic risk.

For example:

```text
                 MARKET SHOCK
                      │
                      ▼
                     PNB
                  ╱   │   ╲
                 ▼    ▼    ▼
              CANBK  SBIN  BANKBARODA
                 │     │      │
                 └─────┼──────┘
                       ▼
                 ICICIBANK
                       │
                       ▼
                   AXISBANK
```

The objective of this project is to build an intelligent engine that can:

- Detect abnormal market behavior
- Quantify financial shock severity
- Identify persistent shock events
- Construct a financial correlation network
- Simulate shock propagation
- Measure systemic risk
- Estimate recovery time
- Visualize the complete shock lifecycle

---

## 💡 Solution

The Financial Shock Propagation & Recovery Engine combines:

```text
Market Data
    │
    ▼
Data Preprocessing
    │
    ▼
Feature Engineering
    │
    ├── Daily Returns
    ├── Volatility
    ├── Drawdown
    └── Rolling Z-Score
    │
    ▼
Shock Score
    │
    ▼
Isolation Forest
    │
    ▼
Shock Classification
    │
    ▼
Shock Event Detection
    │
    ▼
Correlation Network
    │
    ▼
Shock Propagation
    │
    ▼
Systemic Risk
    │
    ▼
Recovery Simulation
    │
    ▼
Interactive Streamlit Dashboard
```

---

# 🚀 Key Features

## 1. Market Data Processing

The engine processes historical stock market data and standardizes:

- Dates
- Tickers
- Numerical features
- Duplicate records
- Missing values

### Current Dataset

| Metric | Value |
|---|---:|
| Stocks | 50 |
| Trading Days | 4,111 |
| Daily Observations | 199,820 |

---

## 📊 2. Market Feature Engineering

The system generates important financial risk features.

### Daily Return

Measures the percentage change in stock price.

```text
Return(t) = Price(t) / Price(t-1) - 1
```

### Rolling Volatility

Measures recent market instability using a 20-day rolling window.

### Drawdown

Measures the decline from the historical running maximum.

### Rolling Z-Score

Detects unusually large movements relative to recent behavior.

---

## ⚡ 3. Shock Score

A combined shock score is generated using:

```text
Return Z-Score
        +
Volatility
        +
Drawdown
        ↓
   Shock Score
```

The score is normalized to a practical range for risk classification.

---

## 🚨 4. Shock Classification

Market observations are classified into different risk levels:

```text
Normal
   ↓
Elevated Stress
   ↓
High Stress
   ↓
Severe Shock
   ↓
Extreme Shock
```

The system also identifies:

```text
Anomaly
Insufficient Data
```

### Current Classification Distribution

| Classification | Observations |
|---|---:|
| Normal | 165,101 |
| Elevated Stress | 25,083 |
| High Stress | 4,982 |
| Insufficient Data | 3,000 |
| Severe Shock | 830 |
| Anomaly | 674 |
| Extreme Shock | 150 |

---

## 🤖 5. Anomaly Detection

The project uses **Isolation Forest** from Scikit-learn to identify unusual combinations of:

- Return behavior
- Volatility
- Drawdown

This allows the system to identify abnormal market conditions that may not be captured by simple threshold-based rules.

---

## 🔥 6. Shock Event Detection

Individual shock observations are grouped into continuous financial events.

Each event contains:

```text
Event ID
Ticker
Start Date
End Date
Duration
Peak Date
Peak Shock Score
Severity
```

### Current Engine Results

```text
Shock Events Detected: 671
```

### Event Severity

| Severity | Events |
|---|---:|
| Severe Shock | 514 |
| Extreme Shock | 118 |
| Elevated Stress | 20 |
| Anomaly | 16 |
| High Stress | 3 |

---

# 🌐 7. Financial Correlation Network

The project converts stock return correlations into a graph.

Each company is represented as a node.

A connection is created when the correlation exceeds the selected threshold.

### Current Network

```text
Network Nodes: 50
Network Edges: 10
Network Density: 0.008163
Correlation Threshold: 0.60
```

### Strongest Correlations

| Company A | Company B | Correlation |
|---|---|---:|
| CANBK | PNB | 0.7538 |
| BANKBARODA | PNB | 0.7390 |
| BANKBARODA | CANBK | 0.7390 |
| BANKBARODA | SBIN | 0.7184 |
| CANBK | SBIN | 0.7124 |
| JSWSTEEL | TATASTEEL | 0.6907 |
| PNB | SBIN | 0.6867 |
| HINDALCO | TATASTEEL | 0.6749 |
| AXISBANK | ICICIBANK | 0.6739 |

This network represents potential channels through which financial shocks can propagate.

---

# 🔄 8. Shock Propagation

The system simulates how an initial shock spreads through the correlation network.

### Example

```text
Initial Shock
     │
     ▼
    PNB
     │
 ┌───┼────────┐
 ▼   ▼        ▼
CANBK SBIN BANKBARODA
 │     │       │
 └─────┼───────┘
       ▼
   ICICIBANK
       │
       ▼
   AXISBANK
```

The propagation model considers:

- Network connections
- Transmission strength
- Recovery factor
- Number of propagation steps
- Initial shock magnitude

---

# 📉 9. Systemic Risk

Systemic risk measures the combined effect of shocks across the financial network.

### PNB Shock Scenario

```text
Origin: PNB
Shock Date: 2022-02-24
Initial Shock Score: 67.6742
Initial Shock Level: 0.6767
```

After 10 propagation steps:

```text
Final Systemic Risk: 1.3337
Final Maximum Shock: 0.2152
Affected Nodes: 6
```

### Top Affected Companies

| Company | Final Shock |
|---|---:|
| PNB | 0.215167 |
| CANBK | 0.143520 |
| BANKBARODA | 0.142729 |
| SBIN | 0.115785 |
| ICICIBANK | 0.035591 |
| AXISBANK | 0.014071 |

---

# 🛡️ 10. Recovery Simulation

The recovery module simulates how a portfolio or financial system recovers after a shock.

### Current Recovery Scenario

```text
Initial Portfolio Value: 0.323258
Final Portfolio Value: 1.000000
Recovery to 99%: Day 41
```

The system can evaluate different scenarios:

```text
Mild Shock
Moderate Shock
Severe Shock
Extreme Shock
```

Recovery behavior can be controlled using recovery parameters.

---

# 📈 11. Interactive Streamlit Dashboard

The project includes an interactive Streamlit dashboard.

The dashboard provides:

### Market Overview

- Number of stocks
- Trading days
- Daily observations
- Shock events

### Shock Detection

- Shock score timeline
- Classification distribution
- Anomaly detection
- Severe and extreme shocks

### Shock Events

- Event duration
- Event severity
- Persistent events
- Peak shock dates

### Correlation Network

- Correlation matrix
- Stock relationships
- Network graph
- Strongest correlations

### Shock Propagation

- Select shock origin
- Configure transmission
- Configure recovery
- View affected companies
- Systemic risk over time

### Recovery Analysis

- Shock scenario
- Portfolio recovery curve
- Recovery day
- Final portfolio value

---

# 🏗️ Project Architecture

```text
Financial-Shock-Propagation-Recovery-Engine/
│
├── app.py
├── run_engine.py
├── run_propagation.py
├── requirements.txt
├── README.md
│
├── data/
│   └── raw/
│       └── market_data/
│           └── indian_stocks.csv
│
├── src/
│   │
│   ├── data/
│   │   └── preprocess.py
│   │
│   ├── features/
│   │   ├── market_features.py
│   │   └── risk_features.py
│   │
│   ├── shock_detection/
│   │   ├── shock_score.py
│   │   ├── shock_detector.py
│   │   ├── anomaly_detection.py
│   │   └── shock_events.py
│   │
│   ├── network/
│   │   └── correlation_network.py
│   │
│   ├── propagation/
│   │   ├── shock_propagation.py
│   │   └── systemic_risk.py
│   │
│   ├── recovery/
│   │   ├── recovery_model.py
│   │   ├── recovery_prediction.py
│   │   └── scenario_simulator.py
│   │
│   └── visualization/
│       ├── shock_plot.py
│       ├── network_plot.py
│       └── recovery_plot.py
│
├── tests/
│   ├── test_network.py
│   ├── test_preprocessing.py
│   ├── test_recovery.py
│   └── test_shock_detection.py
│
└── outputs/
    ├── processed_market_data.csv
    ├── shock_events.csv
    ├── correlation_matrix.csv
    ├── propagation_results.csv
    ├── recovery_results.csv
    ├── shock_timeline.png
    ├── correlation_network.png
    └── recovery_curve.png
```

---

# 🧰 Technology Stack

### Programming

- Python 3.12

### Data Processing

- Pandas
- NumPy

### Machine Learning

- Scikit-learn
- Isolation Forest
- Random Forest Regressor

### Network Analysis

- NetworkX

### Visualization

- Matplotlib
- Streamlit

### Testing

- Pytest

---

# 🧪 Testing

The project includes automated tests covering:

- Network construction
- Date preprocessing
- Recovery behavior
- Shock score calculation

### Current Test Result

```text
=================== test session starts ====================

tests/test_network.py          PASSED
tests/test_preprocessing.py    PASSED
tests/test_recovery.py         PASSED
tests/test_shock_detection.py  PASSED

==================== 4 passed in 11.65s ====================
```

Run tests:

```bash
python -m pytest -v
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Im-Kamall/Financial-Shock-Propagation-Recovery-Engine.git
```

Move into the project:

```bash
cd Financial-Shock-Propagation-Recovery-Engine
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Financial Shock Engine

Run:

```bash
python run_engine.py
```

The engine performs:

```text
Data Loading
     ↓
Feature Engineering
     ↓
Shock Detection
     ↓
Anomaly Detection
     ↓
Shock Event Detection
     ↓
Correlation Network
     ↓
Shock Propagation
     ↓
Recovery Simulation
     ↓
Visualization
```

---

# 🌐 Run Streamlit Dashboard

Start the dashboard:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

# 📁 Generated Outputs

After running the engine:

```text
outputs/
│
├── processed_market_data.csv
├── shock_events.csv
├── correlation_matrix.csv
├── propagation_results.csv
├── recovery_results.csv
│
├── shock_timeline.png
├── correlation_network.png
└── recovery_curve.png
```

---

# 📊 Example Engine Output

```text
FINANCIAL SHOCK PROPAGATION & RECOVERY ENGINE

Market stocks:          50
Trading days:           4,111
Daily observations:     199,820
Shock events:           671
Network nodes:          50
Network edges:          10

Shock origin:           PNB
Initial shock:          0.6767
Final systemic risk:    1.3337
Final maximum shock:    0.2152
Recovery day:           41
```

---

# 🔬 Example Use Case

Suppose PNB experiences a major financial shock.

The engine can:

```text
1. Detect abnormal PNB behavior
          ↓
2. Calculate shock score
          ↓
3. Classify the event
          ↓
4. Identify the shock date
          ↓
5. Find correlated companies
          ↓
6. Propagate the shock
          ↓
7. Measure systemic risk
          ↓
8. Identify affected companies
          ↓
9. Simulate recovery
          ↓
10. Estimate recovery time
```

This transforms a simple stock-price analysis into a **network-based financial risk intelligence system**.

---

# 🎯 Why This Project Is Different

Most financial dashboards answer:

> "What happened to this stock?"

This project asks:

> **"If this company experiences a shock, how could that shock spread through the financial network, how severe could the systemic impact become, and how long could recovery take?"**

The project combines:

```text
Financial Analytics
        +
Machine Learning
        +
Anomaly Detection
        +
Network Science
        +
Risk Modeling
        +
Scenario Simulation
```

---

# 🔮 Future Improvements

The current version can be extended with:

- Real-time stock market data
- Sector-level propagation
- Dynamic correlation networks
- Time-varying network edges
- Graph Neural Networks
- Transformer-based financial forecasting
- VaR and CVaR risk models
- Monte Carlo recovery simulation
- Portfolio optimization
- News sentiment analysis
- Financial statement integration
- Macroeconomic indicators
- RBI and interest-rate shocks
- Interactive Plotly network visualization
- Real-time Streamlit monitoring
- Cloud deployment
- Docker containerization
- Automated model retraining

---

# ⚠️ Disclaimer

This project is developed for educational, research, and hackathon purposes.

The generated shock scores, systemic-risk measurements, propagation results, and recovery estimates should **not be considered financial advice or investment recommendations**.

Historical market behavior does not guarantee future performance.


### Project Repository

https://github.com/Im-Kamall/Financial-Shock-Propagation-Recovery-Engine

---

# ⭐ Project Highlights

```text
✓ 50 Indian stocks analyzed
✓ 4,111 trading days
✓ 199,820 daily observations
✓ Automated financial feature engineering
✓ Shock scoring system
✓ Isolation Forest anomaly detection
✓ 7-level market classification
✓ 671 detected shock events
✓ Correlation-based financial network
✓ Shock propagation simulation
✓ Systemic risk measurement
✓ Recovery simulation
✓ Streamlit dashboard
✓ Automated tests
✓ Complete visualization pipeline
```

---

# 🚀 Financial Shock Propagation & Recovery Engine

## Detect → Classify → Connect → Propagate → Measure → Recover

> Turning historical market data into a network-based financial risk intelligence system.


---

# ✨ V2 Interactive Dashboard

The project now includes a redesigned Streamlit dashboard focused on financial-risk exploration.

### V2 additions

- Premium dark command-center UI
- Interactive Plotly charts
- Interactive 3D financial correlation network
- Network threshold control
- Company/node explorer
- Hypothetical shock simulator
- Propagation timeline
- Most-affected-company ranking
- Recovery Lab with adjustable shock and recovery assumptions
- Market/company explorer
- Existing engine preserved in `app_legacy.py`

### Run V2

```bash
streamlit run app.py
```

The original dashboard is preserved as:

```text
app_legacy.py
```

The underlying financial engine and data-processing modules were not replaced.

## V3 dashboard experience

The V3 interface replaces the left sidebar navigation with a single full-width dashboard and six progressive layers:

1. Command Center
2. Shock Intelligence
3. Network Map
4. Shock Simulator
5. Recovery Lab
6. Market Explorer

Use the numbered layer controls or Previous/Next buttons to move through the experience. The visual direction intentionally uses 2.5D web design principles—depth, glass panels, layered gradients, soft shadows, perspective cues, and progressive storytelling—rather than turning the data visualization itself into a literal 3D scene.
