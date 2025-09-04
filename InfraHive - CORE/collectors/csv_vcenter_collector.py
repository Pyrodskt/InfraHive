from utils.data_normalizer import DataNormalizer # Importation du normalizer central
from connectors.csv_vcenter_connector import CSVVcenterConnector
import logging

logger = logging.getLogger(__name__)

# 4. The VcenterCollector is the client of the Factory
class CSVVcenterCollector:
    def __init__(self, config):
        """
        Initializes the VcenterCollector.

        Args:
            config (dict): The configuration dictionary for the vCenter connection.
            logger (Logger): The application logger.
        """
        self.config = config
        # Création de l'instance du connecteur vCenter, en lui passant la configuration
        self.csv_vcenter_connector = CSVVcenterConnector(self.config.get('filepath'))
        self.source_type = self.config.get('type')
        self.source_name = self.config.get('name')
        self.normalizer = DataNormalizer()
        self.result = []
        
    def collect(self):
        """
        Runs the collection process using the Vcenter connector and normalizes the output.
        """
        raw_servers_data = self.csv_vcenter_connector.collect()
        
        if not raw_servers_data:
            logger.warning("Aucune donnée brute à normaliser. Retourne une liste vide.")
            return []
            
        normalized_data = []
        for server in raw_servers_data:
            # Normalise chaque serveur individuellement en passant son type de source
            
            normalized_server = self.normalizer.normalize_data(raw_data=server, data_type=self.source_type, config=self.config)
            normalized_data.append(normalized_server)
        
        logger.debug(f"Normalisation terminée. {len(normalized_data)} serveurs normalisés.")
        self.result = normalized_data
        return normalized_data
