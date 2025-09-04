from connectors.vcenter_connector import Vcenter
from utils.data_normalizer import DataNormalizer # Importation du normalizer central
import logging


# 4. The VcenterCollector is the client of the Factory
class VcenterCollector:
    def __init__(self, config):
        """
        Initializes the VcenterCollector.

        Args:
            config (dict): The configuration dictionary for the vCenter connection.
            logger (Logger): The application logger.
        """
        self.config = config
        self.logger = logging.getLogger(f'{__name__} - {self.config.get('name')}')

        # Création de l'instance du connecteur vCenter, en lui passant la configuration
        self.vcenter_connector = Vcenter(self.config, self.logger)
        self.source_type = self.config.get('type')
        self.source_name = self.config.get('name')
        self.result = []
        self.normalizer = DataNormalizer()

        
    def collect(self):
        """
        Runs the collection process using the Vcenter connector and normalizes the output.
        """
        raw_servers_data = self.vcenter_connector.collect()
        
        if not raw_servers_data:
            self.logger.warning("Aucune donnée brute à normaliser. Retourne une liste vide.")
            return []
            
        normalized_data = []
        for server in raw_servers_data:
            # Normalise chaque serveur individuellement en passant son type de source
            
            normalized_server = self.normalizer.normalize_data(raw_data=server, data_type=self.source_type, config=self.config)
            if normalized_server:
                normalized_data.append(normalized_server)
        
        self.logger.debug(f"Normalisation terminée. {len(normalized_data)} serveurs normalisés.")
        self.result = normalized_data
        return normalized_data
