from datetime import datetime, timedelta, timezone
from services.models.ynab_models import Transaction
from services.upbank_service import UpBankService
from sync.sync_base import SyncBase
from utilities.config import DestinationConfig, SourceUpBank


class SyncUpbank(SyncBase):
    UPBANK_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

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
        attributes = t.get("attributes", {})
        # extract and transform the date
        date_raw = attributes.get("createdAt")
        ynab_formatted_date = datetime.strptime(
            date_raw, self.UPBANK_DATE_FORMAT
        ).strftime(self.YNAB_DATE_FORMAT)

        # extract the value, and multiply by 10 as YNAB stores it in milliunits
        amount = (
            attributes
            .get("amount", {})
            .get("valueInBaseUnits")
            * 10
        )

        transactions = []
        transactions.append(Transaction(
            date=ynab_formatted_date,
            amount=amount,
            payee_name=attributes.get("description"),
            cleared="cleared" if t.get("status") == "SETTLED" else "uncleared",
        ))
        
        # check for round ups
        if self.source_config.round_up_payee_id:
            round_up = attributes.get("roundUp")
            if round_up is not None:
                round_up_amount = round_up.get('amount').get("valueInBaseUnits") * 10
                transactions.append(Transaction(
                    date=ynab_formatted_date,
                    amount=round_up_amount,                
                    payee_id=self.source_config.round_up_payee_id,
                    cleared="cleared"
                ))
            
        return transactions

    def get_transactions_from_source(self) -> Transaction:
        since_date = (
            datetime.now(timezone.utc) - timedelta(days=self.duration_in_days)
        ).strftime(self.UPBANK_DATE_FORMAT)

        # upbank date format is slightly different from what is usually supported, add 
        # colon to timezone information.  HHMM -> HH:MM
        since_date = since_date[:-2] + ":" + since_date[-2:]

        transactions = self.upbank_service.get_transactions(
            account_id=self.source_config.account_id, since=since_date
        )

        # transform transactions to...
        return sum([self._transform_to_transaction(t) for t in transactions], [])
