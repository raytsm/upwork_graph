import streamlit as st

main_page = st.Page("main_page.py", title="Main Page")
budget_analysis_page = st.Page("budget_analysis.py", title="Budget Analysis")
daily_job_trend_page = st.Page("daily_job_trend.py", title="Daily Job Trend")
hourly_rate_analysis_page = st.Page("hourly_rate_analysis.py", title="Hourly Rate Analysis")
jobs_by_category_page = st.Page("jobs_by_category.py", title="Jobs by Category")
jobs_by_experience_page = st.Page("jobs_by_experience.py", title="Jobs by Experience")

pg = st.navigation([main_page, budget_analysis_page, daily_job_trend_page, hourly_rate_analysis_page, jobs_by_category_page, jobs_by_experience_page])

pg.run()

# conn = st.connection("postgresql", type="sql")

# df = conn.query('SELECT * FROM bronze.ingestion_batches;', ttl="10m")

# for row in df.itertuples():
#     st.write(f"{row.source_file} has hash: {row.source_hash} ingested at: {row.ingested_at}")