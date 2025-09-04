# managers/agent_manager.py

import logging, os, json
from workers.server_agents_worker import ServerAgentsWorker
from agents.checkmk_collector import CheckMKCollector
from agents.glpi_collector import GLPICollector
from agents.rapid7_collector import Rapid7Collector
from workers.server_db_worker import DBWorker
from db.db_connector import DBQueries, SessionLocal
logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self, settings):
        self.settings = settings
        self.collectors = []
        
        self.all_servers = self.get_servers_list()
        
        for chmk_config in self.settings.CHECK_MK_CONFIGS:
            self.collectors.append(CheckMKCollector(config=chmk_config))
            
        for glpi_config in self.settings.GLPI_CONFIGS:
            self.collectors.append(GLPICollector(config=glpi_config))
        
        # for rapid7_config in self.settings.RAPID7_CONFIGS:
        #     self.collectors.append(Rapid7Collector(config=rapid7_config, servers=self.all_servers))
        
    
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
            logger.info(f"Données exportées avec succès vers {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'exportation des données pour la source {source_type}: {e}", exc_info=True)
              
    def get_servers_list(self):
        all_servers = []
        
        db_queries = DBQueries(SessionLocal())
        
        # Obtient la méthode à appeler dynamiquement
        # Par exemple, si self.action_method_name est "insert_server_in_db",
        # `action_method` devient une référence à db_queries.insert_server_in_db
        
        all_servers = db_queries.get_all_servers()
        return all_servers
            
        
    
    def get_server_agent_info(self, server_name, agent_name):
         with SessionLocal() as session:
            try:
                db_queries = DBQueries(session)
                
                # Obtient la méthode à appeler dynamiquement
                # Par exemple, si self.action_method_name est "insert_server_in_db",
                # `action_method` devient une référence à db_queries.insert_server_in_db
                
                res = db_queries.get_required_agents_to_check(server_name=server_name, agent_name=agent_name)
                logger.debug(f"Récupération réussie pour {server_name} dans la table server_has_agents ({server_name} - {agent_name}).")
                self.success = True
            except Exception as e:
                logger.error(f"Erreur lors de la récupération du serveur {server_name} dans la table server_has_agents : {e}", exc_info=True)
            finally:
                session.close()
                return res
                
    def update_agent_info(self, server_name, agent_name, status):
        with SessionLocal() as session:
            try:
                db_queries = DBQueries(session)
                
                # Obtient la méthode à appeler dynamiquement
                # Par exemple, si self.action_method_name est "insert_server_in_db",
                # `action_method` devient une référence à db_queries.insert_server_in_db
                
                db_queries.upsert_agent_db(server_name=server_name, agent_name=agent_name, status=status)
                session.commit() # Effectue le commit une seule fois pour tout le lot
                logger.debug(f"Insertion réussie pour {server_name} dans la table server_has_agents ({server_name} - {agent_name} - {status}).")
                self.success = True
            except Exception as e:
                logger.error(f"Erreur lors de l'upsert du serveur {server_name} dans la table server_has_agents : {e}", exc_info=True)
                session.rollback()
            finally:
                session.close()
                
    def update_risk_score(self, server_name, riskScore): 
        with SessionLocal() as session:
            try:
                db_queries = DBQueries(session)
                
                # Obtient la méthode à appeler dynamiquement
                # Par exemple, si self.action_method_name est "insert_server_in_db",
                # `action_method` devient une référence à db_queries.insert_server_in_db
                
                db_queries.update_r7_riskscore(server_name=server_name, r7_risk_score=riskScore)
                session.commit() # Effectue le commit une seule fois pour tout le lot
                logger.debug(f"Update réussi pour le riskScore du serveur {server_name} dans la table server ({server_name} - {riskScore}).")
                self.success = True
            except Exception as e:
                logger.error(f"Erreur lors de l'update du riskScore du serveur {server_name} dans la table server : {e}", exc_info=True)
                session.rollback()
            finally:
                session.close()
                
    def upsert_networks(self, server_name, ip_address, netw_name):
        with SessionLocal() as session:
            try:
                db_queries = DBQueries(session)
                
                # Obtient la méthode à appeler dynamiquement
                # Par exemple, si self.action_method_name est "insert_server_in_db",
                # `action_method` devient une référence à db_queries.insert_server_in_db
                
                db_queries.upsert_network_db(server_name=server_name, ip_addr=ip_address, netw_name=netw_name)
                session.commit() # Effectue le commit une seule fois pour tout le lot
                logger.debug(f"Update réussi pour l'adresse ip du serveur {server_name} dans la table server_has_network ({server_name} - {ip_address} - {netw_name}).")
                self.success = True
            except Exception as e:
                logger.error(f"Erreur lors de l'update de l'adresse ip du serveur {server_name} dans la table server_has_network : {e}", exc_info=True)
                session.rollback()
            finally:
                session.close()

    def collect_and_process_all_servers_multithreaded(self):
        """
        Lance un thread de traitement pour chaque source, puis attend leur achèvement.
        Optimise la phase de traitement en restructurant les données pour un accès rapide.
        """
        logger.info("Démarrage de la collecte et du traitement en parallèle...")
        
        # 1. Lancement et attente des threads (cette partie est déjà bonne)
        all_in_one_threads = []
        for collector in self.collectors:
            worker = ServerAgentsWorker(collector)
            all_in_one_threads.append(worker)
            worker.start()
        
        for thread in all_in_one_threads:
            thread.join()
            
        logger.info("Collecte terminée. Démarrage de la consolidation des données.")
        
        # 2. Consolider et restructurer les données pour un accès rapide
        # La clé de ce dictionnaire sera le nom court du serveur
        unified_agent_data = {server.server_name: {} for server in self.all_servers}

        # Créer une liste de tous les noms de serveurs courts pour une recherche rapide
        server_names_set = {server.server_name for server in self.all_servers}
        
        for collector in self.collectors:
            # Pour chaque élément collecté, essayez de trouver le nom de serveur court
            for agent_data in collector.result:
                # On utilise le nom de l'agent qui pourrait être un FQDN
                agent_name_full = agent_data.get('server_name')
                if not agent_name_full:
                    continue

                # Chercher le nom de serveur court correspondant
                found_server_name = None
                for server_name in server_names_set:
                    if server_name in agent_name_full:
                        found_server_name = server_name
                        break
                
                if found_server_name:
                    # Si une correspondance est trouvée, stocker les données dans la structure unifiée
                    # en utilisant le nom court comme clé
                    
                    if collector.collector_type not in unified_agent_data[found_server_name]:
                        unified_agent_data[found_server_name][collector.collector_type] = {}
                    
                    # Fusionner les données de l'agent si plusieurs sources existent
                    unified_agent_data[found_server_name][collector.collector_type].update(agent_data)
                    
        # 3. Traiter chaque serveur en utilisant la structure de données unifiée
        logger.info("Démarrage de la phase de traitement et de mise à jour des agents.")
        
        for server in self.all_servers:            
            # Accès direct aux données consolidées du serveur. C'est O(1) !
            server_data = unified_agent_data.get(server.server_name, {})
            ip = ""

            # Utiliser un dictionnaire pour suivre l'état des agents de manière propre
            found_agents = {
                "checkmk": False,
                "glpi": False,
                "rapid7": False,
                # Ajoutez d'autres agents ici
            }

            # Traitement pour CheckMK
            checkmk_data = server_data.get("checkmk")
            required = self.get_server_agent_info(server.server_name, 'checkmk').is_required
            if checkmk_data and required:
                found_agents["checkmk"] = True
                if not ip and checkmk_data.get('ip_address'):
                    ip = checkmk_data.get('ip_address')

            # Traitement pour GLPI
            glpi_data = server_data.get("glpi")
            required = self.get_server_agent_info(server.server_name, 'glpi').is_required
            if glpi_data:
                found_agents["glpi"] = True
                if not ip and glpi_data.get('ip_address'):
                    ip = glpi_data.get('ip_address')

            # Traitement pour Rapid7
            rapid7_data = server_data.get("rapid7")
            required = self.get_server_agent_info(server.server_name, 'rapid7').is_required
            if rapid7_data and rapid7_data.get('is_installed'):
                found_agents["rapid7"] = True
                self.update_risk_score(server.server_name, rapid7_data.get('riskScore'))
                if not ip and rapid7_data.get('ip_address'):
                    ip = rapid7_data.get('ip_address')

            # Mettre à jour le réseau si une IP a été trouvée
            if ip:
                self.upsert_networks(server_name=server.server_name, ip_address=ip, netw_name='Unknown')

            # Mettre à jour l'état de chaque agent de manière centralisée
            for agent_name, status in found_agents.items():
                self.update_agent_info(server_name=server.server_name, agent_name=agent_name, status=status)
                
        self.export_to_json(unified_agent_data, "all_agents")
        logger.info("Phase de traitement terminée. Les agents ont été mis à jour.")