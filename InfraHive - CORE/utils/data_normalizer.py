import yaml
import logging
from utils.normalization_strategies import NormalizationStrategy, VCenterNormalizationStrategy, AWSNormalizationStrategy, AzureNormalizationStrategy, CSVVCenterNormalizationStrategy, CheckMKNormalizationStrategy, GLPINormalizationStrategy, Rapid7NormalizationStrategy

logger = logging.getLogger(__name__)

class DataNormalizer:
    """
    Manages the normalization of raw data from various sources into a standardized format.
    
    This class implements the Strategy and Adapter design patterns to handle different
    data formats (e.g., AWS, Azure, CSV, CheckMK) and apply a common normalization process.
    It uses a YAML file for flexible field mapping and ensures data is consistently
    formatted before being used by other parts of the application.
    """
    def __init__(self, mapping_file="config/normalization_maps.yaml"):
        """
        Initializes the DataNormalizer, loading field mappings from a YAML file
        and setting up normalization strategies for different data types.

        Args:
            mapping_file (str): Path to the YAML file containing the field mappings.
        """
        try:
            # Attempt to open and load the YAML mapping file

            with open(mapping_file, 'r') as f:
                self.mappings = yaml.safe_load(f)
        except FileNotFoundError:
            # Log an error if the file is not found and set mappings to an empty dict
            logger.error(f"Fichier de mappage de normalisation non trouvé: {mapping_file}")
            self.mappings = {}
        except yaml.YAMLError as e:
            # Log an error if there's an issue parsing the YAML file
            logger.error(f"Erreur lors du chargement du fichier YAML de mappage: {e}")
            self.mappings = {}
        
        
        # Dictionary to store pre-instantiated normalization strategies
        self.strategies = {
            "aws": AWSNormalizationStrategy(),
            "azure": AzureNormalizationStrategy(),
            "csv": CSVVCenterNormalizationStrategy(),
            "checkmk": CheckMKNormalizationStrategy(),
            "glpi": GLPINormalizationStrategy(),
            'rapid7': Rapid7NormalizationStrategy()
        }

    def normalize_data(self, data_type: str, raw_data: dict, config) -> dict:
        """
        Normalizes a single piece of raw data based on its source type and a
        pre-defined mapping.

        The process involves two steps:
        1. Applying a specific normalization strategy (e.g., AWS, Azure) to
           standardize the data format.
        2. Applying a YAML-based mapping to rename fields and extract nested data
           into a final, target structure.

        Args:
            data_type (str): The type of data source (e.g., 'aws', 'azure', 'ngdt').
            raw_data (dict): The raw, unnormalized data from the source.
            config (dict): A dictionary of configuration settings needed by some strategies.

        Returns:
            dict: The fully normalized data in the final target format.
        """
        
        logger.debug(f"Début de la normalisation pour le type '{data_type}'.")
        
        # Dynamically selects the normalization strategy based on the data_type.
        # VCenter strategies ('ngdt', 'oxya') are instantiated here because they
        # require a source_type parameter at initialization.
        
        if data_type == 'ngdt' or data_type == 'oxya':
            strategy = VCenterNormalizationStrategy(source_type=data_type, config=config)
        else:
            strategy = self.strategies.get(data_type)
        
        
        # If no strategy is found, log a warning and return the raw data unchanged.
        if not strategy:
            logger.warning(f"Aucune stratégie de normalisation trouvée pour le type: {data_type}. Retourne les données brutes.")
            return raw_data
        
        # Step 1: Apply the basic normalization strategy
        normalized_data = strategy.normalize(raw_data)
        final_normalized_data = {}
        # Step 2: Apply the YAML-based field mapping
        mapping_key = f"{data_type}_server_map"
        mapping = self.mappings.get(mapping_key)
        if mapping:
            
            
            # Iterate through the mapping rules (target field: source path)
            for target_field, source_path in mapping.items():
                value = normalized_data 
                try:
                    for part in source_path.split('.'):
                        if isinstance(value, dict):
                            value = value.get(part)
                        else:
                            
                            # Stop traversing if an intermediate part is not a dictionary
                            value = None
                            break
                except AttributeError:
                    
                    # Handle cases where the path doesn't exist
                    value = None
                final_normalized_data[target_field] = value
            
            logger.debug(f"Normalisation terminée pour le type '{data_type}'.")
            return final_normalized_data
        
        else:
            logger.debug(f"Aucun mappage configuré trouvé pour le type: {data_type}. Utilise uniquement la sortie de la stratégie.")
            return normalized_data
        