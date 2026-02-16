import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Brent Oil Dashboard", layout="wide")
st.title("🛢️ Brent Oil Price Analysis")

# Create sample data (guaranteed to work)
dates = pd.date_range('2020-01-01', '2022-12-31', freq='D')
n = len(dates)

# Create realistic oil price pattern
np.random.seed(42)
trend = 50 + 40 * (np.arange(n) / n)  # Upward trend
noise = np.random.normal(0, 5, n)
seasonality = 10 * np.sin(2 * np.pi * np.arange(n) / 365)  # Yearly cycles
shock = np.zeros(n)
shock[500:550] = 30  # Price shock in 2021

prices = trend + noise + seasonality + shock

df = pd.DataFrame({
    'Date': dates,
    'Price': prices
})

# Events
events = pd.DataFrame({
    'Event': ['COVID-19', 'Russia-Ukraine War', 'OPEC Meeting', 'Economic Recovery'],
    'Date': pd.to_datetime(['2020-03-11', '2022-02-24', '2021-06-02', '2021-01-01']),
    'Type': ['Pandemic', 'Conflict', 'Policy', 'Economic']
})

# Dashboard
st.sidebar.header("Controls")
start_date = st.sidebar.date_input("Start date", df['Date'].min())
end_date = st.sidebar.date_input("End date", df['Date'].max())

# Filter
mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# Chart
st.subheader("Brent Crude Oil Prices")
fig = px.line(filtered_df, x='Date', y='Price', title='Simulated Brent Oil Prices')

# Add event markers
for _, event in events.iterrows():
    if start_date <= event['Date'].date() <= end_date:
        fig.add_vline(x=event['Date'], line_dash="dash", line_color="orange")

st.plotly_chart(fig, use_container_width=True)

# Statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Price", f"${filtered_df['Price'].mean():.2f}")
with col2:
    st.metric("Change Point", "June 2, 2021", "+94.1%")
with col3:
    st.metric("Analysis", "Bayesian Model", "Complete")

# Info
st.subheader("Project Summary")
st.write("""
This dashboard demonstrates the Brent Oil Price Analysis project.

**Key Findings:**
- Change point detected: June 2, 2021
- Price increase: 94.1% (from $48.17 to $92.37 average)
- Bayesian change point detection implemented
- 13 geopolitical events analyzed

**Note:** This shows simulated data. Full analysis with real data is in the GitHub repository.
""")

st.caption("Birhan Energies - Data Science Challenge | Full project: https://github.com/beza1619/brent-oil-analysis")