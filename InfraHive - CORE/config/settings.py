import os
from dotenv import load_dotenv
import yaml, csv

class Settings:
    """
    Classe pour gérer la configuration de l'application.
    Charge automatiquement les variables depuis le fichier .env
    ou depuis l'environnement système.
    """
    def __init__(self):
        """
        Initializes the Settings class, loading environment variables and configuration
        from 'config.yaml'.
        """
        # Charger le fichier .env s'il existe
        load_dotenv()
        config = self.load_configs()
        
        # --- Logging ---
        self.LOGGING = True
        self.LOGGING_DIRECTORY = 'logs'
        self.LOGGING_LEVEL = "INFO"
        
        # --- Base de données ---
        self.DRIVER = os.getenv('SQL_DRIVER')
        
        
        self.OEIL_SERVER = os.getenv("OEIL_SERVER")
        self.OEIL_DB = os.getenv("OEIL_DB")
        self.OEIL_DB_USER = os.getenv("OEIL_DB_USER")
        self.OEIL_DB_USER_PWD = os.getenv("OEIL_DB_USER_PWD")

        self.HOSTING_SERVER = os.getenv("HOSTING_SERVER")
        self.HOSTING_DB = os.getenv("HOSTING_DB")
        self.HOSTING_DB_USER = os.getenv("HOSTING_DB_USER")
        self.HOSTING_DB_USER_PWD = os.getenv("HOSTING_DB_USER_PWD")
        
        self.CORTEX_URL = os.getenv('CORTEX_URL')
        self.CORTEX_KEY_ID = os.getenv('CORTEX_KEY_ID')
        self.CORTEX_API_KEY = os.getenv("CORTEX_KEY")
        
        self.AZURE_CONFIGS = config.get('AZURE_CONFIGS')
        
        self.CSV_CONFIGS = config.get('CSV_CONFIGS')

        # --- VCenter Configurations ---
        self.VCENTER_CONFIGS = []
        for vc_config_from_yaml in config.get('VCENTER_CONFIGS', []):
            vc_config = vc_config_from_yaml.copy()
            password_env_var_name = vc_config.get('password')
            if password_env_var_name:
                vc_config['password'] = os.getenv(password_env_var_name)
            
            self.VCENTER_CONFIGS.append(vc_config)
        
        self.THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", 10))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # --- Check_MK Configurations ---
        
        #self.CHECK_MK_CONFIGS = config['CHECK_MK']
        self.CHECK_MK_CONFIGS = []
        for chmk_config_from_yaml in config.get('CHECK_MK_CONFIGS', []):
            chmk_config = chmk_config_from_yaml.copy()
            username_env_var_name = chmk_config.get('username')
            password_env_var_name = chmk_config.get('password')
            if password_env_var_name and username_env_var_name:
                chmk_config['username'] = os.getenv(username_env_var_name)
                chmk_config['password'] = os.getenv(password_env_var_name)
                
            self.CHECK_MK_CONFIGS.append(chmk_config)
        
        # --- GLPI Configurations ---
        self.GLPI_CONFIGS = []
        for glpi_config_from_yaml in config.get('GLPI_CONFIGS', []):
            glpi_config = glpi_config_from_yaml.copy()
            app_token_env_var_name = glpi_config.get('GLPI_APP_TOKEN')
            user_token_env_var_name = glpi_config.get('GLPI_USER_TOKEN')
            if app_token_env_var_name and user_token_env_var_name:
                glpi_config['APP_TOKEN'] = os.getenv(app_token_env_var_name)
                glpi_config['USER_TOKEN'] = os.getenv(user_token_env_var_name)
                
            self.GLPI_CONFIGS.append(glpi_config)
            
        # --- Rapid7 Configurations ---
        self.RAPID7_CONFIGS = []
        for rapid7_config_from_yaml in config.get('RAPID7_CONFIGS', []):
            rapid7_config = rapid7_config_from_yaml.copy()
            url_env_var_name = rapid7_config.get('url')
            rapid7_key_env_var_name = rapid7_config.get('RAPID7_KEY')
            if url_env_var_name and rapid7_key_env_var_name:
                rapid7_config['url'] = os.getenv(url_env_var_name)
                rapid7_config['rapid7_key'] = os.getenv(rapid7_key_env_var_name)
                
            self.RAPID7_CONFIGS.append(rapid7_config)
        
        
        # --- Autres ---
        self.THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", 10))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.NGDT_PORTGROUPS = self.read_csv('config//ngdt_portgroups.csv')
        self.OXYA_PORTGROUPS = self.read_csv('config//oxya_portgroups.csv')

    def read_csv(self, filename):
      with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        content = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                content.append(row)
        return content
    
    def load_configs(self):
        """
        Loads configuration data from the 'config.yaml' file.

        Returns:
            dict: The loaded configuration data.
        """
        with open("config//config.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        return data
    
    def __repr__(self):
        return f"<Settings LOG_LEVEL={self.LOG_LEVEL} THREAD_POOL_SIZE={self.THREAD_POOL_SIZE}>"


settings = Settings()

VCENTER_CONFIGS = settings.VCENTER_CONFIGS
THREAD_POOL_SIZE = settings.THREAD_POOL_SIZE