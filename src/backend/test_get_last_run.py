from lib.utils import *
from lib.config import *
import time

config_manager = ConfigManager(get_independent_os_path(['input', 'config.txt']))
config_manager.load_data()
first_newspaper = config_manager.get_newspaper_list()[0]
print("get last run:" + str(first_newspaper.get_last_run()))
time.sleep(5)
first_newspaper.set_last_run()

print("set new last run: " + str(first_newspaper.get_last_run()))
print("save data")
config_manager.save_data()
print("OK")
