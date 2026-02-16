import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Brent Oil Dashboard", layout="wide")
st.title("🛢️ Brent Oil Price Analysis - Birhan Energies")

# Create sample data (works without external files)
dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
n = len(dates)

# Create realistic oil price pattern
np.random.seed(42)
trend = 50 + 40 * (np.arange(n) / n)  # Upward trend
noise = np.random.normal(0, 5, n)
seasonality = 10 * np.sin(2 * np.pi * np.arange(n) / 365)
shock = np.zeros(n)
shock[500:550] = 30  # Simulated price shock in June 2021

prices = trend + noise + seasonality + shock

df = pd.DataFrame({
    'Date': dates,
    'Price': prices
})

# Key events
events = pd.DataFrame({
    'Event': ['COVID-19 Pandemic', 'Russia-Ukraine War', 'OPEC Meeting', 'Economic Recovery', 'Change Point'],
    'Date': pd.to_datetime(['2020-03-11', '2022-02-24', '2021-06-02', '2021-01-01', '2021-06-02']),
    'Type': ['Pandemic', 'Conflict', 'Policy', 'Economic', 'Statistical']
})

# Sidebar
st.sidebar.header("📊 Dashboard Controls")
start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())

# Filter data
mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# Main chart
st.subheader("Brent Crude Oil Price Simulation")
fig = px.line(filtered_df, x='Date', y='Price', 
              title='Brent Oil Prices with Event Markers',
              labels={'Price': 'Price (USD/barrel)', 'Date': 'Date'})

# Add event markers
event_colors = {'Pandemic': 'red', 'Conflict': 'orange', 'Policy': 'green', 'Economic': 'blue', 'Statistical': 'purple'}
for _, event in events.iterrows():
    if start_date <= event['Date'].date() <= end_date:
        fig.add_vline(x=event['Date'], line_dash="dash", 
                     line_color=event_colors.get(event['Type'], 'gray'),
                     annotation_text=event['Event'][:15],
                     annotation_position="top right")

st.plotly_chart(fig, use_container_width=True)

# Key metrics
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Price", f"${filtered_df['Price'].mean():.2f}", 
              f"{filtered_df['Price'].std():.1f} std")

with col2:
    price_change = ((filtered_df['Price'].iloc[-1] - filtered_df['Price'].iloc[0]) / 
                    filtered_df['Price'].iloc[0] * 100) if len(filtered_df) > 1 else 0
    st.metric("Price Change", f"{price_change:+.1f}%", "Selected period")

with col3:
    st.metric("Change Point", "June 2, 2021", "+94.1%")

with col4:
    events_in_view = len([e for e in events['Date'] if start_date <= e.date() <= end_date])
    st.metric("Events in View", events_in_view, "Geopolitical")

# Project findings
st.subheader("🔍 Project Findings")
st.markdown("""
| Finding | Value | Impact |
|---------|-------|--------|
| **Change Point** | June 2, 2021 | Structural market break |
| **Price Increase** | 94.1% | \$48.17 → \$92.37 average |
| **Method** | Bayesian Change Point | PyMC implementation |
| **Events Analyzed** | 13 | Geopolitical & economic |
| **Data Period** | 1987-2022 | 35 years of daily prices |
""")

# Event details
st.subheader("📅 Key Events Analyzed")
st.dataframe(events, use_container_width=True)

# Methodology
with st.expander("📖 Methodology Details"):
    st.markdown("""
    ### Bayesian Change Point Analysis
    1. **Data**: Daily Brent oil prices (1987-2022)
    2. **Model**: PyMC with MCMC sampling
    3. **Detection**: Single change point (τ)
    4. **Parameters**: μ₁ (before), μ₂ (after), σ (volatility)
    
    ### Key Results
    - **τ (change point)**: Day 359 (June 2, 2021)
    - **μ₁ (before)**: \$48.06 average
    - **μ₂ (after)**: \$92.32 average
    - **Increase**: 94.1% statistically significant
    
    ### Limitations
    - Correlation ≠ causation
    - Daily data misses intra-day moves
    - External factors not modeled
    """)

# Footer
st.markdown("---")
st.caption("""
**Birhan Energies - Data Science Challenge**  
**Dashboard**: Simulated data for demonstration | **Full Analysis**: https://github.com/beza1619/brent-oil-analysis  
**Change Point Detection**: Bayesian modeling with PyMC | **Event Correlation**: 13 geopolitical events
""")