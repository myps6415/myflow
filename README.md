# myflow
## Hello Ralph
Thank you for helping me to find the problems.

I think I need to introduce myself first. My name is Hsiao-Yu, and I live in Taiwan. My current job is data engineer. My mother language is Chinese, so I am trying my best to write in English.

Here is the [docker-compose.yml](/docker/airflow/docker-compose.yml) file.

Here, as you can see, the setting of airflow is the same as the official. (https://airflow.apache.org/docs/apache-airflow/2.7.1/docker-compose.yaml)

### Installation Steps
#### Step.1 Build image
```
docker build -t hsiaoyu/airflow:1.0.0 . --no-cache
```
#### Step.2 Initialize the database
```
docker-compose up airflow-init
```
#### Step.3 Running Airflow
```
docker-compose up -d
```

### Introduction
I think because my code needs to be executed within the container, I need to start a proxy server to provide services.

So, as you can see in the docker-compose.yml I add mitmproxy below, and I will set selenium-wire to `--proxy-server=http://airflow-mitmproxy-1:8080`.

### Test cases
- Here, I set addr as `0.0.0.0` and use the `8080` port. I tried to set `http://airflow-mitmproxy-1` but I got an error here.
- I put 2 cases below.

#### run Python in `airflow-webserver-1`
- In this case, I ran the code in `airflow-webserver-1`, but I just got nothing back.
  - code
```python=
import logging
from seleniumwire import webdriver
import time

# 配置日誌
logging.basicConfig(level=logging.DEBUG)

sw_options = {
    'auto_config': False,  # Ensure this is set to False
    'addr': '0.0.0.0',  # The address the proxy will listen on
    'port': 8080,
}


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://airflow-mitmproxy-1:8080')  # Specify your Kubernetes service-name here
chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Remote(
    command_executor="http://localhost:4444",
    options=chrome_options,
    seleniumwire_options=sw_options
)

driver.get('https://www.example.com')

time.sleep(5)

for request in driver.requests:
    print(request.url, request.response.status_code)
```
  - log
```
INFO:seleniumwire.storage:Using default request storage
INFO:seleniumwire.backend:Created proxy listening on :::8080
DEBUG:selenium.webdriver.remote.remote_connection:POST http://localhost:4444/session {"capabilities": {"firstMatch": [{}], "alwaysMatch": {"browserName": "chrome", "pageLoadStrategy": "normal", "goog:chromeOptions": {"extensions": [], "args": ["--proxy-server=http://airflow-mitmproxy-1:8080", "--ignore-certificate-errors"]}}}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): localhost:4444
DEBUG:urllib3.connectionpool:http://localhost:4444 "POST /session HTTP/1.1" 200 1504
DEBUG:selenium.webdriver.remote.remote_connection:Remote response: status=200 | data={
  "value": {
    "sessionId": "6d88c9d00a212d111d58fbd1eecb6168",
    "capabilities": {
      "acceptInsecureCerts": false,
      "browserName": "chrome",
      "browserVersion": "114.0.5735.106",
      "chrome": {
        "chromedriverVersion": "114.0.5735.106 (5148e93c94b4990618801dd6918f26936be770f9-refs\u002fbranch-heads\u002f5735_90@{#9})",
        "userDataDir": "\u002ftmp\u002f.org.chromium.Chromium.ZYyIRv"
      },
      "goog:chromeOptions": {
        "debuggerAddress": "localhost:33163"
      },
      "networkConnectionEnabled": false,
      "pageLoadStrategy": "normal",
      "platformName": "linux",
      "proxy": {
      },
      "se:bidiEnabled": false,
      "se:cdp": "ws:\u002f\u002f172.25.0.7:4444\u002fsession\u002f6d88c9d00a212d111d58fbd1eecb6168\u002fse\u002fcdp",
      "se:cdpVersion": "114.0.5735.106",
      "se:vnc": "ws:\u002f\u002f172.25.0.7:4444\u002fsession\u002f6d88c9d00a212d111d58fbd1eecb6168\u002fse\u002fvnc",
      "se:vncEnabled": true,
      "se:vncLocalAddress": "ws:\u002f\u002f172.25.0.7:7900",
      "setWindowRect": true,
      "strictFileInteractability": false,
      "timeouts": {
        "implicit": 0,
        "pageLoad": 300000,
        "script": 30000
      },
      "unhandledPromptBehavior": "dismiss and notify",
      "webauthn:extension:credBlob": true,
      "webauthn:extension:largeBlob": true,
      "webauthn:extension:minPinLength": true,
      "webauthn:extension:prf": true,
      "webauthn:virtualAuthenticators": true
    }
  }
} | headers=HTTPHeaderDict({'content-length': '1504', 'Cache-Control': 'no-cache', 'Content-Type': 'application/json; charset=utf-8'})
DEBUG:selenium.webdriver.remote.remote_connection:Finished Request
DEBUG:selenium.webdriver.remote.remote_connection:POST http://localhost:4444/session/6d88c9d00a212d111d58fbd1eecb6168/url {"url": "https://www.example.com"}
DEBUG:urllib3.connectionpool:http://localhost:4444 "POST /session/6d88c9d00a212d111d58fbd1eecb6168/url HTTP/1.1" 200 14
DEBUG:selenium.webdriver.remote.remote_connection:Remote response: status=200 | data={"value":null} | headers=HTTPHeaderDict({'content-length': '14', 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-cache'})
DEBUG:selenium.webdriver.remote.remote_connection:Finished Request
```

#### Airflow container run selenium-wire in selenium grid
- Because here is just a demo for my Airflow environment, so I'm not sure the code in here can run normally.
- The Airflow task code will be [fetch_twitter.py](/docker/airflow/dags/fetch_twitter.py), and it will use [module.py](/src/myflow/tasks/twitter/module.py)
  - In [module.py](/src/myflow/tasks/twitter/module.py), as you can see the setting looks like the previous case I set `mitmproxy` as proxy server.

## Resource
[Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)