import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="Google Ads Dashboard", layout="wide")

# --- BACKGROUND AND STYLING (Dark Starry Blue Theme) ---
st.markdown("""
    <style>
        body {
            background-color: #0d1b2a;
            color: white;
        }
        .stApp {
            background-color: #0d1b2a;
        }
        h1, h2, h3, .stMarkdown {
            color: #f1f6f9;
        }
        .css-1d391kg {
            background-color: #1b263b !important;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df['Ad_Date'] = pd.to_datetime(df['Ad_Date'], errors='coerce')
    return df

df = load_data()

# --- TITLE ---
st.title("📊 Google Ads Campaign Performance Dashboard")

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🔍 Filter Options")
    selected_device = st.multiselect("Select Device(s):", df['Device'].unique(), default=df['Device'].unique())
    selected_location = st.multiselect("Select Location(s):", df['Location'].unique(), default=df['Location'].unique())

# --- FILTERED DATA ---
filtered_df = df[(df['Device'].isin(selected_device)) & (df['Location'].isin(selected_location))]

# --- SECTION 1: Conversion Rate ---
st.subheader("🏆 Top 10 Campaigns by Average Conversion Rate")
top_campaigns = (
    filtered_df.groupby('Campaign_Name')['Conversion Rate']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(x=top_campaigns.values, y=top_campaigns.index, palette="viridis", ax=ax1)
ax1.set_title("Top 10 Campaigns by Conversion Rate", fontsize=14)
ax1.set_xlabel("Conversion Rate")
ax1.set_ylabel("Campaign Name")
st.pyplot(fig1)

# --- SECTION 2: Sales by Device ---
st.subheader("📱 Total Sales Amount by Device")
sales_by_device = filtered_df.groupby('Device')['Sale_Amount'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(x=sales_by_device.index, y=sales_by_device.values, palette="magma", ax=ax2)
ax2.set_title("Sales by Device", fontsize=14)
ax2.set_ylabel("Sales Amount")
ax2.set_xlabel("Device")
st.pyplot(fig2)

# --- SECTION 3: Impressions by Location ---
st.subheader("🌍 Impressions by Location")
top_locations = filtered_df.groupby('Location')['Impressions'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(8, 3))
sns.barplot(x=top_locations.index, y=top_locations.values, palette="coolwarm", ax=ax3)
ax3.set_title("Top 10 Locations by Impressions", fontsize=14)
ax3.set_ylabel("Impressions")
ax3.set_xlabel("Location")
plt.xticks(rotation=45)
st.pyplot(fig3)

# --- SECTION 4: Daily Sales Trend ---
st.subheader("📅 Daily Sales Trend")
daily_sales = filtered_df.groupby('Ad_Date')['Sale_Amount'].sum()

fig4, ax4 = plt.subplots(figsize=(8, 3))
daily_sales.plot(kind='line', marker='o', color='cyan', ax=ax4)
ax4.set_title("Sales Trend Over Time", fontsize=14)
ax4.set_xlabel("Date")
ax4.set_ylabel("Sales Amount")
st.pyplot(fig4)

# --- SECTION 5: Cost vs. Sales Scatterplot ---
st.subheader("💸 Cost vs. Sales Scatterplot")

fig5, ax5 = plt.subplots(figsize=(7, 4))
sns.scatterplot(
    data=filtered_df,
    x='Cost',
    y='Sale_Amount',
    hue='Campaign_Name',
    alpha=0.6,
    palette='tab10',
    ax=ax5
)

sns.regplot(
    data=filtered_df,
    x='Cost',
    y='Sale_Amount',
    scatter=False,
    ax=ax5,
    color='red',
    line_kws={'linewidth': 1.2}
)

ax5.set_title("Cost vs. Sales Amount", fontsize=14)
ax5.set_xlabel("Ad Cost")
ax5.set_ylabel("Sales Amount")
ax5.legend([], [], frameon=False)
st.pyplot(fig5)
