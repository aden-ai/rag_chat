import json
import psycopg2
from database.db_connection import get_connection

def process_and_store():
    try:
        # Load data from the fetched JSON file
        with open("data_pipeline/raw_data.json", "r") as f:
            data = json.load(f)['results']

        # Get database connection
        conn = get_connection()
        if conn is None:
            print("Database connection failed.")
            return

        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Documents (
                id VARCHAR(255) PRIMARY KEY,
                title TEXT,
                summary TEXT,
                publication_date DATE,
                president TEXT
            )
        """)

        # Insert data into the database
        for item in data:
            cursor.execute("""
                REPLACE INTO Documents (id, title, summary, publication_date, president) 
                VALUES (%s, %s, %s, %s, %s)
            """, (
                item.get('document_number'),
                item.get('title'),
                item.get('abstract'),
                item.get('publication_date'),
                item.get('president', 'unknown')
            ))

        conn.commit()
        cursor.close()
        conn.close()
        print("Data successfully processed and stored.")
    except Exception as e:
        print(f"An error occurred during processing and storing data: {e}")
