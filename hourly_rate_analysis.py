import streamlit as st

st.title(" Hourly Rate Anlysis")

conn = st.connection("postgresql", type="sql")

df = conn.query('SELECT * FROM gold.hourly_rate_analysis;', ttl="10m")

chart_data = (
    df
    .set_index("category")[["avg_min_hourly_rate", "avg_max_hourly_rate"]]
)

st.bar_chart(
    chart_data,
    x_label="Job Category",
    y_label="Average Hourly Rate",
    stack=False
)

df