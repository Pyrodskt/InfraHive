import re
import csv
import logging
from config.settings import settings
logger = logging.getLogger(__name__)
config = settings
class VCenterAnalyzer:
    """
    Analyse les données brutes d'une VM vCenter pour en extraire des informations
    spécifiques basées sur la logique métier (e.g., tags, nom de la VM).
    """
    def __init__(self):
        # Vous pouvez charger des configurations ou des exceptions ici si nécessaire
        pass

    def import_exceptions(self, file_path):
        """Fonction utilitaire pour importer des exceptions."""
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                return list(reader)
        except FileNotFoundError:
            logger.warning(f"Fichier d'exceptions non trouvé: {file_path}")
            return []

    def get_vm_infos_ngdt(self, vm):
        vc_div = "UKN"
        env = "UKN"
        role = "UKN"
        app = "UKN"

        if 'tags' in vm:
            for i in vm['tags']:
                if i['tag_name'] == "VC-DIVISIONS":
                    vc_div = i['tag_value']
                if i['tag_name'] == "SLA" and i['tag_value'] == "PROD":
                    env = "PRD"

        reg = re.compile(r'([a-zA-Z]{3})([a-zA-Z]{3})([a-zA-Z]{4})([a-zA-Z]{3})')
        if reg.match(vm['name']):
            if vc_div == "UKN":
                vc_div = reg.match(vm['name']).group(1).upper()
            if env == "UKN":
                env = reg.match(vm['name']).group(2).upper()
            app = reg.match(vm['name']).group(3).upper()
            role = reg.match(vm['name']).group(4).upper()
        networks = [self.get_networks_ngdt(net) for net in vm['infos']['network']]
        return vc_div, env, app, role, networks
    
    
    def get_vm_infos_csv(self, vm):
        vc_div = "UKN"
        env = "UKN"
        role = "UKN"
        app = "UKN"
        reg = re.compile(r'([a-zA-Z]{3})([a-zA-Z]{3})([a-zA-Z]{4})([a-zA-Z]{3})')
        reg2 = re.compile(r'([A-Z]{1}[0-9]{2})([A-Z]{3})([A-Z]{4})([A-Z]{3})([0-9]{2})')
        if reg.match(vm['name']):
            vc_div = reg.match(vm['name']).group(1).upper()
            env = reg.match(vm['name']).group(2).upper()
            app = reg.match(vm['name']).group(3).upper()
            role = reg.match(vm['name']).group(4).upper()
        elif reg2.match(vm['name']):
            env = reg2.match(vm['name']).group(2).upper()
            app = reg2.match(vm['name']).group(3).upper()
            role = reg2.match(vm['name']).group(4).upper()
        
        return vc_div, env, app, role
    
    def get_networks_ngdt(self, portgroup_id):
        
        for net in config.NGDT_PORTGROUPS:
            if net[1] == portgroup_id:
                return net[0]
        else:
            return None
        
    def get_networks_oxya(self, portgroup_id):
        
        for net in config.OXYA_PORTGROUPS:
            if net[1] == portgroup_id:
                return net[0]
        else:
            return None
        
    def get_vm_infos_oxya(self, oxy_server):
        env = 'UKN'
        tier = 'T1'
        
        # NOTE: Assurez-vous que le chemin vers votre fichier d'exceptions est correct
        excep = self.import_exceptions('config//exceptions_oxya.csv')
        match = re.search(r"(.*)-[a-zA-Z-0-9]{4}$", oxy_server.get("name"))
        # print(vm_detail.get('name'), [net['value']['backing']['network'] for net in vm_detail.get('nics')])
        name = ""
        if match:
            name = match.group(1)
                
        else:
            name = oxy_server.get("name")

        if 'infos' in oxy_server and 'network' in oxy_server['infos']:
            networks = [self.get_networks_oxya(net) for net in oxy_server['infos']['network']]
            for net in networks:
                if not net:
                    continue
                if "TIERS0" in net or "T0" in net:
                    tier = 'T0'
                if "TIERS1" in net or "T1" in net:
                    tier = 'T1'
                if "vNet_IaaS_" in net and 'NPRD' not in net:
                    env = net[10:13]
                if "vNet_IaaS_" in net and 'NPRD' in net:
                    env = "UKN"
        else:
            env = 'UKN'
            tier = 'T1'
        
        if 'name' in oxy_server:
            for vm in excep:
                if oxy_server['name'].upper() == vm[0]:
                    tier = vm[1]
        

        return env, tier, networks, name
    