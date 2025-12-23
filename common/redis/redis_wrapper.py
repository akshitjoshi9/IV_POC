from redis import Redis
import json

from core.config import settings


class RedisWrapper:
    """
        Wrapper for redis

        Use these db values for the following tasks/services:
        db=0 - common
        db=1 - memory
        db=2 - message streaming
    """

    def __init__(self, db=0):
        self.redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=db,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()

    # CRUD
    def setex(self, key, expiry, value):
        """ Set a key with a value and expiration (in seconds) """

        if not isinstance(value, str):
            value = json.dumps(value)
        return self.redis_client.setex(key, expiry, value)

    def get(self, key):
        """ Get a value by key """

        value = self.redis_client.get(key)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def delete(self, key: str):
        """ Delete a key from Redis """
        return self.redis_client.delete(key)

    # Pub/Sub
    def publish(self, channel, message):
        """ Publish message to redis channel """

        if not isinstance(message, str):
            message = json.dumps(message)
        return self.redis_client.publish(channel, message)

    def listen(self):
        """ Yield messages from the pubsub channel """

        return self.pubsub.listen()

    def subscribe(self, *channels):
        """ Subscribe to one or more redis channels """

        self.pubsub.subscribe(*channels)

    def unsubscribe(self, *channels):
        """ Subscribe to one or more redis channels """

        self.pubsub.unsubscribe(*channels)

    def rpush(self, key, message):
        """ Push a message to the end of redis list """

        if not isinstance(message, str):
            message = json.dumps(message)
        return self.redis_client.rpush(key, message)

    def expire(self, key, duration):
        """ Set an expiry on a redis key  """

        return self.redis_client.expire(key, duration)

    def lrange(self, key, start=0, end=-1):
        """ Retrieve range of elements from redis list """

        return self.redis_client.lrange(key, start, end)

    def lrem(self, key, start=0, end=-1):
        """ Remove range of elements from redis list """

        return self.redis_client.lrem(key, start, end)

    def set(self, key, value, expire=None):
        """Set key in Redis. Optionally set expiry in seconds."""
        if not isinstance(value, str):
            value = json.dumps(value)
        if expire:
            return self.redis_client.setex(key, expire, value)
        return self.redis_client.set(key, value)

    def get_json(self, key):
        """Get JSON object from Redis key"""
        value = self.redis_client.get(key)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value