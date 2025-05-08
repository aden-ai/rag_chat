import psycopg2
import streamlit as st
from urllib.parse import urlparse

def get_connection():
    try:
        # Extract the database URL from secrets
        db_url = st.secrets["postgres"]["url"]

        # Parse the URL
        result = urlparse(db_url)

        # Connect to PostgreSQL using parsed URL
        conn = psycopg2.connect(
            host=result.hostname,
            port=result.port,
            user=result.username,
            password=result.password,
            dbname=result.path[1:],  # Remove the leading '/'
            sslmode="require"
        )

        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None
