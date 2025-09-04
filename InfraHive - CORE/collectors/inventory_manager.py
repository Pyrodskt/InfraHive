from collectors.aws_collector import AWSCollector
from collectors.azure_collector import AzureCollector
from collectors.vcenter_collector import VcenterCollector
from collectors.csv_vcenter_collector import CSVVcenterCollector
from workers.server_worker import ServerWorker # Import ServerWorker
from workers.server_db_worker import DBWorker # Importe le nouveau worker
import json, os
import logging

logger = logging.getLogger(__name__)
class InventoryManager:
    """
    Coordinates inventory collection from multiple sources.
    """
    def __init__(self, settings):
        """
        Initializes the inventory manager and its collectors.
        """
        
        self.settings = settings
        self.collectors = []
        # Initialisation des collecteurs Azure
        for azure_config in self.settings.AZURE_CONFIGS:
            self.collectors.append(AzureCollector(config=azure_config))
            
        # Initialisation des collecteurs Vcenter
        for vc_config in self.settings.VCENTER_CONFIGS:
            self.collectors.append(VcenterCollector(config=vc_config))
            
        # Initialisation des collecteurs CSV
        for csv_config in self.settings.CSV_CONFIGS:
            self.collectors.append(CSVVcenterCollector(config=csv_config))
        
        
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
            logger.debug(f"Données exportées avec succès vers {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'exportation des données pour la source {source_type}: {e}", exc_info=True)
            
    def collect_and_process_all_servers_multithreaded(self):
        """
        Lance un thread de traitement pour chaque source, puis attend leur achèvement.
        """
        logger.info("Démarrage de la collecte et du traitement en parallèle...")
        
        threads = []
        for collector in self.collectors:
            worker = ServerWorker(collector)
            threads.append(worker)
            worker.start()
        
        # Attend que tous les threads se terminent
        for thread in threads:
            thread.join()

        logger.info("Phase de collecte terminée. Récupération des résultats...")
        
        all_inventory = {}
        cloud_provider_data = {}
        for collector in self.collectors:
            all_inventory[collector.source_name] = collector.result
            if collector.source_type == "azure" or collector.source_type == 'aws':
                cloud_provider_data[collector.source_name] = {
                    "subnets": collector.subnets,
                    "ressource_groups": collector.ressource_groups
                }
         # --- NOUVELLE LOGIQUE POUR RÉCUPÉRER LES RÉSULTATS ---
        logger.info("Démarrage de la phase d'insertion dans la base de données en parallèle...")
        self.export_to_json(all_inventory, "all_inventory")
        
        logger.info("Insertion des données de cloud subscriptions dans la base de données...")

        db_threads = []

        for source_type, cloud_data in cloud_provider_data.items():
            # Ne lance un DBWorker que s'il y a des données à insérer
            if cloud_data:
                for data_type, data in cloud_data.items():
                    if data_type == "subnets":
                        # Ici, on spécifie explicitement la méthode à appeler pour ce worker.
                        worker = DBWorker(source_type, data, "upsert_network")
                        db_threads.append(worker)
                        worker.start()
                    if data_type == "ressource_groups":
                        # Ici, on spécifie explicitement la méthode à appeler pour ce worker.
                        worker = DBWorker(source_type, data, "upsert_subscription")
                        db_threads.append(worker)
                        worker.start()
                    
        for thread in db_threads:
            thread.join()
        
        logger.info("Insertions des données de cloud subscriptions terminées.")
        
        db_threads = []

        for source_name, servers_data in all_inventory.items():
            
            # Ne lance un DBWorker que s'il y a des données à insérer
            if servers_data:
                # Ici, on spécifie explicitement la méthode à appeler pour ce worker.
                worker = DBWorker(source_name, servers_data, "insert_server_in_db")
                db_threads.append(worker)
                worker.start()
        
        for thread in db_threads:
            thread.join()
        
        logger.info("Toutes les insertions de serveurs dans la base de données sont terminées.")
        
        db_threads = []

        for source_name, servers_data in all_inventory.items():
            
            # Ne lance un DBWorker que s'il y a des données à insérer
            if servers_data:
                # Ici, on spécifie explicitement la méthode à appeler pour ce worker.
                worker = DBWorker(source_name, servers_data, "insert_networks_of_server")
                db_threads.append(worker)
                worker.start()
        
        for thread in db_threads:
            thread.join()
        
        logger.info("Toutes les insertions de networks dans la base de données sont terminées.")
        
        # Vous pouvez retourner l'inventaire si vous voulez l'utiliser plus tard
        return all_inventory
