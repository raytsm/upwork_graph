import streamlit as st

st.title("Budget Analysis")

conn = st.connection("postgresql", type="sql")

df = conn.query('SELECT * FROM gold.budget_analysis;', ttl="10m")

chart_data = (
    df
    .set_index("category")[["avg_budget"]]
    .sort_values("category", ascending=False)
)

st.bar_chart(
    chart_data,
    x_label="Job Category",
    y_label="Average Fixed Budget"
)

df