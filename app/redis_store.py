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

    def set(self, key: str, value: any) -> str:
        return_message = "OK" if key not in self.store else self.store.get(key)
        self.store[key] = value
        return return_message

    def set_with_expiry(self, key, value, expiry_in_sec: int) -> str:
        self.expiry[key] = int(time.time() + expiry_in_sec * 0.001)
        return self.set(key, value)

    def _is_expired(self, key) -> bool:
        return self.expiry.get(key) < time.time()
