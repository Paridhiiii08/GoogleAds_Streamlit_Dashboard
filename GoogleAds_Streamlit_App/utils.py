
import pandas as pd

def clean_data(df):
    # Clean and standardize column names
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("(", "").str.replace(")", "").str.title()

    # Rename commonly mismatched column names
    if "Campaign_Name" in df.columns:
        df.rename(columns={"Campaign_Name": "Campaign"}, inplace=True)
    if "Sales_Amount" in df.columns:
        df.rename(columns={"Sales_Amount": "Sales"}, inplace=True)

    # Ensure essential columns exist before processing
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if "Clicks" in df.columns and "Impressions" in df.columns:
        df["Ctr"] = (df["Clicks"] / df["Impressions"]) * 100
    if "Cost" in df.columns and "Clicks" in df.columns:
        df["Cpc"] = df["Cost"] / df["Clicks"]
    if "Conversions" in df.columns and "Clicks" in df.columns:
        df["Conversion_Rate"] = (df["Conversions"] / df["Clicks"]) * 100

    return df

def calculate_kpis(df):
    impressions = int(df["Impressions"].sum()) if "Impressions" in df.columns else 0
    clicks = int(df["Clicks"].sum()) if "Clicks" in df.columns else 0
    conversions = int(df["Conversions"].sum()) if "Conversions" in df.columns else 0
    ctr = round((clicks / impressions) * 100, 2) if impressions else 0
    cpc = round((df["Cost"].sum() / clicks), 2) if clicks else 0
    conv_rate = round((conversions / clicks) * 100, 2) if clicks else 0
    return {
        "Impressions": impressions,
        "Clicks": clicks,
        "Conversions": conversions,
        "CTR": ctr,
        "CPC": cpc,
        "Conversion Rate": conv_rate
    }
