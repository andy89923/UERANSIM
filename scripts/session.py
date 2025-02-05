import requests
import requests.adapters


def session_for_src_addr(addr: str):
    session = requests.Session()
    for prefix in ["http://", "https://"]:
        adapter = session.get_adapter(prefix)
        adapter.init_poolmanager(
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            source_address=(addr, 0),
        )
        adapter.timeout = 3
    return session
