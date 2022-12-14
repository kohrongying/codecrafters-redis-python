import time
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
        self.assertEqual(store.store.get("key").expire_at, None)

    def test_set_overwrite(self):
        store = RedisStore()
        store.set("key", "value")
        response = store.set("key", "newvalue")
        self.assertEqual(response, "value")

    def test_set_with_pv_should_set_expiry_in_unix(self):
        store = RedisStore()
        store.set_with_expiry("key", "value", expiry_in_sec=100)
        self.assertNotEqual(store.store.get("key").expire_at, None)

    def test_get_check_expiry(self):
        store = RedisStore()
        store.set_with_expiry("key", "value", expiry_in_sec=1)
        time.sleep(2)
        stored_value = store.get("key")
        self.assertEqual(stored_value, None)
