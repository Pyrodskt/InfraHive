from sqlalchemy import create_engine, select, insert, update, delete
from sqlalchemy.orm import sessionmaker, Session
from db.db_model import *
import urllib.parse
from config.settings import Settings
from datetime import date
from typing import Optional, List
settings = Settings()
params = urllib.parse.quote_plus(
    f"DRIVER={settings.DRIVER};SERVER={settings.HOSTING_SERVER};DATABASE={settings.HOSTING_DB};UID={settings.HOSTING_DB_USER};PWD={settings.HOSTING_DB_USER_PWD}"
)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(connection_string)

# `SessionLocal` est une fabrique de sessions, elle ne crée pas de session elle-même.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class DBQueries:
    def __init__(self, session=SessionLocal):
        """
        Initialise la classe de requêtes avec une session de base de données.
        
        Args:
            session (Session): La session de base de données SQLAlchemy à utiliser.
        """
        self.session = session
    
    def upsert_agent_db(self, server_name: str, agent_name: str, status: bool):
        """
        Inserts or updates an agent's status for a given server.
        """
        # 1. Récupérer les objets Server et Agents
        server = self.session.scalars(select(Server).where(Server.server_name == server_name)).first()
        agent = self.session.scalars(select(Agents).where(Agents.agent_name == agent_name)).first()

        if not server or not agent:
            # Gérer le cas où le serveur ou l'agent n'existe pas
            return

        # 2. Chercher la relation existante
        link = self.session.scalars(
            select(ServerHasAgent)
            .where(ServerHasAgent.server == server, ServerHasAgent.agent == agent)
        ).first()

        # 3. Effectuer l'upsert
        if link:
            link.status = status
            link.update_date = date.today().strftime('%Y-%m-%d')
        else:
            new_link = ServerHasAgent(
                server=server, 
                agent=agent, 
                status=status, 
                is_installable=True
            )
            self.session.add(new_link)
        self.session.commit()

    def get_server_ip_addr(self, server_name: str) -> List[str]:
        """
        Retrieves the IP address of a given server.
        """
        # SQLAlchemy gère les jointures automatiquement
        ip_addresses = self.session.scalars(
            select(ServerHasNetwork.ip_address)
            .join(Server)
            .where(Server.server_name == server_name, ServerHasNetwork.ip_address.is_not(None))
        ).all()
        return ip_addresses

    def get_all_servers(self):
        """
        Retrieves all servers from the database.
        """
        # L'ORM retourne directement une liste d'objets Server
        
        return self.session.scalars(select(Server)).all()

    def update_r7_riskscore(self, server_name: str, r7_risk_score: Optional[float]):
        """
        Updates the Rapid7 risk score for a given server.
        """
        # Rechercher le serveur par son nom et mettre à jour l'attribut
        server = self.session.scalars(select(Server).where(Server.server_name == server_name)).first()
        if server:
            server.r7_risk_score = r7_risk_score
            self.session.commit()

    def update_server_os(self, server_name: str, os_name: str, description: str):
        """
        Inserts a new operating system if it doesn't exist, then updates the server's OS.
        """
        # 1. Rechercher ou créer l'OS
        os_obj = self.session.scalars(
            select(OperatingSystem).where(
                OperatingSystem.os_name == os_name, 
                OperatingSystem.os_description == f"{os_name} {description}"
            )
        ).first()

        if not os_obj:
            os_obj = OperatingSystem(os_name=os_name, os_description=f"{os_name} {description}")
            self.session.add(os_obj)
            self.session.flush() # pour s'assurer que l'objet a un ID

        # 2. Mettre à jour le serveur
        server_obj = self.session.scalars(select(Server).where(Server.server_name == server_name)).first()
        if server_obj:
            server_obj.operating_system = os_obj
            self.session.commit()

    def upsert_network_db(self, server_name: str, netw_name: str, ip_addr: Optional[str]):
        """
        Inserts or updates network information for a given server.
        """
        server = self.session.scalars(select(Server).where(Server.server_name == server_name)).first()
        network = self.session.scalars(select(Network).where(Network.subnet_name == netw_name)).first()

        if not server or not network:
            return

        link = self.session.scalars(
            select(ServerHasNetwork)
            .where(ServerHasNetwork.server == server, ServerHasNetwork.network == network)
        ).first()

        if link:
            link.ip_address = ip_addr
        else:
            new_link = ServerHasNetwork(server=server, network=network, ip_address=ip_addr)
            self.session.add(new_link)
        
        self.session.commit()
    
    def insert_if_not_exists(self, model, key_attr, value, other_attrs=None):
        """
        Générique pour insérer un objet s'il n'existe pas.
        """
        obj = self.session.scalars(select(model).where(key_attr == value)).first()
        if not obj:
            obj = model(**{key_attr.key: value}, **(other_attrs or {}))
            self.session.add(obj)
            self.session.flush()
        return obj

    def get_unknown_division(self, div_code: str):
        """
        Récupère l'ID d'une division "Unknown".
        """
        # Simplifie votre méthode qui faisait une requête SQL
        div = self.session.scalars(select(VinciDivision).where(VinciDivision.division_code == div_code)).first()
        if div:
            return div.id_vinci_division
        return None

    def insert_agent(self, agent_name, agent_process_name, agent_type, agent_criticity, has_api):
        self.insert_if_not_exists(
            Agents,
            Agents.agent_name,
            agent_name,
            {'agent_process_name': agent_process_name, 'agent_type': agent_type, 'agent_criticity': agent_criticity, 'has_api': has_api}
        )
        self.session.commit()

    def insert_application(self, app_name, app_code):
        self.insert_if_not_exists(
            Application,
            Application.app_code,
            app_code,
            {'app_name': app_name}
        )
        self.session.commit()

    def insert_unknown_application(self):
        self.insert_application("Unknown", "UKN")
    
    def insert_division(self, div_name, div_code):
        self.insert_if_not_exists(
            VinciDivision,
            VinciDivision.division_code,
            div_code,
            {'division_name': div_name}
        )
        self.session.commit()

    def insert_unknown_division(self):
        self.insert_division("Unknown", "UKN")

    def insert_env(self, env_name, env_code):
        self.insert_if_not_exists(
            Environnement,
            Environnement.env_code,
            env_code,
            {'env_name': env_name}
        )
        self.session.commit()

    def insert_unknown_env(self):
        self.insert_env("Unknown", "UKN")

    def insert_network(self, netw, div_code):
        is_dmz = 'DMZ' in netw[0].upper()
        # D'abord, on s'assure que la division existe
        div = self.session.scalars(select(VinciDivision).where(VinciDivision.division_code == div_code)).first()
        
        if div:
            self.insert_if_not_exists(
                Network,
                Network.subnet_name,
                netw[0].lower(),
                {'is_dmz': is_dmz, 'vinci_division': div}
            )
            self.session.commit()
    
    def insert_role(self, role_name, role_description):
        self.insert_if_not_exists(
            ServerRole,
            ServerRole.role_code,
            role_name,
            {'role_description': role_description}
        )
        self.session.commit()

    def insert_unknown_role(self):
        self.insert_role("UKN", "Unknown")

    def insert_source(self, source_name, source_desc):
        self.insert_if_not_exists(
            ServerSource,
            ServerSource.source_name,
            source_name,
            {'source_description': source_desc}
        )
        self.session.commit()

    def insert_tier(self, tier_name):
        self.insert_if_not_exists(
            ServerTier,
            ServerTier.tier_name,
            tier_name
        )
        self.session.commit()
    
    def insert_server_in_db(self, server_data: dict):
        """
        Inserts a new server into the database if it does not already exist.
        """
        # Chercher le serveur existant
        server_obj = self.session.scalars(
            select(Server).where(Server.server_name == server_data['name'])
        ).first()

        sub_name = server_data.get('souscription_name')
        rg_name = server_data.get('rg_name')
        sub_obj = None
        if sub_name and rg_name:
            sub_obj = self.session.scalar(
                select(CloudSubscription).where(
                    CloudSubscription.sub_name == sub_name,
                    CloudSubscription.rg_name == rg_name
                )
            )
        # else:
        #     # Si les données de souscription sont manquantes, utiliser l'abonnement "Unknown"
        #     sub_obj = self.session.scalar(
        #         select(CloudSubscription).where(CloudSubscription.sub_name == 'Unknown')
        #     )
        #     # Cas d'erreur si l'abonnement 'Unknown' n'a pas été pré-inséré
        #     if not sub_obj:
        #         return
        if server_obj:
            server_obj.update_date = date.today().strftime('%Y-%m-%d')
            server_obj.server_source =  self.session.scalars(select(ServerSource).where(ServerSource.source_name == server_data.get('source', 'Unknown'))).first()
            server_obj.id_cloud_subscription = sub_obj.id_cloud_subscription if sub_obj else None

            self.session.commit()
            return

        # 1. Traiter les données brutes
        tier_name = server_data['tier']
        if tier_name == 'T1':
            tier_name = 'Tier 1'
        elif tier_name == 'T0':
            tier_name = 'Tier 0'
        else:
            tier_name = 'Unknown'
            
        division_code = server_data['division']
        if division_code == 'VCGP':
            division_code = 'VGP'
        else:
            division_code = division_code
            
        # 2. Récupérer les objets liés ou les objets "Unknown"
        os_obj = self.session.scalars(select(OperatingSystem).where(OperatingSystem.os_name == server_data.get('guest_OS', 'Unknown'))).first()
        if not os_obj:
            os_obj = self.session.scalars(select(OperatingSystem).where(OperatingSystem.os_name == 'Unknown')).first()
            if not os_obj: return # Gérer le cas où 'Unknown' n'existe pas
        
        app_obj = self.session.scalars(select(Application).where(Application.app_code == server_data.get('app', 'UKN'))).first()
        if not app_obj:
            app_obj = self.session.scalars(select(Application).where(Application.app_code == 'UKN')).first()
            if not app_obj: return

        role_obj = self.session.scalars(select(ServerRole).where(ServerRole.role_code == server_data.get('role', 'UKN'))).first()
        if not role_obj:
            role_obj = self.session.scalars(select(ServerRole).where(ServerRole.role_code == 'UKN')).first()
            if not role_obj: return

        tier_obj = self.session.scalars(select(ServerTier).where(ServerTier.tier_name == tier_name)).first()
        if not tier_obj:
            tier_obj = self.session.scalars(select(ServerTier).where(ServerTier.tier_name == 'Unknown')).first()
            if not tier_obj: return

        source_obj = self.session.scalars(select(ServerSource).where(ServerSource.source_name == server_data.get('source', 'Unknown'))).first()
        if not source_obj:
            source_obj = self.session.scalars(select(ServerSource).where(ServerSource.source_name == 'Unknown')).first()
            if not source_obj: return
            
        env_obj = self.session.scalars(select(Environnement).where(Environnement.env_code == server_data.get('env', 'UKN'))).first()
        if not env_obj:
            env_obj = self.session.scalars(select(Environnement).where(Environnement.env_code == 'UKN')).first()
            if not env_obj: return

        div_obj = self.session.scalars(select(VinciDivision).where(VinciDivision.division_code == division_code)).first()
        if not div_obj:
            div_obj = self.session.scalars(select(VinciDivision).where(VinciDivision.division_code == 'UKN')).first()
            if not div_obj: return
        
            
        # 3. Créer le nouvel objet Server avec ses relations
        new_server = Server(
            server_name=server_data['name'],
            is_appliance=False,
            is_obsolete=False,
            power_state=server_data['power_state'],
            r7_risk_score=None,
            operating_system=os_obj,
            application=app_obj,
            server_role=role_obj,
            server_tier=tier_obj,
            server_source=source_obj,
            environnement=env_obj,
            vinci_division=div_obj,
            id_cloud_subscription=sub_obj.id_cloud_subscription if sub_obj else None
        )
        self.session.add(new_server)
        self.session.commit()
    
    def insert_networks_of_server(self, server_data: dict):
        """
        Inserts a network association for a server if it does not already exist.
        """
        for netw in server_data['networks']:
            
            server = self.session.scalars(select(Server).where(Server.server_name == server_data['name'])).first()
            if not server:
                return

            network = self.session.scalars(select(Network).where(Network.subnet_name == netw)).first()
            if not network:
                # Assurez-vous que le réseau 'Unknown' est inséré si nécessaire
                network = self.session.scalars(select(Network).where(Network.subnet_name == 'Unknown')).first()
                if not network:
                    return

            link = self.session.scalars(
                select(ServerHasNetwork).where(
                    ServerHasNetwork.server == server, 
                    ServerHasNetwork.network == network
                )
            ).first()

            if not link:
                new_link = ServerHasNetwork(server=server, network=network, ip_address=None)
                self.session.add(new_link)
                self.session.commit()

    def upsert_subscription(self, sub_data: dict):
        """
        Insère ou met à jour un enregistrement de souscription.
        """
        # 1. Remplacement des fonctions get_id par des requêtes SQLAlchemy
        #    Note: Utilisation de `select` pour une meilleure pratique (SQLAlchemy 2.0 style)
        
        # Récupère l'ID de l'environnement
        env_stmt = select(Environnement).where(Environnement.env_code == sub_data['sub_env'])
        environnement = self.session.execute(env_stmt).scalars().first()
        id_env = environnement.id_environnement if environnement else None
        
        # Récupère l'ID de la division
        div_stmt = select(VinciDivision).where(VinciDivision.division_code == sub_data['sub_div'])
        division = self.session.execute(div_stmt).scalars().first()
        id_div = division.id_vinci_division if division else None
        
        # Récupère l'ID du tier
        tier_stmt = select(ServerTier).where(ServerTier.tier_name == sub_data['sub_tier'])
        tier = self.session.execute(tier_stmt).scalars().first()
        id_tier = tier.id_tier if tier else None
        
        # Récupère l'ID de la source
        src_stmt = select(ServerSource).where(ServerSource.source_name == sub_data['cloud_provider'])
        src = self.session.execute(src_stmt).scalars().first()
        id_src = src.id_source if src else None
        # 2. Implémentation de la logique "upsert" (recherche puis insertion)
        stmt = select(CloudSubscription).where(
            CloudSubscription.sub_id == sub_data['sub_id'],
            CloudSubscription.rg_name == sub_data['rg_name']
        )
        existing_sub = self.session.execute(stmt).scalars().first()
        
        if existing_sub:
            # # L'enregistrement existe, mise à jour (logique optionnelle)
            # # Vous pouvez mettre à jour d'autres colonnes si nécessaire
            # existing_sub.sub_name = sub_data.get('sub_name', existing_sub.sub_name)
            # existing_sub.id_vinci_division = id_div
            # existing_sub.id_environnement = id_env
            # existing_sub.id_tier = id_tier
            # existing_sub.update_date = datetime.now()
            # self.session.add(existing_sub)
            return existing_sub
        else:
            # L'enregistrement n'existe pas, on l'insère
            new_sub = CloudSubscription(
                sub_id=sub_data['sub_id'],
                sub_name=sub_data['sub_name'],
                id_source=id_src, # Valeur en dur
                rg_name=sub_data['rg_name'],
                id_vinci_division=id_div,
                id_environnement=id_env,
                id_tier=id_tier
            )
            self.session.add(new_sub)
            return new_sub

    def upsert_network(self, subnet_data: dict):
        """
        Insère un enregistrement de sous-réseau s'il n'existe pas déjà.
        """
        # Remplacement de la fonction get par une requête SQLAlchemy
        div_stmt = select(VinciDivision).where(VinciDivision.division_code == subnet_data['id_div'])
        division = self.session.execute(div_stmt).scalars().first()
        id_div = division.id_vinci_division if division else None
        
        # 1. Rechercher si le sous-réseau existe déjà
        stmt = select(Network).where(Network.subnet_name == subnet_data['subnet_name'])
        existing_subnet = self.session.execute(stmt).scalars().first()

        if not existing_subnet:
            # 2. Si le sous-réseau n'existe pas, l'insérer
            new_subnet = Network(
                subnet_name=subnet_data['subnet_name'],
                is_dmz=subnet_data['is_dmz'],
                vnet_name=subnet_data['vnet_name'],
                id_vinci_division=id_div
            )
            self.session.add(new_subnet)
            return new_subnet
        else:
            # 3. S'il existe, retourner l'objet existant (pas de mise à jour par défaut)
            return existing_subnet

    def get_required_agents_to_check(self):
        """
        Récupère tous les enregistrements ServerHasAgent où is_required est True.
        """
        stmt = select(ServerHasAgent).where(ServerHasAgent.is_required == True)
        return self.session.scalars(stmt).all()

    def update_agent_status(self, server_has_agent_obj: ServerHasAgent, status: bool):
        """
        Met à jour le statut et le commentaire d'un agent sur un serveur donné.
        """
        server_has_agent_obj.status = status
        server_has_agent_obj.update_date = date.today()
        
