from services.models.ynab_models import Transaction
from sync.sync_base import SyncBase
from utilities.config import DestinationConfig, SourceUpBank


class SyncUpbank(SyncBase):
    def __init__(
        self,
        source_config: SourceUpBank,
        destination_config: DestinationConfig,
        duration_in_days: int,
    ):
        super().__init__(destination_config, duration_in_days)
        self.source_config = source_config

    
    def get_transactions_from_source(self) -> Transaction:
        """query upbank to retrieve transactions"""