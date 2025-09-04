from utils.logger_setup import Logger
from collectors.inventory_manager import InventoryManager
from config.settings import settings, VCENTER_CONFIGS, THREAD_POOL_SIZE
from agents.agent_manager import AgentManager


logger = Logger("main_app")
main_logger = logger.get_logger("main")
main_logger.info('Application démarrée')

# --- Inventory Collection and Processing ---
# inventory_manager = InventoryManager(settings)
# main_logger.info('Démarrage de l\'inventory des serveurs')
# all_inventory = inventory_manager.collect_and_process_all_servers_multithreaded()
# main_logger.info('Inventory des serveurs terminé')

agent_manager = AgentManager(settings)
all_agents = agent_manager.collect_and_process_all_servers_multithreaded()

main_logger.info('Application terminée')