# Task 1: Analysis Plan for Brent Oil Price Impact Study

## 1. Analysis Workflow Steps

### Step 1: Data Preparation
- Load historical Brent oil prices (1987-2022)
- Clean and format date column
- Handle any missing values

### Step 2: Exploratory Data Analysis
- Visualize price trends over 35-year period
- Calculate log returns for stationarity
- Identify periods of high volatility

### Step 3: Event Research & Compilation
- Research major geopolitical/economic events
- Create structured events dataset (13 events identified)
- Map event dates to price data

### Step 4: Change Point Analysis
- Implement Bayesian change point detection using PyMC
- Identify structural breaks in price series
- Quantify magnitude of changes

### Step 5: Event Correlation
- Match detected change points with known events
- Analyze time lags between events and price reactions
- Quantify impact of specific events

### Step 6: Dashboard Development
- Create interactive visualization
- Allow users to explore event impacts
- Display key metrics and insights

## 2. Key Events Identified
13 major events identified affecting oil prices:
1. 2008 Financial Crisis
2. Arab Spring (2010)
3. OPEC production decision (2014)
4. COVID-19 pandemic (2020)
5. Russia-Ukraine war (2022)
6. 2011 Libya civil war
7. 2014 oil price crash
8. 2019 Saudi drone attacks
9. 2020 negative oil prices
10. Iran sanctions (2018)
11. Iraq War (2003)
12. Gulf War (1990)
13. Iran nuclear deal (2015)

## 3. Assumptions & Limitations
- **Correlation vs Causation**: Statistical correlation doesn't prove causation
- **Data Frequency**: Daily data may miss intra-day volatility spikes
- **External Factors**: Many unmeasured factors influence oil prices
- **Event Timing**: Exact impact timing may vary from event dates

## 4. Communication Channels
1. **PDF Report**: Detailed analysis for policymakers
2. **Interactive Dashboard**: For analysts and investors
3. **Executive Summary**: One-page summary for decision-makers
4. **Presentation**: Stakeholder briefing with key findings
