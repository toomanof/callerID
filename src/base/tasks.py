from src.base.constants import URLS_REGISTRY
from src.celeryconf import app

@app.task
def update_registry():
    from src.base.services.dispatchers import RegistryDispatcher
    dispatcher = RegistryDispatcher()
    for url_registry in URLS_REGISTRY:
        dispatcher.execute(url=url_registry)
