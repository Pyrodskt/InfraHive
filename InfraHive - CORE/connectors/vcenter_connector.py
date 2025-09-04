import requests, json, re
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Vcenter:
    def __init__(self, config: dict, logger):
        """
        Initializes the Vcenter collector with a configuration dictionary and a logger.
        
        Args:
            config (dict): A dictionary containing 'url', 'username', 'password', and 'type'.
            logger (Logger): The application logger instance.
        """
        # Récupération des informations depuis l'objet de configuration
        self.logger = logger
        self.vcenter_url = config.get('url')
        self.vcenter_username = config.get('username')
        self.vcenter_password = config.get('password')
        self.source_type = config.get('type')

    def get_vcenter_api_session(self, vcenter, user, password):
        url = f'https://{vcenter}/rest/com/vmware/cis/session'
        response = requests.post(url, auth=HTTPBasicAuth(user, password), verify=False)
        if response.status_code == 200:
            return response.json()['value']
        else:
            self.logger.error(f"Erreur de création de session API: {response.status_code}, {response.text}")
            return None

    def get_all_vms(self, vcenter, session_id):
        url = f'https://{vcenter}/rest/vcenter/vm/'
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            self.logger.error(f"Erreur lors de la récupération des VMs: {response.status_code}, {response.text}")
            return []

    def get_all_tags(self, vcenter, session_id):
        url = f'https://{vcenter}/api/vcenter/tagging/associations'
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Erreur lors de la récupération de la liste des associations de balises : {response.status_code}, {response.text}")
            
    def get_vm_info(self, vm_id, vcenter, session_id, vm_name):
        url = f'https://{vcenter}/rest/vcenter/vm/{vm_id}'
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            val = {
                "power_state": response.json()['value']['power_state'],
                "guest_OS": response.json()['value']['guest_OS'],
                "network": [net['value']['backing']['network'] for net in response.json()['value'].get('nics')] 
            }
            return val
        else:
            self.logger.error(f"Erreur lors de la récupération des infos de la vm {vm_name}: {response.status_code}, {response.text}")
            return []

    def get_tags_value(self, all_tags, vm_id, vcenter, session_id, vm_name):
        # ... (le code de cette méthode ne change pas) ...
        tags_ids = [tag['tag'] for tag in all_tags["associations"] if tag['object']['id'] == vm_id]
        tags = []
        for tag in tags_ids:
            tag_info = self.get_tag_info(tag, vcenter, session_id)
            if tag_info:
                tags.append(tag_info)
            else:
                self.logger.error(f"Erreur lors de la récupération des balises pour la VM {vm_name}: ID non trouvé")
        return tags

    def get_tag_info(self, tag_id, vcenter, session_id):
        # ... (le code de cette méthode ne change pas) ...
        url = f'https://{vcenter}/rest/com/vmware/cis/tagging/tag/id:{tag_id}'
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            tag_info = response.json().get('value', {})
            tag_name = tag_info.get('name', 'Unknown')
            category_id = tag_info.get('category_id', 'Unknown')
            category_name = self.get_category_info(category_id, vcenter, session_id)
            return {'tag_name': category_name, 'tag_value': tag_name}
        else:
            self.logger.error(f"Erreur lors de la récupération des informations de la balise {tag_id}: {response.status_code}, {response.text}")
            return None

    def get_category_info(self, category_id, vcenter, session_id):
        # ... (le code de cette méthode ne change pas) ...
        url = f'https://{vcenter}/rest/com/vmware/cis/tagging/category/id:{category_id}'
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            category_info = response.json().get('value', {})
            return category_info.get('name', 'Unknown')
        else:
            self.logger.error(f"Erreur lors de la récupération des informations de la catégorie {category_id}: {response.status_code}, {response.text}")
            return 'Unknown'
    
    def export_to_json(self, vm_list, file_path):
        # ... (le code de cette méthode ne change pas) ...
        try:
            with open(file_path, 'w') as f:
                json.dump(vm_list, f, indent=4)
            self.logger.debug(f"Données exportées avec succès vers {file_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exportation des données JSON: {str(e)}")
            
    # CORRECTION ICI : La méthode a été renommée en 'collect'
    def collect(self):
        """
        Récupère toutes les VMs, leurs informations et leurs tags.
        Retourne une liste de VMs traitées.
        """
        try:
            self.logger.debug(f"Connexion au vCenter : {self.vcenter_url}")
            session_id = self.get_vcenter_api_session(self.vcenter_url, self.vcenter_username, self.vcenter_password)
            
            if not session_id:
                self.logger.error("Échec de la connexion à l'API vCenter.")
                return []
            
            self.logger.debug("Récupération de la liste de toutes les VMs...")
            vms_list_raw = self.get_all_vms(self.vcenter_url, session_id)
            if not vms_list_raw:
                self.logger.warning("Aucune VM trouvée.")
                return []
            
            reg_ignore1 = re.compile(r'([a-zA-Z]{3})([a-zA-Z]{3})([a-zA-Z]{4})([a-zA-Z]{3})([0-9]{2})_.*')
            reg_ignore2 = re.compile(r'([A-Z]{1}[0-9]{2})([A-Z]{3})([A-Z]{4})([A-Z]{3})([0-9]{2})_.*')
            vm_to_process = []
            for vm in vms_list_raw:
                 if not reg_ignore1.match(vm['name']) and not reg_ignore2.match(vm['name']):
                    vm_to_process.append(vm)
            self.logger.debug("Récupération de tous les tags...")
            all_tags = self.get_all_tags(self.vcenter_url, session_id)

            processed_vms = self.process_vms_multithreaded(vm_to_process, all_tags, session_id)
            
            self.logger.debug(f"Collecte et traitement terminés pour {self.vcenter_url}")
            return processed_vms

        except Exception as e:
            self.logger.error(f"Erreur générale lors de l'exécution du VcenterConnector : {e}", exc_info=True)
            return []
        
    def process_vm_data(self, vm, all_tags, session_id):
        # ... (le code de cette méthode ne change pas) ...
        vm_id = vm['vm']
        vm_name = vm['name']

        vm_info = self.get_vm_info(vm_id, self.vcenter_url, session_id, vm_name)
        vm_tags = self.get_tags_value(all_tags, vm_id, self.vcenter_url, session_id, vm_name)
        
        try:
            nets = vm_info['network']
        except Exception:
            vm_info['network'] = []

        return {
            'name': vm_name,
            'tags': vm_tags,
            'infos': vm_info
        }

    def process_vms_multithreaded(self, vms_list_raw, all_tags, session_id):
        # ... (le code de cette méthode ne change pas) ...
        self.logger.debug(f"Démarrage du traitement multi-thread de {len(vms_list_raw)} VMs...")
        processed_vms = []

        with ThreadPoolExecutor(max_workers=24) as executor:
            futures = {
                executor.submit(self.process_vm_data, vm, all_tags, session_id): vm 
                for vm in vms_list_raw
            }
            
            for future in as_completed(futures):
                try:
                    vm_info = future.result()
                    if vm_info:
                        processed_vms.append(vm_info)
                        self.logger.debug(f"Traitement de la VM {vm_info.get('name', 'inconnue')} effectué.")
                except Exception as e:
                    self.logger.error(f"Erreur lors du traitement d'une VM : {e}", exc_info=True)
                        
        return processed_vms