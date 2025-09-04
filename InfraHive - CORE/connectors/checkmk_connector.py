import requests
import json
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed


import yaml


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CheckMK:
    def __init__(self, config, logger) -> None:
        
        self.target = config.get('name')
        self.url = config.get('url')
        self.credentials = {
            'username': config.get('username'),
            'password': config.get('password'),
        }

    def connect(self):
        self.session = requests.session()
        self.session.headers['Authorization'] = f"Bearer {self.credentials['username']} {self.credentials['password']}"
        self.session.headers['Accept'] = 'application/json'
        self.session.verify = False

    def get_configs(self):
        with open("config.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        return data
    
    def collect(self): 
        self.connect()
        self.servers = self.getAllHosts().json()

        # self.export_to_json(f"Traitements//Agents//exports//{self.target}-checkmk.json", self.servers['value'])
        return self.servers['value']

    def getAllHosts(self): # Retourne la liste des vm registered sur le checkmk
        return self.session.get(
            f"{self.url}/domain-types/host_config/collections/all",
            params={  # goes into query string
                        "effective_attributes": True,  # Show all effective attributes on hosts, not just the attributes which were set on this host specifically.
                        },
        )
