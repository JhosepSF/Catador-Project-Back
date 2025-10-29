# inference/middleware.py
import json, time, logging
from typing import Optional

logger = logging.getLogger("api")

class APILoggingMiddleware:
    """
    Loggea método, ruta, status y el cuerpo JSON (si existe).
    Solo para debugging; no usar en producción con datos sensibles.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _safe_json(self, body: bytes) -> Optional[dict]:
        if not body:
            return None
        try:
            return json.loads(body.decode("utf-8"))
        except Exception:
            return None

    def __call__(self, request):
        start = time.monotonic()
        method = request.method
        path = request.get_full_path()
        content_type = request.META.get("CONTENT_TYPE", "")

        # Captura cuerpo (no consume el stream; request.body está cacheado por Django)
        raw_body = request.body or b""
        json_body = self._safe_json(raw_body) if "application/json" in content_type else None

        logger.info("➡️ %s %s CT=%s", method, path, content_type)
        if json_body is not None:
            logger.info("📦 JSON in: %s", json_body)
        elif raw_body:
            # limita a 2KB para evitar logs enormes
            preview = raw_body[:2048].decode("utf-8", errors="replace")
            logger.info("📦 Body (raw, preview): %s", preview)

        response = self.get_response(request)

        elapsed = (time.monotonic() - start) * 1000
        logger.info("⬅️ %s %s → %s (%.1f ms, len=%s)",
                    method, path, getattr(response, "status_code", "?"),
                    elapsed, len(getattr(response, "content", b"")))

        return response
