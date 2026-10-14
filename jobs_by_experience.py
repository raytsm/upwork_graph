import streamlit as st

st.title(" Jobs by Experience")

conn = st.connection("postgresql", type="sql")

df = conn.query('SELECT * FROM gold.jobs_by_experience;', ttl="10m")

chart_data = (
    df
    .set_index("experience_level")[["fixed_jobs", "hourly_jobs"]]
)

st.bar_chart(
    chart_data,
    stack=True,
    x_label="Experience Level",
    y_label="Number of Jobs",
)

df