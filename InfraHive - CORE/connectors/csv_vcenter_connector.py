import csv
class CSVVcenterConnector:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def import_csv(self):
        with open(self.filepath, newline="", mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            content = []
            for row in csv_reader:
                content.append(row)
        return content
    
    def collect(self):
        servers = self.import_csv()
        all_servers = []
        for serv in servers:
            all_servers.append({
                "name": serv['VM'],
                "guest_OS": serv["OS according to the VMware Tools"],
                "power_state": serv['Powerstate'],
                "source": "NGDT",
                "tier": "T0",
                "networks": [serv[f'Network #{i}'] for i in range(1, 9) if serv[f'Network #{i}'] != ""],
                "ip_address": serv['Primary IP Address']
            })
        return all_servers