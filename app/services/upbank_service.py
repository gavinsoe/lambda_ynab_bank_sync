import json
from typing import List
import requests
from utilities.config import CFG


class UpBankService:
    def __init__(self, access_token):
        self._endpoint = CFG.endpoints.upbank
        self._headers = {"Authorisation": "Brearer {access_token}"}

    def get_transactions(self, account_id, since_date: str = None) -> List[dict]:
        try:
            url = f"{self._endpoint}/accounts/{account_id}/transactions"

            if since_date:
                url += f"?since_date={since_date}"

            response = requests.get(headers=self._headers, url=url)
            response.raise_for_status()
            result = json.loads(response.content.decode("utf-8"))
            
            results = result.get("data", [])
            next_page = result.get("links",{}).get("next", None)
            
            # retrieve more data if paginated
            while next_page:
                response = requests.get(headers=self._headers, url=next_page)
                response.raise_for_status()
                
                result = json.loads(response.content.decode("utf-8"))
                results += result.get("data", [])
                next_page = result.get("links",{}).get("next", None)
            
            return results
        except Exception as e:
            print(f"Something went wrong while fetching the list of transactions. {e}")
            raise e
