from unittest import TestCase

from app.redis_store import RedisStore


class TestRedisStore(TestCase):
    def test_get(self):
        store = RedisStore()
        store.set("key", "value")
        stored_value = store.get("key")
        self.assertEqual(stored_value, "value")

    def test_set(self):
        store = RedisStore()
        response = store.set("key", "value")
        self.assertEqual(response, "OK")

    def test_set_overwrite(self):
        store = RedisStore()
        store.set("key", "value")
        response = store.set("key", "newvalue")
        self.assertEqual(response, "value")