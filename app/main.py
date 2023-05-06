from utilities.config import CFG


def sync_factory(source, destination):
    """syncs source to destination"""

def sync():
    for sync_config in CFG.sync_configs:
        sync_factory(sync_config.source, sync_config.destination)
