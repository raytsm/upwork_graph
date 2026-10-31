"""Streamlit entry point for the skills and location dashboards."""

import streamlit as st

from database import clear_data_cache
from location_pattern import render_location_patterns
from skills_ranking import render_skill_rankings

st.set_page_config(
    page_title="Upwork Skills & Location Dashboard",
    page_icon="📊",
    layout="wide",
)

if st.sidebar.button("Reload data"):
    clear_data_cache()

page = st.navigation(
    [
        st.Page(render_skill_rankings, title="Skill Rankings", default=True),
        st.Page(render_location_patterns, title="Location Patterns"),
    ]
)
page.run()
