# workers/server_worker.py
import threading
import logging
from sqlalchemy.orm import Session
from db.db_connector import SessionLocal, DBQueries  # Importe la fabrique de sessions

logger = logging.getLogger(__name__)
class DBWorker(threading.Thread):
    """
    Worker thread responsable d'insérer des données normalisées dans la base de données.
    """
    def __init__(self, source_type: str, data_to_process: list, action_method_name: str):
        """
        Initialise le DBWorker.

        Args:
            source_type (str): Le type de la source (e.g., "aws", "azure").
            servers_data (list): La liste des serveurs à insérer.
        """
        super().__init__()
        self.source_type = source_type
        self.data_to_process = data_to_process
        self.action_method_name = action_method_name
        self.success = False

    def run(self):
        """
        Exécute la logique d'insertion dans la base de données.
        """
        logger.info(f"Démarrage de l'insertion pour la source : {self.source_type}")

        with SessionLocal() as session:
            try:
                db_queries = DBQueries(session)
                
                # Obtient la méthode à appeler dynamiquement
                # Par exemple, si self.action_method_name est "insert_server_in_db",
                # `action_method` devient une référence à db_queries.insert_server_in_db
                action_method = getattr(db_queries, self.action_method_name)
                
                for data_item in self.data_to_process:
                    # Exécute la méthode avec l'objet de données
                    action_method(data_item)

                session.commit() # Effectue le commit une seule fois pour tout le lot
                logger.info(f"Insertion réussie pour {len(self.data_to_process)} éléments de la source {self.source_type} avec la méthode {self.action_method_name}.")
                self.success = True
            except Exception as e:
                logger.error(f"Erreur lors de l'insertion pour la source {self.source_type} : {e}", exc_info=True)
                session.rollback()
            finally:
                session.close()