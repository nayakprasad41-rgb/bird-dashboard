import streamlit as st
import pandas as pd
import plotly.express as px
# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Bird Species Dashboard", layout="wide")

st.title("🐦 Bird Species Observation Analysis Dashboard")
# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Bird_Data.csv")
    return df

df = load_data()
# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

habitat_filter = st.sidebar.multiselect(
    "Select Habitat",
    options=df['Habitat'].unique(),
    default=df['Habitat'].unique()
)

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['Year'].dropna().unique()),
    default=sorted(df['Year'].dropna().unique())
)

species_filter = st.sidebar.multiselect(
    "Select Species",
    options=df['Common_Name'].unique(),
    default=df['Common_Name'].unique()[:10]
)

# Apply filters
filtered_df = df[
    (df['Habitat'].isin(habitat_filter)) &
    (df['Year'].isin(year_filter)) &
    (df['Common_Name'].isin(species_filter))
]

# -------------------------------
# KPI METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Observations", len(filtered_df))
col2.metric("Total Species", filtered_df['Common_Name'].nunique())
col3.metric("Total Locations", filtered_df['Site_Name'].nunique())

st.markdown("---")

# -------------------------------
# TOP SPECIES
# -------------------------------
st.subheader("📊 Top 10 Bird Species")

top_species = filtered_df['Common_Name'].value_counts().head(10).reset_index()
top_species.columns = ['Species', 'Count']

fig1 = px.bar(top_species, x='Species', y='Count', title="Top 10 Species")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# HABITAT DISTRIBUTION
# -------------------------------
st.subheader("🌿 Habitat Distribution")

habitat_dist = filtered_df['Habitat'].value_counts().reset_index()
habitat_dist.columns = ['Habitat', 'Count']

fig2 = px.pie(habitat_dist, names='Habitat', values='Count')
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# MONTHLY TREND
# -------------------------------
st.subheader("📈 Monthly Observation Trend")

monthly = filtered_df.groupby('Month')['Common_Name'].count().reset_index()
monthly.columns = ['Month', 'Observations']

fig3 = px.line(monthly, x='Month', y='Observations', markers=True)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# WEATHER IMPACT
# -------------------------------
st.subheader("☁️ Weather Impact (Sky Condition)")

sky = filtered_df['Sky'].value_counts().reset_index()
sky.columns = ['Sky', 'Observations']

fig4 = px.bar(sky, x='Sky', y='Observations')
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# DISTANCE ANALYSIS
# -------------------------------
st.subheader("📏 Distance Analysis")

distance = filtered_df['Distance'].value_counts().reset_index()
distance.columns = ['Distance', 'Observations']

fig5 = px.bar(distance, x='Distance', y='Observations')
st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# TEMPERATURE VS COUNT
# -------------------------------
st.subheader("🌡️ Temperature vs Bird Count")

fig6 = px.scatter(
    filtered_df,
    x='Temperature',
    y='Initial_Three_Min_Cnt',
    color='Habitat'
)

st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# CONSERVATION (WATCHLIST)
# -------------------------------
st.subheader("🚨 Watchlist Species")

watchlist = filtered_df[filtered_df['PIF_Watchlist_Status'] == True]

if not watchlist.empty:
    watch_species = watchlist['Common_Name'].value_counts().head(10).reset_index()
    watch_species.columns = ['Species', 'Count']

    fig7 = px.bar(watch_species, x='Species', y='Count')
    st.plotly_chart(fig7, use_container_width=True)
else:
    st.write("No watchlist species found in selected filters.")

# -------------------------------
# RAW DATA VIEW
# -------------------------------
st.subheader("📄 Raw Data")

st.dataframe(filtered_df.head(100))

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("✅ Project by Prasad Nayak | Bird Species Analysis Dashboard")

