from utils.data_normalizer import DataNormalizer
from connectors.azure_connector import AzureConnector
import logging, os, json

logger = logging.getLogger(__name__)
class AzureCollector:
    def __init__(self, config):
        """
        Initializes the AzureCollector.
        """
        self.config = config
        self.logger = logging.getLogger(f'{__name__} - {self.config.get('name')}')
        self.source_type = self.config.get('type')
        self.source_name = self.config.get('name')
        # Création de l'instance du connecteur vCenter, en lui passant la configuration
        self.azure_connector = AzureConnector(self.config, self.logger)
        self.normalizer = DataNormalizer()
        self.result = []
        self.subnets = []
        self.ressource_groups = []
    def export_to_json(self, data: list, filename: str):
        """
        Exporte les données normalisées dans un fichier JSON dédié à la source.
        """
        output_dir = "exports"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        file_path = os.path.join(output_dir, f"{filename}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.debug(f'Donnée exportées avec succès dans le fichier {file_path}')
        except Exception as e:
            logger.error(f"Erreur lors de l'exportation des données dans le fichier {file_path}: {e}", exc_info=True)
    
    def collect(self):
        """
        Collects server information from Azure.

        Returns:
            list: A list of dictionaries, where each dictionary represents an Azure server.
        """
        raw_servers_data = self.azure_connector.collect()
        
        if not raw_servers_data:
            self.logger.warning("Aucune donnée brute à normaliser. Retourne une liste vide.")
            return []
            
        normalized_data = []
        for server in raw_servers_data['servers']:
            # Normalise chaque serveur individuellement en passant son type de source
            
            normalized_server = self.normalizer.normalize_data(raw_data=server, data_type='azure', config=self.config)
            normalized_data.append(normalized_server)
        
        self.export_to_json(raw_servers_data['subnets'], f'{self.source_name}_subnets')
        self.export_to_json(raw_servers_data['ressource_groups'], f'{self.source_name}_ressource_groups')
        self.subnets = raw_servers_data['subnets']
        self.ressource_groups = raw_servers_data['ressource_groups']
        self.logger.debug(f"Normalisation terminée. {len(normalized_data)} serveurs normalisés.")
        self.result = normalized_data
        return normalized_data
