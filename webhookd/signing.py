import hmac, hashlib, os

_SECRETS = {
    "stripe": os.environ.get("STRIPE_WEBHOOK_SECRET", ""),
    "github": os.environ.get("GITHUB_WEBHOOK_SECRET", ""),
    "slack":  os.environ.get("SLACK_WEBHOOK_SECRET", ""),
}


def verify(provider, body, headers):
    secret = _SECRETS.get(provider)
    if not secret:
        return False
    sig = headers.get("X-Signature", "")
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)
