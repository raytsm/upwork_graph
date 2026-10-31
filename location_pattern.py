"""Location-patterns dashboard page."""

import os

import psycopg2
import streamlit as st

from database import get_database_connection, load_location_patterns


def render_location_patterns():
    st.title("Location Patterns")
    st.caption("Explore locations and proposal patterns in job postings")

    connection = get_database_connection()
    if connection is None:
        if not os.getenv("DB_PASSWORD"):
            st.error("Set DB_PASSWORD in your .env file to load data.")
        return

    try:
        location_patterns = load_location_patterns(*connection)
    except psycopg2.Error as error:
        st.error(f"Could not load gold.gold_location_patterns: {error}")
        return

    if location_patterns.empty:
        st.info(
            "No location patterns found. Build the gold table after the Silver tables are available."
        )
        return

    level_labels = {
        "country": "Country (JSON jobs)",
        "city": "City (JSON jobs)",
        "location": "Location (flat jobs)",
    }
    levels = location_patterns["location_level"].dropna().drop_duplicates().tolist()
    if not levels:
        st.info("No location levels found.")
        return

    selected_level = st.selectbox(
        "Break down locations by",
        levels,
        format_func=lambda level: level_labels.get(level, level.title()),
    )
    locations = location_patterns[
        location_patterns["location_level"] == selected_level
    ].copy()

    location_search = st.text_input("Search locations")
    if location_search:
        locations = locations[
            locations["location"].str.contains(
                location_search,
                case=False,
                na=False,
                regex=False,
            )
        ]

    if locations.empty:
        st.info("No matching locations.")
        return

    location_limit = min(50, len(locations))
    location_top_n = st.slider(
        "Number of locations to show",
        min_value=1,
        max_value=location_limit,
        value=min(20, location_limit),
    )
    displayed_locations = locations.head(location_top_n)

    st.caption(
        "Job share is calculated among jobs with a known location. "
        "Average proposals uses jobs with proposal counts available."
    )
    st.bar_chart(
        displayed_locations.set_index("location")[["job_count"]],
        horizontal=True,
    )
    st.dataframe(
        displayed_locations,
        use_container_width=True,
        hide_index=True,
        column_config={
            "location_rank": st.column_config.NumberColumn("Rank", format="%d"),
            "location_level": st.column_config.TextColumn("Level"),
            "location": st.column_config.TextColumn("Location"),
            "job_count": st.column_config.NumberColumn("Jobs", format="%d"),
            "percent_of_level_jobs": st.column_config.NumberColumn(
                "Share of located jobs", format="%.2f%%"
            ),
            "jobs_with_proposals": st.column_config.NumberColumn(
                "Jobs with proposals", format="%d"
            ),
            "avg_proposals": st.column_config.NumberColumn(
                "Average proposals", format="%.2f"
            ),
        },
    )
    st.download_button(
        "Download displayed location patterns as CSV",
        data=displayed_locations.to_csv(index=False).encode("utf-8"),
        file_name="upwork_location_patterns.csv",
        mime="text/csv",
    )
