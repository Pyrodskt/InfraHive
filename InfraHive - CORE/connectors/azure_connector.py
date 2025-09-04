import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

class AzureConnector:
    def __init__(self, config, logger) -> None:
        """
        Initializes the AzureToken class, loading Azure credentials from environment variables
        and immediately fetching an access token.
        """
        load_dotenv()
        self.logger = logger
        self.tenantId = os.getenv(config.get("env_tenant_id"))
        self.clientId = os.getenv(config.get("env_client_id"))
        self.clientSecret = os.getenv(config.get("env_client_secret"))
        
        self.token = ''
        
    def _get_token(self) -> str:
        """
        Fetches an Azure access token using client credentials flow.

        Returns:
            str: The access token.

        Raises:
            requests.exceptions.HTTPError: If the token request fails.
        """
        url = f"https://login.microsoftonline.com/{self.tenantId}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "scope": "https://management.azure.com/.default"
        }
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
    
    def get_token(self):
        """
        Returns the stored Azure access token.

        Returns:
            str: The Azure access token.
        """
        return self.token
    
    def get_subs(self):
        url = "https://management.azure.com/subscriptions?api-version=2022-12-01"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])
    
    def get_rgs(self, sub_id):
        url = f"https://management.azure.com/subscriptions/{sub_id}/resourcegroups?api-version=2021-04-01"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])
    
    def get_vms(self, subscription_id, rg_name):
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Compute/virtualMachines?api-version=2023-03-01"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])

    def get_vm_instance(self, vm_id):
        url = f"https://management.azure.com{vm_id}/instanceView?api-version=2024-11-01"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_network_info(self, sub_id, rg_name, vm_data):
        try:
            nic_id = vm_data["properties"]["networkProfile"]["networkInterfaces"][0]["id"]
            nic_name = nic_id.split("/")[-1]
            url = f"https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg_name}/providers/Microsoft.Network/networkInterfaces/{nic_name}?api-version=2024-05-01"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            nic_data = response.json()

            for ip_config in nic_data["properties"]["ipConfigurations"]:
                if ip_config["properties"].get("primary"):
                    return {
                        "ip_address": ip_config["properties"].get("privateIPAddress"),
                        "subnet_name": ip_config["properties"]["subnet"]["id"].split("/")[-1],
                        "vnet_name": ip_config["properties"]["subnet"]["id"].split("/")[8]
                    }
        except Exception as e:
            self.logger.error(f"Erreur réseau pour {vm_data['name']}: {e}")
        return {"ip_address": None, "subnet_name": None, "vnet_name": None}

    def get_subnets_from_rg(self, rg):
        subnets = []
        self.logger.debug(f'RG Traitée {rg['sub_name']} - {rg['rg_name']}')
        sub_id = rg['sub_id']
        sub_div = rg['sub_div']
        rg_name = rg['rg_name']
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            vnet_url = f"https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg_name}/providers/Microsoft.Network/virtualNetworks?api-version=2023-05-01"
            vnet_response = requests.get(vnet_url, headers=headers)
            vnet_response.raise_for_status()
            vnets = vnet_response.json().get("value", [])
        except Exception as e:
            self.logger.error(f"Pas de vnet pour {rg['sub_name']} - {rg_name}")
            return
        
        for vnet in vnets:
            vnet_name = vnet['id'].split('/')[-1]

            #subnet_url = f"https://management.azure.com/{sub_id}/resourceGroups/{rg_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name}/subnets?api-version=2023-05-01"
            try:
                subnet_url = f"https://management.azure.com{vnet['id']}/subnets?api-version=2023-05-01"
                subnet_response = requests.get(subnet_url, headers=headers)
                subnet_response.raise_for_status()

                for subnet in subnet_response.json().get("value", []):
                    subnet_data = {
                        "subnet_name": subnet["name"],
                        "is_dmz": False,
                        "id_div": sub_div,
                        "vnet_name": vnet_name
                    }
                    subnets.append(subnet_data)
            except Exception as e:
                self.logger.error(f'Erreur lors de la récupération des subnets pour {sub_id} - {rg_name} - {vnet}')

        return subnets

    def get_vm_from_rg(self, rg):
        local_vms = []

        try:
            sub_id, rg_name = rg['sub_id'], rg['rg_name']

            vm_metadata = {
                "sub_name":rg['sub_name'],
                "division": rg['sub_div'],
                "env": rg['sub_env'],
                "tier": rg['sub_tier'],
            }

            self.logger.debug(f"Collecte des VMs pour RG: {rg_name}")
            vms = self.get_vms(sub_id, rg_name)

            for vm in vms:
                try:
                    self.logger.debug(f'Traitement de la VM {vm['name']} : {rg['sub_name']} - {rg_name} ')
                    instance_view = self.get_vm_instance(vm["id"])
                    power_state = next(
                        (status["displayStatus"] for status in instance_view.get("statuses", [])
                        if status["code"].startswith("PowerState/")), 
                        "POWER_OFF"
                    )
                    os_info = (
                        f"{instance_view.get('osName', '')} - {instance_view.get('osVersion', '')}".strip(" -")
                        if "osName" in instance_view else
                        vm.get("properties", {}).get("osDisk", {}).get("osType", "Unknown")
                    )
                    network = self.get_network_info(sub_id, rg_name, vm)

                    vm_data = {
                        "name": vm["name"],
                        "infos": {
                            "power_state": "POWER_ON" if power_state == "VM running" else "POWER_OFF",
                            "guest_OS": os_info,
                            "network": [network["subnet_name"]]
                        },
                        "power_state": "POWER_ON" if power_state == "VM running" else "POWER_OFF",
                        "guest_OS": os_info,
                        "env": vm_metadata["env"],
                        "tier": vm_metadata["tier"],
                        "app": "UKN",
                        "division": vm_metadata["division"],
                        "role": "UKN",
                        "source": "AZURE",
                        "networks": [network["subnet_name"]],
                        "souscription_name": vm_metadata["sub_name"],
                        "rg_name": rg_name,
                        "ip_address": network["ip_address"],
                        "vnet": network["vnet_name"]
                    }
                    local_vms.append(vm_data)
                except Exception as vm_err:
                    self.logger.error(f"Erreur sur VM {vm['name']} dans {rg_name}: {vm_err}")
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement du RG {rg_name}: {e}")
        return local_vms

    def process_sub(self, sub):
        sub_id = sub['subscriptionId']
        sub_name = sub['displayName']
        sub_div = "UKN"
        sub_env = "UKN"
        sub_tier= "Unknown"
        cloud_provider="AZURE"
        rgs = self.get_rgs(sub_id)
        tmp =[]
        for rg in rgs:
            rg_name = rg['name']
            data = {
                "sub_name": sub_name,
                "sub_id": sub_id,
                "sub_div": sub_div,
                "sub_env": sub_env,
                "sub_tier": sub_tier,
                "cloud_provider": cloud_provider,
                "rg_name": rg_name
            }
            tmp.append(data)

        return tmp
    
    def collect_subnets(self, all_rgs):
        global all_subnets
        all_subnets = []
        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = [executor.submit(self.get_subnets_from_rg, rg) for rg in all_rgs]
            for future in as_completed(futures):
                try:
                    all_subnets.extend(future.result())
                except Exception as e:
                    self.logger.error(f"Erreur dans un thread: {e}")

        # print(f"\nTotal subnets trouvés : {len(all_subnets)}")
        # with open('Import_VMS/exports/azure_subnets.json', 'w') as f:
        #     json.dump(all_subnets, f, indent=4)
        # print("EXPORTED")
        return all_subnets
    
    def collect_subs(self):
        try:
            subscriptions = self.get_subs()
            for sub in subscriptions:
                if sub['state'] == "Disabled":
                    subscriptions.remove(sub)
            
            all_rgs = []
            with ThreadPoolExecutor(max_workers=32) as executor:
                futures = [executor.submit(self.process_sub, rg) for rg in subscriptions]
                for future in as_completed(futures):
                    try:
                        all_rgs.extend(future.result())
                    except Exception as e:
                        self.logger.error(f"Erreur dans un thread: {e}")

            self.logger.debug(f"Total Subs trouvées actives : {len(subscriptions)}")
            self.logger.debug(f"Total RGs trouvés actifs : {len(all_rgs)}")
            return subscriptions, all_rgs
        
        except Exception as e:
            self.logger.error(f"Erreur fatale dans le script principal: {e}")
            
    def collect_vms(self, all_rgs):
        all_vms = []
        try:
            with ThreadPoolExecutor(max_workers=32) as executor:
                futures = [executor.submit(self.get_vm_from_rg, rg) for rg in all_rgs]
                for future in as_completed(futures):
                    try:
                        all_vms.extend(future.result())
                    except Exception as e:
                        self.logger.error(f"Erreur dans un thread: {e}")
            return all_vms
        except Exception as e:
            self.logger.error(f"Erreur fatale dans le script principal: {e}")
       
    def collect(self):
        all_vms = []
        
        try:
            self.token = self._get_token()
        except Exception as e:
            self.logger.error(f'Connexion échouée {e}')
            
        try:
            self.logger.debug('=== Démarrage de la corrélation Azure ===')
            subscriptions, all_rgs = self.collect_subs()
            all_subnets = self.collect_subnets(all_rgs=all_rgs)
            all_vms = self.collect_vms(all_rgs=all_rgs)
            self.logger.debug('=== Corrélation Azure terminée ===')
            return {"servers": all_vms, "ressource_groups": all_rgs, "subnets": all_subnets}
        except Exception as e:
            self.logger.error(f"Erreur fatale dans le script principal: {e}")