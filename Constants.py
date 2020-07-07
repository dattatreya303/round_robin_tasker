import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# TOKEN = "958111367:AAFbNEDl0V6KJxKLq64P0zHf2YwWefo4Mxc"
# TOKEN_TEST = "1243699574:AAEMQzMsmHlyNqpueSZo9xaq6zFsGBwuV8g"

# FILENAME_PKL = '/Users/dattatreyamohapatra/round_robin_tasker_project/data/chat_task_data.pkl'

# MYSQL_USER = "dattatreya303"
# MYSQL_PWD = "roundrobin@2020"
# MYSQL_DB = "dattatreya303$round-robin-tasker-bot"

NUM_TASKS_CREATED_DATA_KEY = 'bot_num_tasks_created'

CANCEL_CONV_PROMPT = "Send /cancel to terminate this command."
