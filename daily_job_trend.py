import streamlit as st
import pandas as pd

st.title("Daily Job Trend")

conn = st.connection("postgresql", type="sql")

df = conn.query("""
    SELECT *
    FROM gold.daily_job_trends
    ORDER BY posted_day
""", ttl="10m")

df["posted_day"] = pd.to_datetime(df["posted_day"])

chart_data = (
    df
    .set_index("posted_day")[
        ["total_jobs", "fixed_jobs", "hourly_jobs"]
    ]
)

st.bar_chart(
    df,
    x="posted_day",
    y=["fixed_jobs", "hourly_jobs"],
    stack=True,
    x_label="Posting Date",
    y_label="Number of Jobs"
)

df