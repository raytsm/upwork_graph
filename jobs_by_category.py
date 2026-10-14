import streamlit as st

st.title(" Jobs By Category")

conn = st.connection("postgresql", type="sql")

df = conn.query('SELECT * FROM gold.jobs_by_category;', ttl="10m")

chart_data = (
    df
    .set_index("category")[["total_jobs"]]
    .sort_values("total_jobs", ascending=False)
)

st.bar_chart(
    chart_data,
    horizontal=True,
    y_label="Number of Jobs",
    x_label="Job Category",
)

df