# Fichier e:\KPI_HOSTING - V2.1\utils\normalization_strategies.py

from abc import ABC, abstractmethod
from analyzers.vcenter_analyser import VCenterAnalyzer # Importation du nouvel analyseur
import logging, re

logger = logging.getLogger(__name__)

class NormalizationStrategy(ABC):
    @abstractmethod
    def normalize(self, data: dict) -> dict:
        pass

class VCenterNormalizationStrategy(NormalizationStrategy):
    def __init__(self, source_type: str, config):
        # Initialise l'analyseur en fonction du type de source
        self.analyzer = VCenterAnalyzer()
        self.source_type = source_type
    
    def normalize(self, data: dict) -> dict:
        """
        Normalise les données brutes de vCenter et les enrichit avec l'analyseur.
        """
        # 1. Normalisation de base (comme avant)
        normalized_data = {
            "name": data.get("name"),
            "source": self.source_type,
            "tags": {},
            "infos": data.get("infos", {})
        }
        tags_list = data.get("tags", [])
        for tag in tags_list:
            tag_name = tag.get("tag_name")
            tag_value = tag.get("tag_value")
            if tag_name:
                normalized_data["tags"][tag_name] = tag_value
        
        # 2. Ajout de la logique d'analyse
        if self.source_type == 'ngdt':
            vc_div, env, app, role, networks = self.analyzer.get_vm_infos_ngdt(data)
            normalized_data['division'] = vc_div
            normalized_data['env'] = env
            normalized_data['app'] = app
            normalized_data['role'] = role
            normalized_data['tier'] = "T1"
            normalized_data['networks'] = networks
        
        elif self.source_type == 'oxya':
            env, tier, networks, name = self.analyzer.get_vm_infos_oxya(data)
            normalized_data['name'] = name
            normalized_data['env'] = env
            normalized_data['tier'] = tier
            normalized_data['networks'] = networks
            normalized_data['app'] = "UKN"
            normalized_data['role'] = "UKN"
            normalized_data['division'] = "UKN"

            
        return normalized_data
    
class CSVVCenterNormalizationStrategy(NormalizationStrategy):
    def __init__(self):
        pass
        # Initialise l'analyseur en fonction du type de source
        self.analyzer = VCenterAnalyzer()
    
    def normalize(self, data: dict) -> dict:
        """
        Normalise les données brutes de vCenter et les enrichit avec l'analyseur.
        """
        # 1. Normalisation de base (comme avant)
        normalized_data = {
            "name": data.get("name"),
            "tags": {},
            "infos": data.get("infos", {}),
            "source" : "ngdt"
        }
            
        vc_div, env, app, role, = self.analyzer.get_vm_infos_csv(data)
        normalized_data['division'] = vc_div
        normalized_data['env'] = env
        normalized_data['app'] = app
        normalized_data['role'] = role
        normalized_data['tier'] = 'T0'
        normalized_data['ip_address'] = data.get('ip_address', "")
        normalized_data['networks'] = data.get('networks', [])
            
        return normalized_data

class AWSNormalizationStrategy(NormalizationStrategy):
    def normalize(self, data: dict) -> dict:
        # ... (le code de cette classe ne change pas) ...
        logger.info("Normalisation des données AWS...")
        return {"server_name": data.get("tags", {}).get("Name"), "instance_id": data.get("instance_id")}

class AzureNormalizationStrategy(NormalizationStrategy):
    def normalize(self, data: dict) -> dict:
        # ... (le code de cette classe ne change pas) ...
        # logger.info("Normalisation des données Azure...")
        return data
        # return {"server_name": data.get("name"), "resource_group": data.get("resourceGroup")}

class CheckMKNormalizationStrategy(NormalizationStrategy):
     def normalize(self, data: dict) -> dict:
        return data
    
class GLPINormalizationStrategy(NormalizationStrategy):
     def normalize(self, data: dict) -> dict:
        return data

class Rapid7NormalizationStrategy(NormalizationStrategy):
     def normalize(self, data: dict) -> dict:
        return data