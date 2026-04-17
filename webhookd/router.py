from webhookd.handlers import stripe as stripe_handler
from webhookd.handlers import github as github_handler


HANDLERS = {
    "stripe": stripe_handler.handle,
    "github": github_handler.handle,
}


def dispatch(provider, body, headers):
    handler = HANDLERS.get(provider)
    if handler is None:
        return {"error": "unknown provider"}, 404
    return handler(body, headers)
