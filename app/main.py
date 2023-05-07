from sync.sync_factory import SyncFactory
from utilities.config import CFG


def sync():
    for sync_config in CFG.sync_configs:
        sync_class = SyncFactory.get_sync_class(
            source_config=sync_config.source,
            destination_config=sync_config.destination,
            duration_in_days=2,
        )
        sync_class.run()

if __name__ == "__main__":
    sync()