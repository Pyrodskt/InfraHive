# utils/logger_setup.py
import logging
import logging.config
import os, datetime
from config.settings import Settings

class Logger:
    def __init__(self, filename):
        """
        Initializes the Logger class, setting up logging configuration.

        Args:
            filename (str): The base name for the log file.
        """
        self.filename = filename
        self.config = Settings()
        self.current_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.setup_logging()

        
    def setup_logging(self):
        """
        Configure le logger de l'application en utilisant le fichier config.yaml.
        """

        if not self.config.LOGGING:
            # Configuration par défaut si la section 'logging' n'est pas présente
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            logging.info("Configuration de logging par défaut utilisée.")
            return

        # S'assurer que le répertoire des logs existe
        log_dir = self.config.LOGGING_DIRECTORY
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configuration détaillée du logger
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': self.config.LOGGING_LEVEL,
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                },
                'file': {
                    'level': self.config.LOGGING_LEVEL,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'filename': os.path.join(log_dir, f"{self.current_date}_{self.filename}.log"),
                    'maxBytes': 1024 * 1024 * 5,  # 5 MB
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
            },
            'loggers': {
                '': {  # Logger racine
                    'handlers': ['console', 'file'],
                    'level': self.config.LOGGING_LEVEL,
                    'propagate': True,
                },
            }
        })
        
        logging.info("Configuration de logging chargée avec succès.")

    def get_logger(self, name):
        """
        Fonction utilitaire pour obtenir un logger avec un nom spécifique.
        """
        return logging.getLogger(name)