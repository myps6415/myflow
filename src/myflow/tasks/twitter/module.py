import os
import random
import re
import time
from typing import List

import m3u8
from pymongo import DESCENDING
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

from ..utils import MongoDBConfig, SeleniumConfig


class FetchTwitter(MongoDBConfig, SeleniumConfig):
    def __init__(self):
        MongoDBConfig.__init__(self)
        SeleniumConfig.__init__(self)

    @classmethod
    def get_twitter_urls(cls) -> List[str]:
        instance = cls()
        twitter_urls = [
            url["url"]
            for url in instance.db["twitter_source"]
            .find({"status": 1}, {"url": 1, "_id": 0})
            .sort("fetched_datetime", DESCENDING)
            .limit(5)
        ]
        return twitter_urls

    @classmethod
    def run(cls, **context) -> List[str]:
        instance = cls()
        twitter_urls = context["ti"].xcom_pull(task_ids="get_twitter_urls")
        twitter_account = os.environ.get("twitter_account")
        twitter_password = os.environ.get("twitter_password")

        executor = "http://seleniarm-hub:4444"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server=http://airflow-mitmproxy-1:8080")
        chrome_options.add_argument("--ignore-certificate-errors")

        driver = webdriver.Remote(
            command_executor=executor,
            options=chrome_options,
            seleniumwire_options=instance.sw_options,
        )

        driver.get("https://twitter.com/login")

        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input',
                )
            )
        )
        username.send_keys(twitter_account)
        username.send_keys(Keys.RETURN)
        time.sleep(instance.sleep_time)

        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
                )
            )
        )
        password.send_keys(twitter_password)
        password.send_keys(Keys.RETURN)
        time.sleep(instance.sleep_time)

        pattern = r"\/(\d+)\/"

        for twitter_url in twitter_urls:
            driver.get(twitter_url)
            time.sleep(instance.sleep_time)
            driver.scopes = [".*"]
            driver.refresh()

            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 向下滑动五次
            for _ in range(5):
                driver.execute_script("window.scrollBy(0, 1500);")
                time.sleep(instance.sleep_time)
                print(driver.requests)
