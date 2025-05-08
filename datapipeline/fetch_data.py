import aiohttp
import datetime
import json
import asyncio
import os
import psycopg2
from psycopg2.extras import execute_batch

# Ensure the directory exists
os.makedirs('data_pipeline', exist_ok=True)

async def fetch_federal_data():
    today = datetime.date.today()
    url = f"https://www.federalregister.gov/api/v1/documents.json?per_page=100&order=newest&conditions[publication_date][gte]={today - datetime.timedelta(days=7)}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    with open("data_pipeline/raw_data.json", "w") as f:
                        json.dump(data, f, indent=4)
                    print("Data successfully fetched and saved.")
                    await process_and_store(data['documents'])
                else:
                    print(f"Failed to fetch data. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")

async def process_and_store(documents):
    try:
        conn = psycopg2.connect("your_connection_string_here")
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO documents (title, summary, president, publication_date)
        VALUES (%s, %s, %s, %s)
        """
        records = [(doc['title'], doc['summary'], doc['president'], doc['publication_date']) for doc in documents]
        
        execute_batch(cursor, insert_query, records)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")
    except Exception as e:
        print(f"An error occurred while processing and storing data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    asyncio.run(fetch_federal_data())
