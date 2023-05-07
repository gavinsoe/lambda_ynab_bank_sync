from datetime import datetime
from services.models.ynab_models import Transaction
from services.upbank_service import UpBankService
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
        self.upbank_service = UpBankService(source_config.access_token)

    def _transform_to_transaction(self, t: dict) -> Transaction:
        # extract and transform the date
        date_raw = t.get("attributes", {}).get("createdDate")
        ynab_formatted_date = datetime.strptime(
            date_raw, "%Y-%m-%dT%H:%M:%S%z"
        ).strftime(self.YNAB_DATE_FORMAT)

        # extract the value, and multiply by 10 as YNAB stores it in milliunits
        amount = (
            t.get("attributes", {})
            .get("holdInfo", {})
            .get("amount", {})
            .get("valueInBaseUnits")
            * 10
        )

        return Transaction(
            date=ynab_formatted_date,
            amount=amount,
            payee_name=t.get("attributes", {}).get("description"),
            cleared="uncleared",
        )

    def get_transactions_from_source(self) -> Transaction:
        transactions = self.upbank_service.get_transactions(
            account_id=self.source_config.account_id
        )

        # transform transactions to...
        return [self._transform_to_transaction(t) for t in transactions]
