
class RedisStore:
    def __init__(self) -> None:
        self.store = {}

    def get(self, key: str):
        return self.store.get(key, None)

    def set(self, key: str, value: any) -> str:
        return_message = "OK" if key not in self.store else self.store.get(key)
        self.store[key] = value
        return return_message
