import sys
import os

# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import Settings
from db.connection_pool import ConnectionPool
import logging

# Configure basic logging for the test script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_connection_pool():
    """
    Tests the functionality of the ConnectionPool by:
    1. Initializing Settings.
    2. Initializing ConnectionPool with database configurations.
    3. Attempting to get and release a connection.
    4. Executing a simple query to verify the connection.
    5. Closing all connections in the pool.

    Returns:
        bool: True if all tests pass, False otherwise.
    """
    logger.info("Starting ConnectionPool functionality test...")
    settings = None
    connection_pool = None
    conn = None

    try:
        # 1. Instantiate Settings
        logger.info("Initializing Settings...")
        settings = Settings()
        logger.info("Settings initialized.")

        # Prepare db_config from settings
        db_config = {
            "driver": "ODBC Driver 17 for SQL Server", # Assuming this is correct, should be in settings eventually
            "server": settings.HOSTING_SERVER,
            "database": settings.HOSTING_DB,
            "username": settings.HOSTING_DB_USER,
            "password": settings.HOSTING_DB_USER_PWD
        }

        # Check if essential DB settings are available
        if not all([db_config['server'], db_config['database'], db_config['username'], db_config['password']]):
            logger.error("Missing essential database configuration in settings. Please check .env and config.yaml.")
            return False

        # 2. Instantiate ConnectionPool
        logger.info(f"Initializing ConnectionPool with pool size: {settings.THREAD_POOL_SIZE}...")
        connection_pool = ConnectionPool(db_config, pool_size=settings.THREAD_POOL_SIZE)
        logger.info("ConnectionPool initialized.")

        # 3. Attempt to get a connection
        logger.info("Attempting to get a connection from the pool...")
        conn = connection_pool.get_connection()
        if conn:
            logger.info("Successfully got a connection.")
            # Optional: Try to execute a simple query to verify connection
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info(f"Simple query executed successfully: {result}")
            except Exception as e:
                logger.error(f"Error executing simple query: {e}")
                return False
        else:
            logger.error("Failed to get a connection from the pool.")
            return False

        # 4. Attempt to release the connection
        logger.info("Attempting to release the connection back to the pool...")
        connection_pool.release_connection(conn)
        logger.info("Connection successfully released.")
        conn = None # Clear reference after releasing

        logger.info("ConnectionPool functionality test completed successfully.")
        return True

    except Exception as e:
        logger.error(f"An unexpected error occurred during test: {e}")
        return False
    finally:
        # 5. Attempt to close all connections in the pool
        if connection_pool:
            logger.info("Attempting to close all connections in the pool...")
            connection_pool.close_all()
            logger.info("All connections closed.")

if __name__ == "__main__":
    if test_connection_pool():
        logger.info("ConnectionPool test PASSED.")
    else:
        logger.error("ConnectionPool test FAILED.")
