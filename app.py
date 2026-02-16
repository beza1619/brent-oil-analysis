# app.py - Brent Oil Change Point Analysis Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Brent Oil Change Point Analysis",
    page_icon="🛢️",
    layout="wide"
)

# Title
st.title("🛢️ Brent Oil Price Change Point Analysis")
st.markdown("---")

# Load data function
@st.cache_data
def load_data():
    """Load all data files from the data folder"""
    
    # Get current directory
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, "data")
    
    # Initialize variables
    prices_df = None
    events_df = None
    change_data = None
    
    # Load price data
    price_path = os.path.join(data_dir, "brent_prices_cleaned.csv")
    if os.path.exists(price_path):
        try:
            prices_df = pd.read_csv(price_path, parse_dates=['Date'])
        except Exception as e:
            st.error(f"Error loading price data: {e}")
            return None, None, None
    else:
        st.error("Price data file not found. Please check your data folder.")
        return None, None, None
    
    # Load events data
    events_path = os.path.join(data_dir, "key_events.csv")
    if os.path.exists(events_path):
        try:
            events_df = pd.read_csv(events_path, parse_dates=['Date'])
        except Exception as e:
            st.warning(f"Could not load events: {e}")
            # Create sample events as fallback
            events_df = pd.DataFrame({
                'Event': ['COVID-19 Pandemic', 'OPEC+ Production Cuts', 'Russia-Ukraine Conflict'],
                'Date': pd.to_datetime(['2020-03-11', '2020-04-12', '2022-02-24']),
                'Type': ['Pandemic', 'Supply', 'Geopolitical']
            })
    else:
        st.warning("Events file not found. Using sample events.")
        events_df = pd.DataFrame({
            'Event': ['COVID-19 Pandemic', 'OPEC+ Production Cuts', 'Russia-Ukraine Conflict'],
            'Date': pd.to_datetime(['2020-03-11', '2020-04-12', '2022-02-24']),
            'Type': ['Pandemic', 'Supply', 'Geopolitical']
        })
    
    # Load change point results
    change_path = os.path.join(data_dir, "change_point_results.json")
    if os.path.exists(change_path):
        try:
            with open(change_path, 'r') as f:
                change_data = json.load(f)
        except Exception as e:
            st.warning(f"Could not load change points: {e}")
            # Create sample change point data
            change_data = {
                'tau_samples': list(range(350, 370)),
                'mu1_samples': [48.0] * 20,
                'mu2_samples': [92.0] * 20,
                'sigma_samples': [15.6] * 20,
                'prices': prices_df['Price'].tolist() if prices_df is not None else [],
                'change_point': 359,
                'change_date': '2021-06-02'
            }
    else:
        st.warning("Change point results not found. Using sample data.")
        change_data = {
            'tau_samples': list(range(350, 370)),
            'mu1_samples': [48.0] * 20,
            'mu2_samples': [92.0] * 20,
            'sigma_samples': [15.6] * 20,
            'prices': prices_df['Price'].tolist() if prices_df is not None else [],
            'change_point': 359,
            'change_date': '2021-06-02'
        }
    
    return prices_df, events_df, change_data

# Load the data
prices_df, events_df, change_data = load_data()

# Check if we have the minimum required data
if prices_df is None:
    st.error("❌ Could not load price data. Please check your data folder.")
    st.stop()

# Sidebar controls
st.sidebar.header("📊 Dashboard Controls")

# Date range selector
min_date = prices_df['Date'].min()
max_date = prices_df['Date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter data
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])
mask = (prices_df['Date'] >= start_date) & (prices_df['Date'] <= end_date)
filtered_df = prices_df.loc[mask]

# Main dashboard
st.header("📈 Price Analysis")

# Create two columns
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Brent Oil Price with Change Point")
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(filtered_df['Date'], filtered_df['Price'], 
            linewidth=1.5, color='blue', alpha=0.7, label='Daily Price')
    
    # Add change point if available
    if change_data and 'change_date' in change_data:
        change_date = datetime.strptime(change_data['change_date'], '%Y-%m-%d')
        if start_date <= change_date <= end_date:
            ax.axvline(x=change_date, color='red', linewidth=2, 
                      linestyle='--', label=f'Change Point: {change_date.strftime("%Y-%m-%d")}')
    
    # Add events
    if events_df is not None:
        events_in_range = events_df[
            (events_df['Date'] >= start_date) & 
            (events_df['Date'] <= end_date)
        ]
        
        for _, event in events_in_range.iterrows():
            ax.axvline(x=event['Date'], color='orange', 
                      linewidth=1, linestyle=':', alpha=0.5)
            ax.text(event['Date'], filtered_df['Price'].max() * 0.95,
                   event['Event'][:20], rotation=90, fontsize=8)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD/barrel)', fontsize=12)
    ax.set_title('Brent Crude Oil Prices with Detected Change Point', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("📊 Key Statistics")
    
    # Price stats
    st.metric(
        label="Average Price",
        value=f"${filtered_df['Price'].mean():.2f}",
        delta=f"Min: ${filtered_df['Price'].min():.2f}"
    )
    
    st.metric(
        label="Price Range",
        value=f"${filtered_df['Price'].min():.2f} - ${filtered_df['Price'].max():.2f}",
        delta=f"Volatility: ${filtered_df['Price'].std():.2f}"
    )
    
    # Change point stats
    if change_data:
        if 'mu1_samples' in change_data and len(change_data['mu1_samples']) > 0:
            before_mean = np.mean(change_data['mu1_samples'])
            after_mean = np.mean(change_data['mu2_samples'])
            pct_change = ((after_mean - before_mean) / before_mean) * 100
            
            st.metric(
                label="Price Change at Breakpoint",
                value=f"{pct_change:.1f}%",
                delta=f"Before: ${before_mean:.2f} → After: ${after_mean:.2f}"
            )

# Second row - Analysis tabs
st.markdown("---")
st.header("🔍 Detailed Analysis")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Distribution Analysis", 
    "📅 Event Impact", 
    "📈 Model Parameters",
    "📋 Raw Data"
])

with tab1:
    st.subheader("Price Distribution Before and After Change Point")
    
    if change_data and 'prices' in change_data and len(change_data['prices']) > 0:
        # Get prices before and after change
        change_idx = change_data.get('change_point', 359)
        prices = change_data['prices']
        
        if len(prices) > change_idx:
            before_prices = prices[:change_idx]
            after_prices = prices[change_idx:]
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                fig1, ax1 = plt.subplots(figsize=(8, 4))
                ax1.hist(before_prices, bins=30, alpha=0.7, color='blue', edgecolor='black')
                ax1.axvline(np.mean(before_prices), color='red', linestyle='--', 
                           label=f"Mean: ${np.mean(before_prices):.2f}")
                ax1.set_xlabel('Price (USD/barrel)')
                ax1.set_ylabel('Frequency')
                ax1.set_title(f'Before Change Point (n={len(before_prices)})')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                st.pyplot(fig1)
            
            with col_b:
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                ax2.hist(after_prices, bins=30, alpha=0.7, color='green', edgecolor='black')
                ax2.axvline(np.mean(after_prices), color='red', linestyle='--',
                           label=f"Mean: ${np.mean(after_prices):.2f}")
                ax2.set_xlabel('Price (USD/barrel)')
                ax2.set_ylabel('Frequency')
                ax2.set_title(f'After Change Point (n={len(after_prices)})')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
                st.pyplot(fig2)

with tab2:
    st.subheader("Event Impact Analysis")
    
    if events_df is not None and change_data:
        # Find event closest to change point
        change_date = datetime.strptime(change_data['change_date'], '%Y-%m-%d')
        events_df['days_diff'] = abs((events_df['Date'] - change_date).dt.days)
        closest_event = events_df.loc[events_df['days_diff'].idxmin()]
        
        st.write(f"### Event Closest to Detected Change Point")
        st.write(f"**Event:** {closest_event['Event']}")
        st.write(f"**Date:** {closest_event['Date'].strftime('%B %d, %Y')}")
        st.write(f"**Days from change:** {closest_event['days_diff']} days")
        st.write(f"**Type:** {closest_event['Type']}")
        
        # Show all events
        st.write("### All Key Events")
        st.dataframe(events_df[['Event', 'Date', 'Type']], use_container_width=True)

with tab3:
    st.subheader("Bayesian Model Parameters")
    
    if change_data:
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            st.metric("Number of MCMC Samples", 
                     len(change_data.get('tau_samples', [])))
        
        with col_p2:
            uncertainty = np.std(change_data.get('tau_samples', [0]))
            st.metric("Change Point Uncertainty", 
                     f"±{uncertainty:.1f} days")
        
        with col_p3:
            if 'sigma_samples' in change_data:
                st.metric("Volatility (σ)", 
                         f"${np.mean(change_data['sigma_samples']):.2f}")
        
        # Parameter distributions
        fig3, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        if 'mu1_samples' in change_data:
            axes[0, 0].hist(change_data['mu1_samples'], bins=30, alpha=0.7, color='blue')
            axes[0, 0].set_title('μ₁: Mean Before Change')
            axes[0, 0].set_xlabel('Price (USD)')
            axes[0, 0].grid(True, alpha=0.3)
        
        if 'mu2_samples' in change_data:
            axes[0, 1].hist(change_data['mu2_samples'], bins=30, alpha=0.7, color='green')
            axes[0, 1].set_title('μ₂: Mean After Change')
            axes[0, 1].set_xlabel('Price (USD)')
            axes[0, 1].grid(True, alpha=0.3)
        
        if 'sigma_samples' in change_data:
            axes[1, 0].hist(change_data['sigma_samples'], bins=30, alpha=0.7, color='orange')
            axes[1, 0].set_title('σ: Standard Deviation')
            axes[1, 0].set_xlabel('Price (USD)')
            axes[1, 0].grid(True, alpha=0.3)
        
        if 'tau_samples' in change_data:
            axes[1, 1].hist(change_data['tau_samples'], bins=30, alpha=0.7, color='red')
            axes[1, 1].axvline(change_data.get('change_point', 0), color='black', 
                              linestyle='--', label='Most Likely')
            axes[1, 1].set_title('τ: Change Point Location')
            axes[1, 1].set_xlabel('Day Index')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig3)

with tab4:
    st.subheader("Raw Data Sample")
    
    # Show price data
    st.write("### Price Data")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Price Data as CSV",
        data=csv,
        file_name=f"brent_prices_{start_date.date()}_to_{end_date.date()}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>📊 <b>Brent Oil Change Point Analysis</b> | Bayesian Time Series Analysis</p>
    <p style='font-size: 0.8em; color: gray;'>Data: 1987-2022 | Change point detection using MCMC</p>
</div>
""", unsafe_allow_html=True)