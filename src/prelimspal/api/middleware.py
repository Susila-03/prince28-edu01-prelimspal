"""Gives every HTTP request an ID and logs its completion."""

import logging
import time
import uuid

from prelimspal.logging_setup import request_id_ctx

logger = logging.getLogger("prelimspal.http")


class RequestContextMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))

        request_id = headers.get(b"x-request-id", b"").decode() or uuid.uuid4().hex[:16]

        token = request_id_ctx.set(request_id)
        start = time.perf_counter()
        status_code = 500

        async def send_with_context(message):
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

                response_headers = list(message.get("headers", []))
                response_headers.append((b"x-request-id", request_id.encode()))

                message = {
                    **message,
                    "headers": response_headers,
                }

            await send(message)

        try:
            await self.app(scope, receive, send_with_context)

        except Exception:
            logger.exception("unhandled error")
            raise

        finally:
            logger.info(
                "request finished",
                extra={
                    "method": scope.get("method"),
                    "path": scope.get("path"),
                    "status": status_code,
                    "duration_ms": round((time.perf_counter() - start) * 1000, 1),
                },
            )

            request_id_ctx.reset(token)
