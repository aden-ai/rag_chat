import os
import sys
import streamlit as st

# Add the directory above the current directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions
from datapipeline.fetch_data import fetch_federal_data
from datapipeline.process_and_store import process_and_store

def main():
    st.write("Starting the federal data fetch and processing...")

    try:
        # Fetch federal data
        st.write("Fetching federal data...")
        fetch_federal_data()  # Fetch data from the Federal Register
        st.write("Data successfully fetched.")

        # Process and store the data
        st.write("Processing and storing data...")
        process_and_store()  # Process and store data into the database
        st.write("Data successfully processed and stored.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
