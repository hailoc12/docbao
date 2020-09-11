import os
from src.backend.lib.data import ArticleManager
from src.backend.lib.rabbitmq_client import RabbitMQ_Client
from src.backend.lib.utils import get_independent_os_path

base_dir = os.environ['DOCBAO_BASE_DIR']

rb = RabbitMQ_Client()
rb.connect()
data_manager = ArticleManager(None, get_independent_os_path([base_dir, 'src', 'backend', 'data', 'article.dat']),get_independent_os_path([base_dir, 'src', 'backend', "data","blacklist.dat"]) ) #article database object
data_manager.load_data()

print("PUSH ALL ARTICLES TO RABBITMQ")
rb.push_to_queue(data_manager._data.values())
