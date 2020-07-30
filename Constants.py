import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

NUM_TASKS_CREATED_DATA_KEY = 'bot_num_tasks_created'

CANCEL_CONV_PROMPT = "Send /cancel to terminate this command."
