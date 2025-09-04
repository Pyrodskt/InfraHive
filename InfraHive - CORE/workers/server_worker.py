# workers/server_worker.py
import threading, os, json
import logging

logger = logging.getLogger(__name__)
class ServerWorker(threading.Thread):
    """
    Worker thread responsable du traitement de serveurs pour une source spécifique.
    Il est conçu pour être exécuté en parallèle pour chaque source de données.
    """
    def __init__(self, collector):
        """
        Initialise le ServerWorker.

        Args:
            source_type (str): Le type de la source (e.g., "aws", "vcenter", "azure").
            servers (list): Une liste de dictionnaires de serveurs à traiter.
        """
        super().__init__()
        self.collector = collector
        self.result = []

    def export_to_json(self, data: list, source_type: str):
        """
        Exporte les données normalisées dans un fichier JSON dédié à la source.
        """
        output_dir = "exports"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        file_path = os.path.join(output_dir, f"{source_type}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.debug(f"Données normalisées pour '{source_type}' exportées avec succès vers {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'exportation des données pour la source {source_type}: {e}", exc_info=True)
    
    def run(self):
        """
        Exécute la logique de collecte et de traitement pour une source spécifique.
        """
        logger.info(f"Démarrage de la collecte et du traitement pour la source : {self.collector.source_name}")
        
        try:
            # La méthode `collect` du collecteur retourne les données normalisées
            servers_data = self.collector.collect()
            
            if not servers_data:
                logger.warning(f"Aucune donnée à traiter pour la source : {self.collector.source_name}")
                return
            
            logger.info(f"Collecte terminée : {len(servers_data)} serveurs trouvés pour la source : {self.collector.source_name}")
            
            # Appel de la nouvelle méthode d'exportation
            self.export_to_json(servers_data, self.collector.source_name)
            
            # Stockage du résultat pour que le thread principal puisse le récupérer (facultatif, mais garde la compatibilité)
            self.result = {self.collector.source_name: servers_data}
            
        except Exception as e:
            logger.error(f"Erreur dans le thread du collecteur {self.collector.source_name} : {e}", exc_info=True)