\# Brent Oil Price Analysis - Change Point Detection



\## 📊 Project Overview

Analysis of how geopolitical and economic events affect Brent oil prices using Bayesian change point detection. Identified structural breaks and quantified event impacts.



\## 🎯 Business Objectives

\- Identify key events impacting Brent oil prices (1987-2022)

\- Quantify price changes using statistical methods

\- Provide insights for investors, policymakers, and energy companies



\## 📁 Project Structure

brent-oil-analysis/

├── data/ # Data files

│ ├── BrentOilPrices.csv # Original dataset

│ ├── brent\_prices\_cleaned.csv # Cleaned data

│ ├── key\_events.csv # 13 key events

│ └── change\_point\_results.json # Model outputs

├── notebooks/ # Jupyter notebooks

│ ├── 01\_data\_exploration.ipynb

│ ├── 02\_event\_research.ipynb

│ └── 03\_change\_point\_analysis.ipynb

├── dashboard/ # Streamlit dashboard

│ └── app.py

├── reports/ # Documentation

│ ├── analysis\_plan\_final.md

│ ├── task2\_change\_point\_results.txt

│ ├── final\_report.md

│ └── dashboard\_screenshots/ # Screenshots

└── README.md # This file



\## 🚀 Quick Start



\### 1. Installation

```bash

pip install -r requirements.txt

\# Open Jupyter notebooks

jupyter notebook notebooks/03\_change\_point\_analysis.ipynb

🔍 Key Findings

Change Point Detected

Date: June 2, 2021



Impact: 94.1% price increase



Before: $48.17 average price



After: $92.37 average price



Key Events Identified (13 events)

2008 Financial Crisis

Arab Spring (2010)



OPEC production cuts 2014



COVID-19 pandemic



Russia-Ukraine war 2022



... and 8 more events



📈 Methodology

1\. Data Preparation

Daily Brent oil prices (1987-2022)

Date formatting and cleaning



Log returns calculation



2\. Bayesian Change Point Model

PyMC implementation



MCMC sampling (600 draws)



Parameter estimation: μ₁, μ₂, σ, τ



3\. Event Correlation

Event database creation

Time-series alignment



Impact quantification



🛠️ Technologies Used

Python: pandas, numpy, matplotlib



Bayesian Modeling: PyMC, ArviZ



Visualization: Streamlit, Plotly



Version Control: Git, GitHub



📊 Dashboard Features

Interactive price chart with date filtering

Event markers and tooltips



Change point visualization



Statistical summaries



Model diagnostics



📝 Deliverables

Task 1: Analysis plan + event database



Task 2: Bayesian change point analysis



Task 3: Interactive dashboard

pandas>=1.5.0

numpy>=1.24.0

matplotlib>=3.7.0

pymc>=5.0.0

arviz>=0.15.0

streamlit>=1.24.0

jupyter>=1.0.0

