import os
import requests
from dotenv import load_dotenv

class Cortex:
    def __init__(self) -> None:
        """
        Initializes the Cortex connector, loading API URL, key ID, and key from environment variables.
        """
        load_dotenv()
        self.url = os.getenv("CORTEX_URL")
        self.headers = {'x-xdr-auth-id':os.getenv("CORTEX_KEY_ID"), 'Authorization': os.getenv("CORTEX_KEY"), 'Content-Type': 'application/json', 'Cookie': 'XSRF-TOKEN=AOeqUzy1Y23tX9XVbZaammEmMZSUfNgjvsgKBlUNxqgAjDuJO7oOnxJJVTdJmv8kfUWiGIC7jHGpPial94om2dolSaU8mLDzvov04dC930YCEyhkialn5E6ePLg51NRz'}