import urllib3
import json
import requests
from rich.console import Console
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
import yaml

class GLPI:
    def __init__(self, config, logger):
        # self.config = self.get_configs()
        self.config = config
        self.logger = logger
        self.base_url = config.get('base_url')
        self.app_token = config.get('APP_TOKEN')
        self.user_token = config.get('USER_TOKEN')
        self.session_token = ''
        self.headers = {
            "Content-Type": "application/json",
            "App-Token": self.app_token,
            "Authorization": f"user_token {self.user_token}"
        }
        self.params = {}
        self.glpi_computers = None
        
    
    def connect(self):
        try:
            response = requests.post(self.base_url + "initSession", headers=self.headers, params=self.params, verify=False) 
            if response.status_code == 200:
                self.session_token = response.json()['session_token']
                self.headers['Session-Token'] = self.session_token
                self.logger.debug(f'Connection successfull, session_token : {self.session_token}')
            else:
                self.logger.debug('Error in get session request')
            
        except :
            self.console.print('Exception occured')
    
    def get_all_computers(self):
        try:
            self.headers['Accept-Range'] = '1999'
            self.headers['Content-Range'] = "0-2000/2000"
            response = requests.get(f"{self.base_url}/search/Computer?expand_dropdowns=1&range=0-1158", headers=self.headers, verify=False)
            if response.status_code == 200 or response.status_code == 206 :
                # self.export_to_json("Traitements//Agents//exports//glpi.json", response.json())
                self.glpi_computers = response.json()
            else:
                self.logger.error('Error in /search/Computer 1')
        except:
            self.logger.error('Error in /search/Computer 2')
    
    def export_to_json(self, path, data):
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
                self.logger.debug(f"Données exportées avec succès vers {path}")
        except Exception as e:
            self.logger.debug(f"Erreur lors de l'exportation des données JSON: {str(e)}")
            
            
    def collect(self):
        self.connect()
        self.get_all_computers()
        return self.glpi_computers['data']