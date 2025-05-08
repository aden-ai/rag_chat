# File: db_queries.py
import psycopg2

def get_executive_orders_by_president(president: str, month: str):
    conn = psycopg2.connect("your_connection_string_here")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, summary
        FROM documents
        WHERE president = %s
        AND EXTRACT(MONTH FROM publication_date) = %s
    """, (president, month))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return str(results)

