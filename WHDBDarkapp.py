import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Women's Health Companies", layout="wide")

# Configure the dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stSelectbox, .stMultiSelect {
        background-color: #2D2D2D;
    }
    .dataframe {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stToolbar"] {
        background-color: #2D2D2D;
    }
    </style>
""", unsafe_allow_html=True)

# Create the dataset
data = {
    'Company': [
        'AbbVie', 'Abbott Laboratories', 'Fuji Pharma Co. Ltd.', 'Veru Inc.',
        'Pulsenmore Ltd.', 'Daré Bioscience Inc.', 'Femasys Inc.',
        "Aspira Women's Health", 'Palatin Technologies Inc.', 'Mithra Pharmaceuticals',
        'The Cooper Companies', 'Hologic Inc.', 'Creative Medical Technology',
        'Minerva Surgical', 'Organon & Co.', 'INVO Bioscience', 'Agile Therapeutics',
        'Bonzun', 'Evofem Biosciences Inc.', 'Callitas Therapeutics'
    ],
    'Market_Cap': [319.84, 207.08, 0.2819, 0.406, 0.175, 0.185, 0.203, 0.247, 0.275, 0.289,
                   20.3, 19.44, 0.302, 0.357, 40.1, 2.69, 2.03, 0.339, 0.128, 0.0033],
    'Founded': [2013, 1888, 1965, 1971, 2014, 2004, 2004, 1993, 1986, 1999,
                1958, 1985, 1998, 2008, 2021, 2007, 1997, 2012, 2007, 2003],
    'Employees': [50000, 113000, 1600, 190, 50, 40, 40, 100, 20, 500,
                  15000, 6940, 10, 240, 9000, 20, 20, 50, 40, 0],
    'Headquarters': ['Illinois, USA', 'Illinois, USA', 'Tokyo, Japan', 'Florida, USA',
                    'Omer, Israel', 'California, USA', 'Georgia, USA', 'Texas, USA',
                    'New Jersey, USA', 'Liège, Belgium', 'California, USA', 'Massachusetts, USA',
                    'Arizona, USA', 'California, USA', 'New Jersey, USA', 'Florida, USA',
                    'New Jersey, USA', 'Stockholm, Sweden', 'California, USA', 'British Columbia, CA'],
    'Exchange': ['NYSE', 'NYSE', 'TYO', 'NASDAQ', 'TASE', 'NASDAQ', 'NASDAQ', 'NASDAQ',
                 'NYSE', 'EBR', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NYSE', '',
                 'NASDAQ', 'STO', 'OTCMKTS', 'OTCMKTS']
}

df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("Filter Options")

# Country filter
countries = sorted(list(set([loc.split(", ")[1] for loc in df['Headquarters']])))
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)

# Exchange filter
exchanges = sorted(list(set(df['Exchange'])))
selected_exchanges = st.sidebar.multiselect("Select Stock Exchanges", exchanges, default=exchanges)

# Market cap range
market_cap_range = st.sidebar.slider(
    "Market Cap Range (USD)",
    min_value=float(df['Market_Cap'].min()),
    max_value=float(df['Market_Cap'].max()),
    value=(float(df['Market_Cap'].min()), float(df['Market_Cap'].max()))
)

# Filter the dataframe
mask = (
    df['Headquarters'].apply(lambda x: x.split(", ")[1] in selected_countries) &
    df['Exchange'].isin(selected_exchanges) &
    (df['Market_Cap'] >= market_cap_range[0]) &
    (df['Market_Cap'] <= market_cap_range[1])
)
filtered_df = df[mask]

# Dashboard tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Data", "Visualizations", "Insights"])

with tab1:
    st.header("Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Market Cap", f"${filtered_df['Market_Cap'].sum():,.0f}B")
    with col2:
        st.metric("Average Market Cap", f"${filtered_df['Market_Cap'].mean():,.0f}M")
    with col3:
        st.metric("Median Founded Year", f"{filtered_df['Founded'].median():.1f}")
    with col4:
        st.metric("Number of Companies", len(filtered_df))

    # Automated insights
    st.subheader("Automated Insights")
    st.markdown(f"""
    * The total market cap of the selected companies is ${filtered_df['Market_Cap'].sum():,.0f}B.
    * On average, companies have a market cap of ${filtered_df['Market_Cap'].mean():,.0f}M.
    * The median founded year is {filtered_df['Founded'].median():.1f}.
    * There are {len(filtered_df)} companies from {len(filtered_df['Headquarters'].unique())} countries.
    """)

with tab2:
    st.header("Companies Data")
    st.dataframe(
        filtered_df.sort_values('Market_Cap', ascending=False),
        hide_index=True,
        use_container_width=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        "Download Filtered Data as CSV",
        csv,
        "filtered_companies.csv",
        "text/csv"
    )

with tab3:
    st.header("Visualizations")
    
    # Market cap visualization
    fig1 = px.bar(
        filtered_df.sort_values('Market_Cap', ascending=True),
        x='Company',
        y='Market_Cap',
        title='Companies by Market Cap',
        template="plotly_dark"
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Founded year vs Market Cap
    fig2 = px.scatter(
        filtered_df,
        x='Founded',
        y='Market_Cap',
        title='Founded Year vs Market Cap',
        template="plotly_dark",
        size='Employees',
        hover_data=['Company']
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("Market Insights")
    
    # Additional analysis and insights
    st.markdown(f"""
    ### Key Findings
    * Oldest Company: {filtered_df.loc[filtered_df['Founded'].idxmin(), 'Company']} ({filtered_df['Founded'].min()})
    * Newest Company: {filtered_df.loc[filtered_df['Founded'].idxmax(), 'Company']} ({filtered_df['Founded'].max()})
    * Largest Employer: {filtered_df.loc[filtered_df['Employees'].idxmax(), 'Company']} ({int(filtered_df['Employees'].max()):,} employees)
    * Most Common Exchange: {filtered_df['Exchange'].mode().iloc[0]}
    """)