from datetime import datetime, timedelta
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class RedisValue:
    value: Optional[str]
    expire_at: Optional[datetime] = None


empty_value = RedisValue(value=None)


class RedisStore:
    def __init__(self) -> None:
        self.store = {}

    def get(self, key: str) -> Optional[str]:
        print('in store get')
        print('now is', time.time())
        if self._is_expired(key):
            return None
        return self.store.get(key, empty_value).value

    def set(self, key: str, value: any) -> str:
        return_message = self.store.get(key).value if self._is_key_present(key) else "OK"
        self.store[key] = RedisValue(value=value)
        return return_message

    def set_with_expiry(self, key, value, expiry_in_sec: float) -> str:
        return_message = self.store.get(key).value if self._is_key_present(key) else "OK"
        expire_at = datetime.now() + timedelta(seconds=expiry_in_sec)
        self.store[key] = RedisValue(value=value, expire_at=expire_at)
        return return_message

    def _is_expired(self, key) -> bool:
        if self._is_key_present(key):
            expire_at = self.store.get(key).expire_at
            if expire_at is not None:
                return expire_at < datetime.now()
        return False

    def _is_key_present(self, key) -> bool:
        return key in self.store
