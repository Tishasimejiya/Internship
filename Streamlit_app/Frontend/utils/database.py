# Frontend/utils/database.py
import psycopg2
from psycopg2 import pool
import os
from utils.logger import app_logger


# Database connection pool
db_pool = None


def init_db_pool():
    """Initialize database connection pool"""
    global db_pool
    if db_pool is None:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                host=os.getenv("DB_HOST", "postgres-db"),
                port=int(os.getenv("DB_PORT", "5432")),
                database=os.getenv("DB_NAME", "registration_db"),
                user=os.getenv("DB_USER", "admin"),
                password=os.getenv("DB_PASSWORD", "")
            )
            app_logger.info("✅ Database connection pool initialized")
        except Exception as e:
            app_logger.error(f"❌ Failed to initialize database pool: {e}")
            raise


def get_db_connection():
    """Get a connection from the pool"""
    init_db_pool()
    return db_pool.getconn()


def release_db_connection(conn):
    """Return connection to the pool"""
    db_pool.putconn(conn)


def save_registration_to_db(name, email, registration_date, file_path=None):
    """Save registration to PostgreSQL database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO registrations (name, email, phone, created_at, file_path) VALUES (%s, %s, %s, NOW(), %s)",
            (name, email, registration_date, file_path)
        )
        conn.commit()
        cursor.close()
        app_logger.info(f"✅ Saved to database: {name} ({email}) - File: {file_path}")
        return True
    except Exception as e:
        conn.rollback()
        app_logger.error(f"❌ Database save failed: {e}")
        return False
    finally:
        release_db_connection(conn)


def get_all_registrations():
    """Fetch all registrations from database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, phone, created_at, file_path FROM registrations ORDER BY created_at DESC"
        )
        data = cursor.fetchall()
        cursor.close()
        app_logger.info(f"📊 Fetched {len(data)} registrations from database")
        return data
    except Exception as e:
        app_logger.error(f"❌ Database fetch failed: {e}")
        return []
    finally:
        release_db_connection(conn)


def get_registration_count():
    """Get total number of registrations"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM registrations")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except Exception as e:
        app_logger.error(f"❌ Failed to get count: {e}")
        return 0
    finally:
        release_db_connection(conn)
