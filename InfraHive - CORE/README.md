# InfraHive

## Overview
InfraHive is a robust and extensible inventory management and API integration solution designed to centralize and process infrastructure data from various sources. It leverages a multi-threaded architecture to efficiently collect server information, normalize it, and interact with external APIs (like Rapid7, Check_MK, Cortex, GLPI) to enrich the data.

## Features
- **Multi-Source Inventory Collection:** Gathers server data from diverse environments including vCenter, AWS, and Azure.
- **Data Normalization:** Standardizes raw data from different sources into a unified format using configurable strategies and mappings.
- **Multi-threaded Processing:** Utilizes worker threads for efficient, parallel processing of collected and API-enriched data.
- **API Integration:** Connects with external APIs (Rapid7, Check_MK, Cortex, GLPI) to fetch additional server-related information.
- **Database Integration:** Stores and manages normalized and enriched infrastructure data in a SQL Server database.
- **Configurable Dispatch Rules:** Dynamically determines which APIs to call for specific servers based on defined rules.
- **Comprehensive Logging:** Provides detailed logging for monitoring application flow and troubleshooting.

## Architecture Overview
InfraHive is structured into several key components:
- **`main.py`**: The entry point of the application, orchestrating the collection and processing workflows.
- **`collectors/`**: Contains modules responsible for gathering raw inventory data from different platforms (e.g., `aws_collector.py`, `azure_collector.py`, `vcenter_collector.py`).
- **`utils/`**: Provides utility functions, including data normalization (`data_normalizer.py`, `normalization_strategies.py`) and logging setup (`logger_setup.py`).
- **`db/`**: Manages database interactions, including connection pooling (`connection_pool.py`) and SQL queries (`queries.py`).
- **`api/`**: Houses modules for interacting with external APIs (`rapid7.py`, `checkmk.py`, `cortex.py`, `glpi.py`) and dispatching API calls based on rules (`api_dispatcher.py`, `api_processor.py`).
- **`connectors/`**: Contains low-level API connectors for various services (e.g., `rapid7_connector.py`, `cortex_connector.py`, `azure_connector.py`, `sql_connector.py`, `vcenter_connector.py`).
- **`workers/`**: Implements multi-threaded workers (`server_worker.py`, `api_worker.py`) to handle concurrent data processing.
- **`config/`**: Stores application settings (`settings.py`) and configuration files (`config.yaml`, `normalization_maps.yaml`).

## Setup

### Prerequisites
- Python 3.x
- SQL Server database
- ODBC Driver for SQL Server (e.g., `ODBC Driver 17 for SQL Server`)
- Required Python packages (listed in `requirements.txt`)

### Environment Variables
Create a `.env` file in the project root directory and populate it with your sensitive credentials and configurations. An example file `.env_exemple` is provided.

```
# Database Credentials (Example for HOSTING DB)
HOSTING_SERVER=your_db_server
HOSTING_DB=your_db_name
HOSTING_DB_USER=your_db_user
HOSTING_DB_USER_PWD=your_db_password

# Database Credentials (Example for OEIL DB)
OEIL_SERVER=your_oeil_db_server
OEIL_DB=your_oeil_db_name
OEIL_DB_USER=your_oeil_db_user
OEIL_DB_USER_PWD=your_oeil_db_password

# Rapid7 API
RAPID7_URL=https://your.rapid7.api.url
RAPID7_KEY=your_rapid7_api_key

# Cortex API
CORTEX_URL=https://your.cortex.api.url
CORTEX_KEY_ID=your_cortex_key_id
CORTEX_KEY=your_cortex_api_key

# Azure API
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret

# GLPI API
GLPI_APP_TOKEN=your_glpi_app_token
GLPI_USER_TOKEN=your_glpi_user_token

# VCenter Passwords (if using environment variables for passwords)
# VCENTER_PASSWORD_VCENTER1=your_vcenter1_password
# VCENTER_PASSWORD_VCENTER2=your_vcenter2_password

# Other Settings
THREAD_POOL_SIZE=10
LOG_LEVEL=INFO
```

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/InfraHive.git
    cd InfraHive
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration Files
-   **`config/config.yaml`**: Contains general application configurations, including Check_MK settings, GLPI base URL, vCenter connection details (excluding sensitive passwords which can be loaded from `.env`), and API dispatch rules.
-   **`config/normalization_maps.yaml`**: Defines rules for normalizing data from different sources to a common format.

Ensure these files are correctly configured according to your environment and requirements.

## Usage
To run the InfraHive application, execute the `main.py` script:

```bash
python main.py
```

The application will:
1.  Collect server inventory from configured sources.
2.  Process and normalize the collected data.
3.  Interact with external APIs based on dispatch rules to enrich server data.
4.  Store the processed data in the database.

## Extensibility

### Adding a New Collector
1.  Create a new collector module in `collectors/` (e.g., `new_collector.py`).
2.  Implement a `collect()` method within your new collector class that returns a list of server dictionaries in a raw format.
3.  Integrate the new collector into `inventory_manager.py` and `collect_all_servers_by_source()`.
4.  Define normalization rules for your new source in `config/normalization_maps.yaml` and potentially a new `NormalizationStrategy` in `utils/normalization_strategies.py`.

### Adding a New API Integration
1.  Create a new API module in `api/` (e.g., `new_api.py`).
2.  Implement methods to query the external API.
3.  Create a corresponding connector in `connectors/` if needed.
4.  Update `api_processor.py` to include calls to your new API.
5.  Define API dispatch rules in `config/config.yaml` to specify when your new API should be called.

## Logging
Application logs are stored in the `logs/` directory. The logging level and directory can be configured in `config/settings.py` and `config/config.yaml`.

## SQL Queries:

```SQL
SELECT s.server_name, e.env_code, o.os_name, a.agent_name, h.status, n.ip_address FROM server s, agents a, server_has_agent h, vinci_division v, environnement e, operating_system o, server_has_network n WHERE h.id_server = s.id_server AND a.id_agent = h.id_agent AND s.power_state LIKE '%ON' AND s.is_appliance=0 AND s.is_obsolete=0 AND v.division_code = 'VIC' AND v.id_vinci_division = s.id_vinci_division AND s.id_source = 3 AND e.id_environnement=s.id_environnement AND o.id_Operating_System=s.id_operating_system AND o.os_name NOT LIKE '%Windows%' AND o.os_name <> 'Unknown' AND h.status = 0 and n.ip_address IS NOT NULL ORDER BY e.env_code
```