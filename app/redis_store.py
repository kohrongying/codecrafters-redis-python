import time


class RedisStore:
    def __init__(self) -> None:
        self.store = {}
        self.expiry = {}

    def get(self, key: str):
        return self.store.get(key, None)

    def set(self, key: str, value: any, *args) -> str:
        return_message = "OK" if key not in self.store else self.store.get(key)
        self.store[key] = value
        self.expiry[key] = None
        if len(args) > 0:
            print(args)
            if args[0] == "PX":
                self.expiry[key] = int(time.time() * 1000 + int(args[1]))
        return return_message
