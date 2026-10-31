"""Shared database configuration and data-loading helpers."""

import os
from pathlib import Path

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))


def get_database_connection():
    password = os.getenv("DB_PASSWORD")
    if not password:
        return None

    try:
        port = int(os.getenv("DB_PORT", "5432"))
    except ValueError:
        st.error("DB_PORT must be a valid integer.")
        return None

    return (
        os.getenv("DB_HOST", "localhost"),
        port,
        os.getenv("DB_NAME", "airflow"),
        os.getenv("DB_USER", "airflow"),
        password,
    )


def _load_table(query, host, port, database, user, password):
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password,
        connect_timeout=10,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()


@st.cache_data(ttl=300)
def load_rankings(host, port, database, user, password):
    return _load_table(
        """
        SELECT skill_rank, skill, job_count, jobs_with_skills, percent_of_jobs
        FROM gold.gold_skill_rankings
        ORDER BY skill_rank, skill
        """,
        host,
        port,
        database,
        user,
        password,
    )


@st.cache_data(ttl=300)
def load_location_patterns(host, port, database, user, password):
    return _load_table(
        """
        SELECT
            location_rank,
            location_level,
            location,
            job_count,
            percent_of_level_jobs,
            jobs_with_proposals,
            avg_proposals
        FROM gold.gold_location_patterns
        ORDER BY location_level, location_rank, location
        """,
        host,
        port,
        database,
        user,
        password,
    )


def clear_data_cache():
    load_rankings.clear()
    load_location_patterns.clear()
