import json
from typing import List

import requests

from services.models.ynab_models import Account, Budget, Transaction
from utilities.config import CFG


class YnabService:
    def __init__(self, access_token):
        self._endpoint = CFG.endpoints.ynab
        self._headers = {"Authorization": f"Bearer {access_token}"}
        
    def list_budgets(self) -> List[Budget]:
        try:
            response = requests.get(
                headers=self._headers,
                url=f"{self._endpoint}/budgets"
            )
            
            response.raise_for_status()
            
            result = json.loads(response.content.decode("utf-8"))
            
            return [Budget(**b) for b in result.get("data",{}).get("budgets",[])]
        except Exception as e:
            print(f"Something went wrong while fetching the list of budgets. {e}")
            raise e
        
    def get_accounts(self, budget_id) -> List[Account]:
        try:
            response = requests.get(
                headers=self._headers,
                url=f"{self._endpoint}/budgets/{budget_id}/accounts"
            )
            
            response.raise_for_status()
            
            result = json.loads(response.content.decode("utf-8"))
            
            return [Account(**b) for b in result.get("data",{}).get("accounts",[])]
        except Exception as e:
            print(f"Something went wrong while fetching the list of accounts. {e}")
            raise e
        
    def get_transactions(self, budget_id, account_id, since_date:str = None) -> List[Transaction]:
        try:
            url = f"{self._endpoint}/budgets/{budget_id}/accounts/{account_id}/transactions"
            
            if since_date:
                url += f"?since_date={since_date}"
            
            response = requests.get(
                headers=self._headers,
                url=url
            )
            
            response.raise_for_status()
            
            result = json.loads(response.content.decode("utf-8"))
            
            return [Transaction(**b) for b in result.get("data",{}).get("transactions",[])]
        except Exception as e:
            print(f"Something went wrong while fetching the list of transactions. {e}")
            raise e

    def create_transactions(self, budget_id, account_id, transactions: List[Transaction]) -> List[Transaction]:
        try:
            url = f"{self._endpoint}/budgets/{budget_id}/transactions"
                        
            transactions_list = []
            for t in transactions:
                t_dict = t.dict()
                # remove id
                t_dict.pop("id")
                t_dict["account_id"] = account_id
                
                transactions_list += [t_dict]
            
            response = requests.post(
                headers=self._headers,
                url=url,
                json={
                    "transactions": transactions_list
                }
            )
            
            response.raise_for_status()
            
            result = json.loads(response.content.decode("utf-8"))
            
            return [Transaction(**b) for b in result.get("data",{}).get("transactions",[])]
        except Exception as e:
            print(f"Something went wrong while importing transactions to ynab. {e}")
            raise e