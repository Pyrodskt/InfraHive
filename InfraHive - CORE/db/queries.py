class Queries:
    
    def upsert_agent_db(self, server, agent_name, status, conn):
        """
        Inserts or updates an agent's status for a given server in the database.

        Args:
            server (str): The name of the server.
            agent_name (str): The name of the agent.
            status (int): The status of the agent (e.g., 0 for inactive, 1 for active).
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = f"""
                    IF NOT EXISTS (
                        SELECT 1
                        FROM [KPI_HOSTING].[dbo].[server_has_agent] sha
                        JOIN [KPI_HOSTING].[dbo].[server] s ON sha.id_server = s.id_server
                        JOIN [KPI_HOSTING].[dbo].[agents] a ON sha.id_agent = a.id_agent
                        WHERE s.server_name = '{server}' AND a.agent_name = '{agent_name}'
                    )
                    BEGIN
                        INSERT INTO [KPI_HOSTING].[dbo].[server_has_agent] (
                            status, is_installable, id_server, id_agent
                        )
                        VALUES (
                            {status}, 1,
                            (SELECT id_server FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server}'),
                            (SELECT id_agent FROM [KPI_HOSTING].[dbo].[agents] WHERE agent_name = '{agent_name}')
                        );
                    END
                    ELSE
                    BEGIN
                        UPDATE sha
                        SET
                            status = {status}
                        FROM [KPI_HOSTING].[dbo].[server_has_agent] sha
                        JOIN [KPI_HOSTING].[dbo].[server] s ON sha.id_server = s.id_server
                        JOIN [KPI_HOSTING].[dbo].[agents] a ON sha.id_agent = a.id_agent
                        WHERE s.server_name = '{server}' AND a.agent_name = '{agent_name}';
                    END
                    """
            cursor.execute(query)
        conn.commit()
        
    def get_server_ip_addr(self, server, conn):
        """
        Retrieves the IP address of a given server from the database.

        Args:
            server (str): The name of the server.
            conn: The database connection object.

        Returns:
            list: A list of IP addresses found for the server.
        """
        with conn.cursor() as cursor:
            query = (
                f"SELECT ip_address FROM [KPI_HOSTING].[dbo].[server_has_network] where id_server = (SELECT id_server FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server}') and ip_address IS NOT NULL;"
            )
        return cursor.execute(query).fetchall()
    
    def get_all_servers(self, conn):
        """
        Retrieves all servers from the database.

        Args:
            conn: The database connection object.

        Returns:
            list: A list of dictionaries, where each dictionary represents a server
                  and its keys are column names.
        """
        with conn.cursor() as cursor:
            query = "SELECT * FROM [KPI_HOSTING].[dbo].[server];"
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            servers_data = []
            for row in cursor.fetchall():
                servers_data.append(dict(zip(columns, row)))
            return servers_data
    
    def update_r7_riskscore(self, server, r7_risk_score, conn):
        """
        Updates the Rapid7 risk score for a given server in the database.

        Args:
            server (str): The name of the server.
            r7_risk_score (float): The Rapid7 risk score.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = f"""
                        UPDATE server SET r7_risk_score = '{r7_risk_score}'
                        WHERE id_server = (SELECT id_server FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server}');
                    """
            cursor.execute(query)
        conn.commit()
        
    def update_server_os(self, server, os, description, conn):
        """
        Inserts a new operating system if it doesn't exist, then updates the server's OS.

        Args:
            server (str): The name of the server.
            os (str): The operating system name.
            description (str): The operating system description.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = f"""
                    IF NOT EXISTS (
                        SELECT 1
                        FROM [KPI_HOSTING].[dbo].[operating_system]
                        WHERE os_name = '{os}'
                        and os_description = '{os} {description}'
                    )
                    BEGIN
                    INSERT INTO [KPI_HOSTING].[dbo].[operating_system] (
                            os_name , os_description
                        )
                        VALUES (
                            '{os}',
                            '{os} {description}'	
                        );
                    END
                    ELSE
                    BEGIN
                        UPDATE server SET id_operating_system = (SELECT id_Operating_System FROM [KPI_HOSTING].[dbo].[operating_system] WHERE os_name = '{os}' and os_description = '{os} {description}')
                        WHERE id_server = (SELECT id_server FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server}')
                    END;
                    """
            cursor.execute(query)
        conn.commit()
        
    def upsert_network_db(self, server, netw, ip_addr, conn):
        """
        Inserts or updates network information for a given server in the database.

        Args:
            server (str): The name of the server.
            netw (str): The subnet name of the network.
            ip_addr (str): The IP address associated with the network.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = f"""
                    IF NOT EXISTS (
                        SELECT 1
                        FROM [KPI_HOSTING].[dbo].[server_has_network] sha
                        JOIN [KPI_HOSTING].[dbo].[server] s ON sha.id_server = s.id_server
                        JOIN [KPI_HOSTING].[dbo].[network] a ON sha.id_network = a.id_network
                        WHERE s.server_name = '{server}' AND a.subnet_name = '{netw}'
                    )
                    BEGIN
                        INSERT INTO [KPI_HOSTING].[dbo].[server_has_network] (
                            ip_address, id_network, id_server
                        )
                        VALUES (
                            '{ip_addr}',
                            (SELECT id_network FROM [KPI_HOSTING].[dbo].[network] WHERE subnet_name = '{netw}'),
                            (SELECT id_server FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server}')
                            
                        );
                    END
                    ELSE
                    BEGIN
                        UPDATE sha
                        SET
                            ip_address = '{ip_addr}'
                        FROM [KPI_HOSTING].[dbo].[server_has_network] sha
                        JOIN [KPI_HOSTING].[dbo].[server] s ON sha.id_server = s.id_server
                        JOIN [KPI_HOSTING].[dbo].[network] a ON sha.id_network = a.id_network
                        WHERE s.server_name = '{server}' AND a.subnet_name = '{netw}';
                    END
                    """
            
            cursor.execute(query)
        conn.commit()
        
    def insert_agent(self, agent_name, agent_process_name, agent_type, agent_criticity, has_api, conn):
        """
        Inserts a new agent into the AGENTS table if it does not already exist.

        Args:
            agent_name (str): The name of the agent.
            agent_process_name (str): The process name of the agent.
            agent_type (str): The type of the agent.
            agent_criticity (str): The criticality of the agent.
            has_api (bool): Indicates if the agent has an API.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = """
            INSERT INTO AGENTS (AGENT_NAME, AGENT_PROCESS_NAME, AGENT_TYPE, AGENT_CRITICITY, HAS_API)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM AGENTS WHERE AGENT_NAME = ?);
            """
            values = (
                agent_name,
                agent_process_name,
                agent_type,
                agent_criticity,
                has_api,
                agent_name
            )
            cursor.execute(query, values)
        conn.commit()
        
    def insert_application(self, app_name, app_code, conn):
        """
        Inserts a new application into the APPLICATION table if it does not already exist.

        Args:
            app_name (str): The name of the application.
            app_code (str): The code of the application.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = """
            INSERT INTO APPLICATION (app_name, app_code)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM APPLICATION WHERE APP_CODE = ?);
            """
            values = (
                app_name,
                app_code,
                app_code
            )
            cursor.execute(query, values)
        conn.commit()
    
    def insert_unknown_application(self, conn):
        """
        Inserts a default 'Unknown' application into the APPLICATION table if it does not already exist.

        Args:
            conn: The database connection object.
        """
        with conn.cursor() as cursor:

            query = """
            INSERT INTO APPLICATION (app_name, app_code)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM APPLICATION WHERE APP_CODE = ?);
            """
            values = (
                "Unknown",
                "UKN",
                "UKN"
            )
            cursor.execute(query, values)
        conn.commit()
        
    def insert_division(self, div_name, div_code, conn):
        """
        Inserts a new division into the VINCI_DIVISION table if it does not already exist.

        Args:
            div_name (str): The name of the division.
            div_code (str): The code of the division.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:

            query = """
            INSERT INTO VINCI_DIVISION (DIVISION_NAME, DIVISION_CODE)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM VINCI_DIVISION WHERE DIVISION_CODE = ?);
            """
            values = (
                div_name,
                div_code,
                div_code
            )
            cursor.execute(query, values)
        conn.commit()
    
    def insert_unknown_division(self, conn):
        """
        Inserts a default 'Unknown' division into the VINCI_DIVISION table if it does not already exist.

        Args:
            conn: The database connection object.
        """
        with conn.cursor() as cursor:

            query = """
            INSERT INTO VINCI_DIVISION (DIVISION_NAME, DIVISION_CODE)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM VINCI_DIVISION WHERE DIVISION_CODE = ?);
            """
            values = (
                "Unknown",
                "UKN",
                "UKN"
            )
            cursor.execute(query, values)
        conn.commit()

    def insert_env(self, env_name, env_code, conn):
        """
        Inserts a new environment into the ENVIRONNEMENT table if it does not already exist.

        Args:
            env_name (str): The name of the environment.
            env_code (str): The code of the environment.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = """
            INSERT INTO ENVIRONNEMENT (ENV_NAME, ENV_CODE)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM ENVIRONNEMENT WHERE ENV_CODE = ?);
            """
            values = (
                env_name,
                env_code,
                env_code
            )
            cursor.execute(query, values)
        conn.commit()

    def insert_unknown_env(self, conn):
        """
        Inserts a default 'Unknown' environment into the ENVIRONNEMENT table if it does not already exist.

        Args:
            conn: The database connection object.
        """
        with conn.cursor() as cursor:

            query = """
            INSERT INTO ENVIRONNEMENT (ENV_NAME, ENV_CODE)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM ENVIRONNEMENT WHERE ENV_CODE = ?);
            """
            values = (
                "Unknown",
                "UKN",
                "UKN"
            )
            cursor.execute(query, values)
        conn.commit()
        
    def get_unknown_division(self, div_code, conn):
        """
        Retrieves the ID of a division based on its code.

        Args:
            div_code (str): The code of the division (e.g., 'UKN' for unknown).
            conn: The database connection object.

        Returns:
            int: The ID of the division.
        """
        with conn.cursor() as cursor:

            query = """
            SELECT id_vinci_division FROM vinci_division WHERE DIVISION_CODE = ?;
            """
            values = (
                div_code,
            )
            cursor.execute(query, values)
        conn.commit()
        return cursor.fetchone()[0]

    def insert_network(self, netw, div_code, conn):
        """
        Inserts a new network into the NETWORK table if it does not already exist.

        Args:
            netw (list): A list containing the subnet name (e.g., ['subnet_name']).
            div_code (str): The code of the division associated with the network.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            id_unknown_div = self.get_unknown_division(conn, div_code)
            is_dmz = False
            if 'DMZ' in netw[0].upper():
                is_dmz = True

            query = """
            INSERT INTO NETWORK (subnet_name, is_dmz, id_vinci_division, vnet_name)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM NETWORK WHERE subnet_name = ?);
            """
            values = (
                netw[0].lower(),
                is_dmz,
                id_unknown_div,
                None,
                netw[0].lower()
            )


            cursor.execute(query, values)
        conn.commit()
    
    def insert_role(self, role_name, role_description, conn):
        """
        Inserts a new server role into the SERVER_ROLE table if it does not already exist.

        Args:
            role_name (str): The code of the server role.
            role_description (str): The description of the server role.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:

            query = """
            INSERT INTO SERVER_ROLE (ROLE_CODE, ROLE_DESCRIPTION)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM SERVER_ROLE WHERE ROLE_CODE = ?);
            """
            values = (
                role_name,
                role_description,
                role_name
            )
            cursor.execute(query, values)
        conn.commit()

    def insert_unknown_role(self, conn):
        """
        Inserts a default 'Unknown' server role into the SERVER_ROLE table if it does not already exist.

        Args:
            conn: The database connection object.
        """
        with conn.cursor() as cursor:

            query = """
            INSERT INTO SERVER_ROLE (ROLE_CODE, ROLE_DESCRIPTION)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM SERVER_ROLE WHERE ROLE_CODE = ?);
            """
            values = (
                "UKN",
                "Unknown",
                "UKN"
            )
            cursor.execute(query, values)
        conn.commit()

    def insert_source(self, source_name, source_desc, conn):
        """
        Inserts a new server source into the SERVER_SOURCE table if it does not already exist.

        Args:
            source_name (str): The name of the source.
            source_desc (str): The description of the source.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = """
            INSERT INTO SERVER_SOURCE (SOURCE_NAME, SOURCE_DESCRIPTION)
            SELECT ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM SERVER_SOURCE WHERE SOURCE_NAME = ?);
            """
            values = (
                source_name,
                source_desc,
                source_name
            )
            cursor.execute(query, values)
        conn.commit()

    def insert_tier(self, tier_name, conn):
        """
        Inserts a new server tier into the SERVER_TIER table if it does not already exist.

        Args:
            tier_name (str): The name of the tier.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = """
            INSERT INTO SERVER_TIER (TIER_NAME)
            SELECT ?
            WHERE NOT EXISTS (SELECT 1 FROM SERVER_TIER WHERE TIER_NAME = ?);
            """
            values = (
                tier_name,
                tier_name
            )
            cursor.execute(query, values)
        conn.commit()
    
    def insert_server_in_db(self, server, conn):
        """
        Inserts a new server into the database if it does not already exist.
        Handles mapping of tier and division values.

        Args:
            server (dict): A dictionary containing server details.
            conn: The database connection object.
        """
        tier = 'Unknown'
        if server['tier'] == 'T1':
            server['tier'] = 'Tier 1'
        elif server['tier'] == 'T0':
            server['tier'] = 'Tier 0'
        else:
            server['tier'] = 'Unknown'
        if server['division'] == 'VCGP':
            server['division'] = 'VGP'

        with conn.cursor() as cursor:
            query = (
                f"IF NOT EXISTS (SELECT 1 FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server['name']}') "
                f"BEGIN "
                f"INSERT INTO [KPI_HOSTING].[dbo].[server] ("
                f"server_name, is_appliance, is_obsolete, power_state, r7_risk_score, "
                f"id_operating_system, id_application, id_server_role, id_tier, id_source, "
                f"cloud_subscription, id_environnement, id_vinci_division) "
                f"VALUES ("
                f"'{server['name']}', "
                f"0, "
                f"0, "
                f"'{server['power_state']}', "
                f"NULL, "
                f"ISNULL((SELECT id_Operating_System FROM [KPI_HOSTING].[dbo].[operating_system] WHERE os_name = '{server['guest_OS']}'), "
                f"      (SELECT id_Operating_System FROM [KPI_HOSTING].[dbo].[operating_system] WHERE os_name = 'Unknown')), "

                f"ISNULL((SELECT id_application FROM [KPI_HOSTING].[dbo].[application] WHERE app_code = '{server['app']}'), "
                f"      (SELECT id_application FROM [KPI_HOSTING].[dbo].[application] WHERE app_code = 'UKN')), "

                f"ISNULL((SELECT id_server_role FROM [KPI_HOSTING].[dbo].[server_role] WHERE role_code = '{server['role']}'), "
                f"        (SELECT id_server_role FROM [KPI_HOSTING].[dbo].[server_role] WHERE role_code = 'UKN')), "

                f"ISNULL((SELECT id_tier FROM [KPI_HOSTING].[dbo].[server_tier] WHERE tier_name = '{server['tier']}'), "
                f"        (SELECT id_tier FROM [KPI_HOSTING].[dbo].[server_tier] WHERE tier_name = 'Unknown')), "

                f"ISNULL((SELECT id_source FROM [KPI_HOSTING].[dbo].[server_source] WHERE source_name = '{server['source']}'), "
                f"        (SELECT id_source FROM [KPI_HOSTING].[dbo].[server_source] WHERE source_name = 'Unknown')), "

                f"NULL, "

                f"ISNULL((SELECT id_environnement FROM [KPI_HOSTING].[dbo].[environnement] WHERE env_code = '{server['env']}'), "
                f"        (SELECT id_environnement FROM [KPI_HOSTING].[dbo].[environnement] WHERE env_code = 'UKN')), "

                f"ISNULL((SELECT id_vinci_division FROM [KPI_HOSTING].[dbo].[vinci_division] WHERE division_code = '{server['division']}'), "
                f"        (SELECT id_vinci_division FROM [KPI_HOSTING].[dbo].[vinci_division] WHERE division_code = 'UKN')) "
                f"); "
                f"END;"
            )
            cursor.execute(query)
        conn.commit()
    
    def insert_network_of_server(self, server, network, conn):
        """
        Inserts a network association for a server if it does not already exist.

        Args:
            server (dict): A dictionary containing server details (e.g., 'name').
            network (str): The subnet name of the network to associate.
            conn: The database connection object.
        """
        with conn.cursor() as cursor:
            query = (
                f"IF EXISTS (SELECT 1 FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server['name']}') "
                f"AND NOT EXISTS ("
                f"    SELECT 1 FROM [KPI_HOSTING].[dbo].[server_has_network] shn "
                f"    JOIN [KPI_HOSTING].[dbo].[server] s ON s.id_server = shn.id_server "
                f"    JOIN [KPI_HOSTING].[dbo].[network] n ON n.id_network = shn.id_network "
                f"    WHERE s.server_name = '{server['name']}' AND n.subnet_name = '{network}'"
                f") "
                f"BEGIN "
                f"INSERT INTO [KPI_HOSTING].[dbo].[server_has_network] "
                f"(ip_address, id_server, id_network) "
                f"VALUES ("
                f"NULL, "
                f"(SELECT id_server FROM [KPI_HOSTING].[dbo].[server] WHERE server_name = '{server['name']}'), "
                f"ISNULL((SELECT id_network FROM [KPI_HOSTING].[dbo].[network] WHERE subnet_name = '{network}'), "
                f"      (SELECT id_network FROM [KPI_HOSTING].[dbo].[network] WHERE subnet_name = 'Unknown')) "
                f"); "
                f"END;"
            )
            cursor.execute(query)
        conn.commit()
