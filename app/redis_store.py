import time
from typing import Optional


class RedisStore:
    def __init__(self) -> None:
        self.store = {}
        self.expiry = {}

    def get(self, key: str) -> Optional[str]:
        if self.expiry.get(key, None) is not None and self._is_expired(key):
            return None
        print('expiry set', self.expiry.get(key))
        print('now is', time.time())
        return self.store.get(key, None)

    def set(self, key: str, value: any, *oargs) -> str:
        return_message = "OK" if key not in self.store else self.store.get(key)
        self.store[key] = value
        self.expiry[key] = None
        print('set args', oargs)
        if len(oargs) > 0:
            if oargs[0].upper() == "PX":
                self.expiry[key] = int(time.time() + int(oargs[1]) * 0.001)
        return return_message

    def _is_expired(self, key) -> bool:
        return self.expiry.get(key) < time.time()
