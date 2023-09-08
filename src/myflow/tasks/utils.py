import os
import random

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

from cleflexlake.connect_db.mongo import Connection


class MongoDBConfig:
    def __init__(self):
        self.host = os.environ.get("host", "localhost")
        self.port = int(os.environ.get("port", 27017))
        self.username = os.environ.get("username", "")
        self.password = os.environ.get("password")
        self.database = "crawler_projects"
        self.client, self.db = Connection.connect_mongodb(
            self.host, self.port, self.username, self.password, self.database
        )


class SeleniumConfig:
    def __init__(self) -> None:
        self.sw_options = {
            "auto_config": False,  # Ensure this is set to False
            "addr": "0.0.0.0",  # The address the proxy will listen on
            "port": 8080,  # The port the proxy will listen on
        }

        self.sleep_time = random.randint(3, 7)
