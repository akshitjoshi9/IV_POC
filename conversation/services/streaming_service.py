import json
import time
from datetime import datetime, timezone
from fastapi.responses import StreamingResponse
import pytz
from common.redis import RedisWrapper
from core.config import settings
from loguru import logger


class StreamMessageService:
    def __init__(self, message_id, user_timezone: str = "UTC"):
        self.channel = str(message_id)
        self.redis_wrapper = RedisWrapper(db=settings.REDIS_MESSAGE_STREAMING_DB)
        self.pubsub = self.redis_wrapper.pubsub
        self.last_heartbeat = time.time()

        try:
            self.tz = pytz.timezone(user_timezone)
        except (pytz.UnknownTimeZoneError, AttributeError):
            self.tz = pytz.UTC

    def subscribe(self):
        self.pubsub.subscribe(self.channel)
        logger.info(f"Subscribed to channel {self.channel}")

    def unsubscribe(self):
        self.pubsub.unsubscribe(self.channel)
        self.pubsub.close()
        logger.info(f"Unsubscribed from channel {self.channel}")

    def _get_local_time(self) -> str:
        """Return current time in user timezone as ISO string"""
        utc_now = datetime.now(timezone.utc)
        local_time = utc_now.astimezone(self.tz).isoformat()
        return local_time

    def _yield_history(self):

        # Inject timestamp event BEFORE history streaming
        created_at = self._get_local_time()
        yield f"event: timestamp\ndata: {created_at}\n\n"

        for msg in self.redis_wrapper.lrange(f"{self.channel}:history", 0, -1):
            if msg == "__done__":
                sources = self.redis_wrapper.get_json(f"{self.channel}:sources") or []
                yield f"event: sources\ndata: {json.dumps(sources)}\n\n"
                yield "event: done\ndata: [DONE]\n\n"
                return
            yield f"event: message\ndata: {msg}\n\n"

    def _event_stream(self):
        yield from self._yield_history()

        try:
            while True:
                message = self.pubsub.get_message(timeout=1)
                now = time.time()

                if message and message["type"] == "message":
                    data = message["data"]
                    if data == "__done__":
                        sources = self.redis_wrapper.get_json(f"{self.channel}:sources") or []
                        yield f"event: sources\ndata: {json.dumps(sources)}\n\n"
                        yield "event: done\ndata: [DONE]\n\n"
                        break
                    yield f"event: message\ndata: {data}\n\n"

                # Heartbeat every 30s with user timezone
                elif now - self.last_heartbeat >= 30:
                    local_time = self._get_local_time()
                    yield f"event: heartbeat\ndata: {local_time}\n\n"
                    self.last_heartbeat = now

        finally:
            self.unsubscribe()

    def get_streaming_response(self) -> StreamingResponse:
        self.subscribe()
        return StreamingResponse(self._event_stream(), media_type="text/event-stream")
