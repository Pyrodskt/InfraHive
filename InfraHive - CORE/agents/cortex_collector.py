import requests
import json
from connectors.cortex_connector import Cortex
from datetime import datetime

#has_cortex_agent = []
class CortexAPI:
	def __init__(self):
		"""
		Initializes the CortexAPI client.
		"""
		pass

	def query_cortex_by_server(self, name, ip, is_appliance):
		"""
		Queries the Cortex XDR API for server information based on IP address.

		Args:
			name (str): The name of the server.
			ip (str): The IP address of the server.
			is_appliance (bool): Indicates if the server is an appliance.

		Returns:
			dict: A dictionary containing agent status and server details.
		"""
		tdy = datetime.now().strftime('%Y-%m-%d')
		CortexConnector = Cortex()
		payload = json.dumps({
			"request_data": {
				"filters": [
					{
						"field": "ip_list",
						"operator": "in",
						"value": [ip]
					}
				]
			}
		})

		response = requests.request("POST", CortexConnector.url, headers=CortexConnector.headers, data=payload)
		response.raise_for_status()
		data = response.text
		dict_data = json.loads(data)

		#= Default value
		is_installed = False

		if(dict_data['reply']['result_count'] == 1):
			if (dict_data['reply']['endpoints'][0]['endpoint_status'] == "CONNECTED"):
				# print(f"{name} - {ip} : CORTEX OK")
				is_installed = True

		has_agent_data = {
			"is_installed": is_installed,
			"is_installable": not 	is_appliance,
			"comment": None,
			"update_date": tdy,
			"server_name": name,
		}
		return has_agent_data

