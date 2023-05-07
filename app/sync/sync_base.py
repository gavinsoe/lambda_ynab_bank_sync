from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List
from services.models.ynab_models import Transaction
from services.ynab_service import YnabService
from utilities.config import DestinationConfig


class SyncBase(ABC):
    YNAB_DATE_FORMAT = "%Y-%m-%d"
    def __init__(self, destination_config: DestinationConfig, duration_in_days: int):
        self.ynab_service = YnabService(access_token=destination_config.access_token)
        self.destination_config = destination_config
        self.duration_in_days = duration_in_days

    @abstractmethod
    def get_transactions_from_source(self) -> Transaction:
        """This method should retrieve transactions and map it to the ynab format"""
        # this should be defined by the derived classes
        raise NotImplementedError

    def get_transactions_from_ynab(self):
        since_date = (datetime.now() - timedelta(days=self.duration_in_days)).strftime(
            self.YNAB_DATE_FORMAT
        )
        transactions = self.ynab_service.get_transactions(
            self.destination_config.budget_id,
            self.destination_config.account_id,
            since_date,
        )

        return transactions

    def upload_transactions(self, transactions: List[Transaction]):
        self.ynab_service.create_transactions(
            budget_id=self.destination_config.budget_id,
            account_id=self.destination_config.account_id,
            transactions=transactions,
        )

    def run(self):
        incoming_transactions = self.get_transactions_from_source()

        existing_transactions = self.get_transactions_from_ynab()

        filter(
            lambda x: x not in existing_transactions,
            incoming_transactions,
        )

        self.upload_transactions(incoming_transactions)
