from sync.sync_upbank import SyncUpbank
from utilities.config import SourceUpBank


class SyncFactory:
    @staticmethod
    def get_sync_class(source_config, destination_config, duration_in_days=1):
        source_config_type = type(source_config)
        if source_config_type is SourceUpBank:
            return SyncUpbank(
                source_config=source_config,
                destination_config=destination_config,
                duration_in_days=duration_in_days,
            )
