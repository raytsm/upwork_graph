"""Skills-ranking dashboard page."""

import os

import pandas as pd
import psycopg2
import streamlit as st

from database import get_database_connection, load_rankings


def render_skill_rankings():
    st.title("Skill Rankings")
    st.caption("Most frequently requested skills in Upwork job postings")

    connection = get_database_connection()
    if connection is None:
        if not os.getenv("DB_PASSWORD"):
            st.error("Set DB_PASSWORD in your .env file to load data.")
        return

    try:
        rankings = load_rankings(*connection)
    except psycopg2.Error as error:
        st.error(f"Could not load gold.gold_skill_rankings: {error}")
        return

    if rankings.empty:
        st.warning("No skill rankings found. Make sure the gold table has been built.")
        return

    rankings["skill"] = rankings["skill"].astype(str)
    rankings["job_count"] = pd.to_numeric(rankings["job_count"])
    rankings["jobs_with_skills"] = pd.to_numeric(rankings["jobs_with_skills"])
    rankings["percent_of_jobs"] = pd.to_numeric(rankings["percent_of_jobs"])

    total_jobs = int(rankings["jobs_with_skills"].iloc[0])
    top_skill = rankings.iloc[0]

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Skills ranked", f"{len(rankings):,}")
    metric2.metric("Jobs with skills", f"{total_jobs:,}")
    metric3.metric("Top skill", top_skill["skill"].title())

    st.subheader("Most requested skills")
    max_skills = min(50, len(rankings))
    min_skills = min(5, max_skills)
    top_n = st.slider(
        "Number of skills to show",
        min_value=min_skills,
        max_value=max_skills,
        value=min(20, max_skills),
    )
    skill_search = st.text_input("Search skills")

    filtered_skills = rankings
    if skill_search:
        filtered_skills = filtered_skills[
            filtered_skills["skill"].str.contains(
                skill_search, case=False, na=False, regex=False
            )
        ]

    displayed_skills = filtered_skills.head(top_n)
    st.bar_chart(displayed_skills.set_index("skill")[["job_count"]], horizontal=True)
    st.subheader("Skill ranking details")
    st.dataframe(
        displayed_skills,
        use_container_width=True,
        hide_index=True,
        column_config={
            "skill_rank": st.column_config.NumberColumn("Rank", format="%d"),
            "skill": st.column_config.TextColumn("Skill"),
            "job_count": st.column_config.NumberColumn("Jobs", format="%d"),
            "jobs_with_skills": st.column_config.NumberColumn(
                "Jobs with skills", format="%d"
            ),
            "percent_of_jobs": st.column_config.NumberColumn(
                "% of jobs", format="%.2f%%"
            ),
        },
    )
    st.download_button(
        "Download displayed skill rankings as CSV",
        data=displayed_skills.to_csv(index=False).encode("utf-8"),
        file_name="upwork_skill_rankings.csv",
        mime="text/csv",
    )
