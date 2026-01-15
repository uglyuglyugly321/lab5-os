import psycopg2
import os

DB_HOST = os.getenv("DB_HOST", "host.docker.internal")
DB_NAME = os.getenv("DB_NAME", "hotel")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1488")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def list_hotels():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM hotel")  # берем все записи
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_hotel(name, city):
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO hotel (name, city) VALUES (%s, %s) RETURNING id", (name, city))
    hotel_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return hotel_id