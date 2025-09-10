import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_session = None

def get_session():
    global _session
    if _session is None:
        s = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504))
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        _session = s
    return _session