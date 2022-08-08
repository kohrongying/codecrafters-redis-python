import time
from typing import Optional, List


class RedisStore:
    def __init__(self) -> None:
        self.store = {}
        self.expiry = {}

    def get(self, key: str) -> Optional[str]:
        print('in store get')
        print('expiry set', self.expiry.get(key))
        print('now is', time.time())
        if self.expiry.get(key, None) is not None and self._is_expired(key):
            return None
        return self.store.get(key, None)

    def set(self, key: str, value: any, *args) -> str:
        return_message = "OK" if key not in self.store else self.store.get(key)
        self.store[key] = value
        self.expiry[key] = None
        opts: List = args[0]
        if len(opts) > 0:
            if opts[0].upper() == "PX":
                self.expiry[key] = int(time.time() + int(opts[1]) * 0.001)
        return return_message

    def _is_expired(self, key) -> bool:
        return self.expiry.get(key) < time.time()
