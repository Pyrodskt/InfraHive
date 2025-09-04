import pyodbc
from config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class SqlConnector:
    def __init__(self, db_source: str):
        """
        Initializes the SqlConnector with database configuration based on the provided source.

        Args:
            db_source (str): The database source, either 'OEIL' or 'HOSTING'.

        Raises:
            ValueError: If an unknown DB source is provided.
        """
        self.config = Settings()
        if db_source.upper() == 'OEIL':
            self.server = self.config.OEIL_SERVER
            self.database = self.config.OEIL_DB
            self.username = self.config.OEIL_DB_USER
            self.password = self.config.OEIL_DB_USER_PWD
        elif db_source.upper() == 'HOSTING':
            self.server = self.config.HOSTING_SERVER
            self.database = self.config.HOSTING_DB
            self.username = self.config.HOSTING_DB_USER
            self.password = self.config.HOSTING_DB_USER_PWD
        else:
            logger.error(f"Unknown DB source '{db_source}'. Expected 'OEIL' or 'HOSTING'.")
        
        self.connect_obj = self.connect()
        
    def connect(self):
        """
        Establishes a connection to the SQL database using the configured parameters.

        Returns:
            pyodbc.Connection: The database connection object if successful, None otherwise.
        """
        connection_string = (
            'DRIVER={SQL Server};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password}'
        )
        try:
            cnxn = pyodbc.connect(connection_string)
            if cnxn:
                #print('DB Connection successfull')
                return cnxn
        except Exception as e:
            logger.error('/!\ Error during db connection', e)