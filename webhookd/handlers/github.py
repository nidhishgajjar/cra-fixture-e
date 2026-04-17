import json
import logging
from webhookd.signing import verify
from webhookd.idempotency import seen, mark


log = logging.getLogger(__name__)


def handle(body, headers):
    payload = json.loads(body)
    delivery = headers.get("X-GitHub-Delivery", "")

    if seen(delivery):
        log.info("duplicate delivery %s", delivery)
        return {"status": "duplicate"}, 200

    event_name = headers.get("X-GitHub-Event", "")
    if event_name == "ping":
        return {"status": "pong"}, 200

    if not verify("github", body, headers):
        log.warning("invalid signature for delivery %s", delivery)
        return {"error": "invalid signature"}, 401

    log.info("github %s delivery=%s repo=%s", event_name, delivery, payload.get("repository", {}).get("full_name"))
    mark(delivery)
    return {"status": "ok"}, 200
