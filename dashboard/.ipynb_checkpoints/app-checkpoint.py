# dashboard/app.py - Simple Streamlit Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
# Try to import, show friendly error if fails
try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import json
    import os
    from datetime import datetime
except ImportError as e:
    import streamlit as st
    st.error(f"Missing dependency: {str(e)}")
    st.info("Please install: pip install streamlit pandas numpy matplotlib")
    st.stop()
# Page configuration
st.set_page_config(
    page_title="Brent Oil Price Analysis",
    page_icon="🛢️",
    layout="wide"
)

# Title
st.title("🛢️ Brent Oil Price Analysis Dashboard")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load all data with error handling"""
    try:
        # Load price data
        if not os.path.exists('../data/brent_prices_cleaned.csv'):
            st.error("❌ Data file not found: ../data/brent_prices_cleaned.csv")
            return None, None, None
            
        prices_df = pd.read_csv('../data/brent_prices_cleaned.csv', parse_dates=['Date'])
        
        # Validate required columns
        required_columns = ['Date', 'Price']
        if not all(col in prices_df.columns for col in required_columns):
            st.error(f"❌ Missing columns in price data. Required: {required_columns}")
            return None, None, None
        
        # Load events data
        if not os.path.exists('../data/key_events.csv'):
            st.warning("⚠️ Events file not found. Using empty events dataframe.")
            events_df = pd.DataFrame(columns=['Event', 'Date', 'Type', 'Description'])
        else:
            events_df = pd.read_csv('../data/key_events.csv', parse_dates=['Date'])
        
        # Load change point results
        if not os.path.exists('../data/change_point_results.json'):
            st.warning("⚠️ Change point results not found. Using default values.")
            change_data = {
                'tau_samples': [359],
                'mu1_samples': [48.06],
                'mu2_samples': [92.32],
                'sigma_samples': [15.64],
                'dates': [],
                'prices': [],
                'change_point': 359,
                'change_date': '2021-06-02'
            }
        else:
            with open('../data/change_point_results.json', 'r') as f:
                change_data = json.load(f)
        
        st.success("✅ All data loaded successfully!")
        return prices_df, events_df, change_data
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None, None

# Load all data
prices_df, events_df, change_data = load_data()

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    [prices_df['Date'].min(), prices_df['Date'].max()],
    min_value=prices_df['Date'].min(),
    max_value=prices_df['Date'].max()
)

# Filter data based on selection
mask = (prices_df['Date'] >= pd.to_datetime(date_range[0])) & \
       (prices_df['Date'] <= pd.to_datetime(date_range[1]))
filtered_df = prices_df.loc[mask]

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Brent Oil Price History")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(filtered_df['Date'], filtered_df['Price'], linewidth=1, alpha=0.7)
    
    # Add change point if in range
    change_date = datetime.strptime(change_data['change_date'], '%Y-%m-%d')
    if date_range[0] <= change_date.date() <= date_range[1]:
        ax.axvline(x=change_date, color='red', linestyle='--', 
                   label=f"Change Point: {change_date.strftime('%b %d, %Y')}")
    
    # Add events if in range
    events_in_range = events_df[
        (events_df['Date'] >= pd.to_datetime(date_range[0])) & 
        (events_df['Date'] <= pd.to_datetime(date_range[1]))
    ]
    
    for _, event in events_in_range.iterrows():
        ax.axvline(x=event['Date'], color='orange', linestyle=':', alpha=0.5)
        ax.text(event['Date'], filtered_df['Price'].max() * 0.95, 
                event['Event'][:15], rotation=90, fontsize=8)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD/barrel)')
    ax.set_title('Brent Crude Oil Prices')
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("Key Statistics")
    
    st.metric(
        label="Current Price Range",
        value=f"${filtered_df['Price'].min():.2f} - ${filtered_df['Price'].max():.2f}",
        delta=f"Avg: ${filtered_df['Price'].mean():.2f}"
    )
    
    st.metric(
        label="Change Point Detected",
        value=change_date.strftime("%b %d, %Y"),
        delta=f"Price increase: {((change_data['mu2_samples'][0] - change_data['mu1_samples'][0]) / change_data['mu1_samples'][0] * 100):.1f}%"
    )
    
    st.metric(
        label="Events in Range",
        value=len(events_in_range),
        delta="Major events affecting prices"
    )

# Event details section
st.markdown("---")
st.subheader("Key Events Affecting Oil Prices")

events_col1, events_col2 = st.columns(2)

with events_col1:
    st.dataframe(
        events_df[['Event', 'Date', 'Type']],
        use_container_width=True
    )

with events_col2:
    st.subheader("Change Point Analysis")
    st.write(f"**Detected Change:** {change_date.strftime('%B %d, %Y')}")
    st.write(f"**Before Change:** ${np.mean(change_data['mu1_samples']):.2f} average")
    st.write(f"**After Change:** ${np.mean(change_data['mu2_samples']):.2f} average")
    st.write(f"**Increase:** {((np.mean(change_data['mu2_samples']) - np.mean(change_data['mu1_samples'])) / np.mean(change_data['mu1_samples']) * 100):.1f}%")
    
    # Show histogram of tau samples
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.hist(change_data['tau_samples'], bins=30, alpha=0.7, edgecolor='black')
    ax2.axvline(change_data['change_point'], color='red', linestyle='--', 
                label='Most Likely Change')
    ax2.set_xlabel('Day Index')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Uncertainty in Change Point Detection')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)
# Additional analysis section
st.markdown("---")
st.subheader("📈 Advanced Analysis")

tab1, tab2, tab3 = st.tabs(["Price Distribution", "Event Impact", "Model Details"])

with tab1:
    st.write("Price distribution before and after change point:")
    
    # Calculate prices before/after change
    change_idx = change_data['change_point']
    prices_before = change_data['prices'][:change_idx]
    prices_after = change_data['prices'][change_idx:]
    
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax3a.hist(prices_before, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax3a.set_xlabel('Price (USD)')
    ax3a.set_ylabel('Frequency')
    ax3a.set_title(f'Before Change (n={len(prices_before)})')
    ax3a.axvline(np.mean(prices_before), color='red', linestyle='--', 
                 label=f'Mean: ${np.mean(prices_before):.2f}')
    ax3a.legend()
    ax3a.grid(True, alpha=0.3)
    
    ax3b.hist(prices_after, bins=30, alpha=0.7, color='green', edgecolor='black')
    ax3b.set_xlabel('Price (USD)')
    ax3b.set_ylabel('Frequency')
    ax3b.set_title(f'After Change (n={len(prices_after)})')
    ax3b.axvline(np.mean(prices_after), color='red', linestyle='--', 
                 label=f'Mean: ${np.mean(prices_after):.2f}')
    ax3b.legend()
    ax3b.grid(True, alpha=0.3)
    
    st.pyplot(fig3)

with tab2:
    st.write("Event impact analysis:")
    
    # Find closest event to change point
    change_date = datetime.strptime(change_data['change_date'], '%Y-%m-%d')
    events_df['days_from_change'] = (events_df['Date'] - change_date).dt.days.abs()
    closest_event = events_df.loc[events_df['days_from_change'].idxmin()]
    
    st.write(f"**Event closest to detected change:**")
    st.write(f"- **{closest_event['Event']}**")
    st.write(f"- Date: {closest_event['Date'].strftime('%B %d, %Y')}")
    st.write(f"- Days from change: {closest_event['days_from_change']} days")
    st.write(f"- Type: {closest_event['Type']}")
    st.write(f"- Description: {closest_event['Description']}")

with tab3:
    st.write("Bayesian Model Details:")
    
    col3a, col3b, col3c = st.columns(3)
    
    with col3a:
        st.metric("Model Samples", "600", "MCMC draws")
    
    with col3b:
        rhat_tau = np.std(change_data['tau_samples']) / np.sqrt(len(change_data['tau_samples']))
        st.metric("Uncertainty (τ)", f"{rhat_tau:.2f}", "Lower is better")
    
    with col3c:
        st.metric("Data Points", "729", "2020-2022 period")
    
    st.write("**Parameter Distributions:**")
    
    fig4, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    axes[0, 0].hist(change_data['mu1_samples'], bins=30, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 0].set_title('μ₁: Mean Before Change')
    axes[0, 0].set_xlabel('Price (USD)')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].hist(change_data['mu2_samples'], bins=30, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].set_title('μ₂: Mean After Change')
    axes[0, 1].set_xlabel('Price (USD)')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].hist(change_data['sigma_samples'], bins=30, alpha=0.7, color='orange', edgecolor='black')
    axes[1, 0].set_title('σ: Standard Deviation')
    axes[1, 0].set_xlabel('Price (USD)')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].hist(change_data['tau_samples'], bins=30, alpha=0.7, color='red', edgecolor='black')
    axes[1, 1].set_title('τ: Change Point Location')
    axes[1, 1].set_xlabel('Day Index')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig4)

# Footer
st.markdown("---")
st.caption("Birhan Energies - Brent Oil Price Analysis Dashboard | Data: 1987-2022")