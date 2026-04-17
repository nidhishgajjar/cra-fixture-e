import json, sys, time

def event(provider, event_type, **fields):
    record = {"ts": time.time(), "provider": provider, "event": event_type, **fields}
    sys.stdout.write(json.dumps(record) + "\n")
    sys.stdout.flush()
