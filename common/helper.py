import asyncio
from common.redis import RedisWrapper
from core.config import settings


def run_async(coro):
    """ Method to run async using event loop safely """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        return asyncio.create_task(coro)


def publish_token(token, channel):
    """ Method to push the token in list, set TTL and publish to the channel """

    redis_wrapper = RedisWrapper(db=settings.REDIS_MESSAGE_STREAMING_DB)

    redis_wrapper.rpush(f"{channel}:history", token)
    redis_wrapper.expire(f"{channel}:history", 5 * 3600)
    redis_wrapper.publish(channel, token)
