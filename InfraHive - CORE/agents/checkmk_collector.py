import logging
from connectors.checkmk_connector import CheckMK
from utils.data_normalizer import DataNormalizer # Importation du normalizer central


class CheckMKCollector:
    def __init__(self, config):
        self.config = config
        self.collector_type = self.config.get('type')
        self.collector_name = f"{self.collector_type.upper()} - {self.config.get('name')}"
        self.logger = logging.getLogger(f'{self.collector_name}')
        self.checkmk_connector = CheckMK(self.config, self.logger)
        self.result = []
        self.normalizer = DataNormalizer()




    def collect(self):
        servers_data = self.checkmk_connector.collect()

        if not servers_data:
            self.logger.info("Aucune donnée brute à normaliser. Retourne une liste vide.")
            return []
            
        normalized_data = []
        for server in servers_data:
            # Normalise chaque serveur individuellement en passant son type de source
            
            normalized_server = self.normalizer.normalize_data(raw_data=server, data_type=self.collector_type, config=self.config)
            normalized_data.append(normalized_server)
        
        self.logger.info(f"Normalisation terminée. {len(normalized_data)} serveurs normalisés.")
        self.result = normalized_data
        return normalized_data