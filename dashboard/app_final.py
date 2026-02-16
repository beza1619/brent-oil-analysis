import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Brent Oil Analysis", layout="wide", page_icon="🛢️")

# Title
st.title("🛢️ Brent Oil Price Analysis Dashboard")
st.markdown("**Birhan Energies - Data Science Challenge**")
st.markdown("---")

# YOUR ACTUAL FINDINGS (from your analysis)
ACTUAL_RESULTS = {
    "change_date": "June 2, 2021",
    "price_before": 48.17,
    "price_after": 92.37,
    "percent_increase": 94.1,
    "data_points": 9011,
    "period": "1987-2022",
    "events_analyzed": 13,
    "model_type": "Bayesian Change Point",
    "confidence": "High",
    "adf_statistic": -16.43,
    "adf_p_value": 0.0000,
    "volatility": 0.0255
}

# Sidebar
st.sidebar.header("📊 Analysis Summary")
st.sidebar.metric("Change Point", ACTUAL_RESULTS["change_date"])
st.sidebar.metric("Price Increase", f"{ACTUAL_RESULTS['percent_increase']}%")
st.sidebar.metric("Before/After", f"${ACTUAL_RESULTS['price_before']} → ${ACTUAL_RESULTS['price_after']}")
st.sidebar.metric("Data Points", f"{ACTUAL_RESULTS['data_points']:,}")
st.sidebar.metric("Events Analyzed", ACTUAL_RESULTS["events_analyzed"])

# Create visualization of YOUR results
st.header("📈 Key Findings from Your Analysis")

# 1. Price change visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Regime Change")
    
    # Create bar chart showing before/after
    fig1 = go.Figure(data=[
        go.Bar(name='Before Change', x=['Before'], y=[ACTUAL_RESULTS["price_before"]], 
               marker_color='blue', text=[f"${ACTUAL_RESULTS['price_before']}"], textposition='auto'),
        go.Bar(name='After Change', x=['After'], y=[ACTUAL_RESULTS["price_after"]], 
               marker_color='red', text=[f"${ACTUAL_RESULTS['price_after']}"], textposition='auto')
    ])
    
    fig1.update_layout(
        title=f"Price Change: {ACTUAL_RESULTS['percent_increase']}% Increase",
        yaxis_title="Average Price (USD/barrel)",
        showlegend=True,
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Statistical Significance")
    
    metrics_data = {
        'Metric': ['ADF Statistic', 'p-value', 'Volatility', 'Confidence'],
        'Value': [ACTUAL_RESULTS["adf_statistic"], ACTUAL_RESULTS["adf_p_value"], 
                  ACTUAL_RESULTS["volatility"], ACTUAL_RESULTS["confidence"]],
        'Interpretation': ['Highly stationary', 'p < 0.001', 'Log returns std', 'High certainty']
    }
    
    df_metrics = pd.DataFrame(metrics_data)
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)

# 2. Event timeline
st.header("📅 Key Events Analyzed")

events_data = [
    {"Event": "2008 Financial Crisis", "Date": "2008-09-15", "Impact": "High", "Type": "Economic"},
    {"Event": "Arab Spring", "Date": "2010-12-17", "Impact": "Medium", "Type": "Political"},
    {"Event": "OPEC 2014 Decision", "Date": "2014-11-27", "Impact": "High", "Type": "Policy"},
    {"Event": "COVID-19 Pandemic", "Date": "2020-03-11", "Impact": "Very High", "Type": "Economic"},
    {"Event": "Russia-Ukraine War", "Date": "2022-02-24", "Impact": "High", "Type": "Conflict"},
    {"Event": "2020 Negative Prices", "Date": "2020-04-20", "Impact": "Very High", "Type": "Market"},
    {"Event": "Iran Sanctions", "Date": "2018-05-08", "Impact": "Medium", "Type": "Political"},
    {"Event": "Detected Change Point", "Date": "2021-06-02", "Impact": "Structural", "Type": "Statistical"}
]

df_events = pd.DataFrame(events_data)
df_events['Date'] = pd.to_datetime(df_events['Date'])

# Create timeline
fig2 = px.scatter(df_events, x='Date', y='Impact', color='Type',
                 size=[20, 15, 20, 25, 20, 25, 15, 30],
                 hover_data=['Event', 'Impact', 'Type'],
                 title='Timeline of Key Events Affecting Oil Prices')

# Add change point line
change_date = datetime(2021, 6, 2)
fig2.add_vline(x=change_date, line_dash="dash", line_color="red", 
               annotation_text="Change Point", annotation_position="top right")

st.plotly_chart(fig2, use_container_width=True)

# 3. Methodology
st.header("🔬 Methodology")

methodology_tab1, methodology_tab2, methodology_tab3 = st.tabs(["Bayesian Model", "Data Processing", "Event Analysis"])

with methodology_tab1:
    st.markdown("""
    ### Bayesian Change Point Model (PyMC)
    ```python
    with pm.Model() as change_point_model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n_days-1)
        mu1 = pm.Normal("mu1", mu=prices.mean(), sigma=50)
        mu2 = pm.Normal("mu2", mu=prices.mean(), sigma=50)
        sigma = pm.HalfNormal("sigma", sigma=30)
        mean = pm.math.switch(tau > np.arange(n_days), mu1, mu2)
        likelihood = pm.Normal("likelihood", mu=mean, sigma=sigma, observed=prices)
    ```
    
    **Results:**
    - τ (change point): Day 359 = June 2, 2021
    - μ₁ (before): $48.06 ± 0.99
    - μ₂ (after): $92.32 ± 1.00
    - σ (volatility): $15.64 ± 0.41
    """)

with methodology_tab2:
    st.markdown("""
    ### Data Processing Pipeline
    1. **Data Loading**: 9,011 daily prices (1987-2022)
    2. **Cleaning**: Date format standardization, missing value check
    3. **Stationarity Test**: ADF test on log returns (p < 0.001)
    4. **Volatility Analysis**: Log returns show clustering pattern
    5. **Transformation**: Log returns for model stability
    
    **Key Statistics:**
    - Mean price: $48.42
    - Price range: $9.10 - $143.95
    - Standard deviation: $32.86
    - Log returns std: 0.0255
    """)

with methodology_tab3:
    st.markdown("""
    ### Event Correlation Analysis
    1. **Event Identification**: 13 major geopolitical/economic events
    2. **Date Rationale**: Approximate start of market impact
    3. **Correlation Analysis**: Time proximity to change points
    4. **Impact Quantification**: Before/after price comparisons
    
    **Event Categories:**
    - Political: Sanctions, wars, conflicts
    - Economic: Recessions, pandemics
    - Policy: OPEC decisions, agreements
    - Market: Price crashes, shocks
    """)

# 4. Business Implications
st.header("💼 Business Implications")

col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("For Investors")
    st.markdown("""
    - **Timing**: Identify structural breaks for portfolio adjustment
    - **Risk**: Anticipate volatility around geopolitical events
    - **Returns**: Capitalize on post-event price movements
    - **Strategy**: Use change points as regime shift signals
    """)

with col4:
    st.subheader("For Policymakers")
    st.markdown("""
    - **Stability**: Prepare for oil price shocks
    - **Security**: Diversify energy sources based on risks
    - **Planning**: Time strategic reserves purchases
    - **Response**: Develop contingency plans for key events
    """)

with col5:
    st.subheader("For Energy Companies")
    st.markdown("""
    - **Operations**: Adjust production based on price regimes
    - **Hedging**: Implement strategies during volatile periods
    - **Supply Chain**: Secure contracts during stable regimes
    - **Forecasting**: Use Bayesian models for price predictions
    """)

# 5. Project Files
st.header("📁 Project Deliverables")

st.markdown("""
| File | Location | Purpose |
|------|----------|---------|
| **Analysis Plan** | `reports/analysis_plan_final.md` | Task 1: Methodology |
| **Event Database** | `data/key_events.csv` | 13 key events |
| **Change Point Analysis** | `notebooks/03_change_point_analysis.ipynb` | Bayesian modeling |
| **Results Summary** | `reports/task2_change_point_results.txt` | Key findings |
| **Full Code** | GitHub Repository | Complete implementation |
""")

st.info("""
**GitHub Repository:** https://github.com/beza1619/brent-oil-analysis  
**Complete analysis with real data in Jupyter notebooks.**
""")

# Footer
st.markdown("---")
st.caption("""
**Birhan Energies Data Science Challenge** | February 2026  
**Change Point Detection**: Bayesian analysis with PyMC | **Event Correlation**: 13 geopolitical events  
**Key Finding**: Structural break detected June 2, 2021 with 94.1% price increase
""")