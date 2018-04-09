import requests
from bs4 import BeautifulSoup

PROXY_POOL_URL = 'http://localhost:5000/get'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            proxy = BeautifulSoup(response.text, "lxml").get_text()
            return proxy
    except ConnectionError:
        return None

