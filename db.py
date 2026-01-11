import psycopg2
import psycopg2.pool
from config import DATABASE_URL

pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL
)

def get_conn():
    return pool.getconn()

def release_conn(conn):
    pool.putconn(conn)

def query(sql, params=None, fetchone=False, fetchall=False):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        if fetchone:
            return cur.fetchone()
        if fetchall:
            return cur.fetchall()
        conn.commit()
    finally:
        cur.close()
        release_conn(conn)
