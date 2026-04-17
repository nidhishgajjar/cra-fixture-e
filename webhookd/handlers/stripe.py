import json
from webhookd.signing import verify
from webhookd.idempotency import seen, mark
from webhookd.log import event


def handle(body, headers):
    if not verify("stripe", body, headers):
        event("stripe", "invalid_signature")
        return {"error": "invalid signature"}, 401
    payload = json.loads(body)
    request_id = payload.get("id")
    if seen(request_id):
        event("stripe", "duplicate", request_id=request_id)
        return {"status": "duplicate"}, 200
    # ... process the payload (no-op in this fixture) ...
    mark(request_id)
    event("stripe", "processed", request_id=request_id)
    return {"status": "ok"}, 200
