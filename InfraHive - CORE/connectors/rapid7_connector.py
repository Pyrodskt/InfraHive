import os, json, requests
from datetime import datetime
from dotenv import load_dotenv
import concurrent.futures

class Rapid7:
    def __init__(self, config, logger, servers) -> None:
        """
        Initializes the Rapid7 connector, loading API URL and key from environment variables.
        """
        self.config = config
        self.logger = logger
        self.servers = servers
        self.url = self.config.get('url')
        self.headers = {'Authorization': f"Basic {self.config.get('rapid7_key')}", 'Content-Type': 'application/json'}
        
    def collect(self):
        all_servers_info = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
                # Utilise executor.map pour soumettre la tâche pour chaque serveur.
                # 'map' applique la fonction 'query_rapid7_by_server' à chaque élément de 'self.servers'.
                # Note: On passe l'instance de la classe ('self') et l'objet 'server' à la fonction.
                # L'objet 'server' est passé via une expression lambda pour simplifier l'appel.
                futures = {executor.submit(self.query_rapid7_by_server, server.server_name): server for server in self.servers}
                
                for future in concurrent.futures.as_completed(futures):
                    server = futures[future]
                    try:
                        server_info = future.result()
                        if server_info:
                            all_servers_info.append(server_info)
                        else:
                            self.logger.debug(f"Aucune donnée trouvée sur Rapid7 pour le serveur {server.server_name}.")
                    except Exception as exc:
                        self.logger.error(f"Erreur lors de la requête Rapid7 pour le serveur {server.server_name}: {exc}")
        self.logger.info(f"Collecte Rapid7 terminée. {len(all_servers_info)} serveurs traités avec succès.")
        return all_servers_info
    
    
    def query_rapid7_by_server(self, name: str):
        """
        Queries the Rapid7 API for server information based on the server name.

        Args:
            name (str): The name of the server to query.

        Returns:
            dict or None: A dictionary containing server information (hostname, ip, is_installed, riskScore)
                          if found, otherwise None.
        """
        tdy = datetime.now().strftime('%Y-%m-%d')
        payload = json.dumps({
            "filters": [
                {
                    "field": "host-name",
                    "operator": "is",
                    "value": f"{name}"
                }
            ],
            "match": "all"
        })
        
        try:
            response = requests.request("POST", self.url, headers=self.headers, data=payload, verify=False)
            response.raise_for_status()
            data = response.text
            dict_data = json.loads(data)

            is_installed = False
            if dict_data.get('resources'):
                for resource in dict_data['resources']:
                    try:
                        for _id in resource.get('ids', []):
                            if _id.get('source') == 'R7 Agent':
                                is_installed = True
                                break
                        has_agent_data = {
                            "hostname": name,
                            "ip": resource.get('ip'),
                            "is_installed": is_installed,
                            "riskScore": resource.get('riskScore')
                        }
                        return has_agent_data
                    except Exception as e:
                        self.logger.warning(f"Erreur de traitement des données pour le serveur {name}: {e}")
                        continue
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur de requête HTTP pour le serveur {name}: {e}")
        except json.JSONDecodeError:
            self.logger.error(f"Erreur de décodage JSON pour le serveur {name}.")
        except Exception as e:
            self.logger.error(f"Erreur inattendue pour le serveur {name}: {e}")
        
        return None