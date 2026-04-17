_seen = set()

def seen(request_id):
    return request_id in _seen

def mark(request_id):
    _seen.add(request_id)
