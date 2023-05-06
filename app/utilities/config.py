import json
from typing import List, Literal, Union
from uuid import UUID
from pydantic import BaseModel
from utilities.aws_ssm import get_parameter
from utilities.environment import Environment


class SourceAmex(BaseModel):
    source_name: Literal['amex']

class SourceUpBank(BaseModel):
    source_name: Literal['up']
    access_token: str

class DestinationYnab(BaseModel):
    access_token: str    
    budget_id: UUID
    account_id: UUID

class SyncConfig(BaseModel):
    source: Union[SourceAmex, SourceUpBank]
    destination: DestinationYnab

class ConfigModel(BaseModel):
    sync_configs: List[SyncConfig]


CFG = ConfigModel()

def populate_ssm_keys(raw_dict: dict) -> dict:
    try:
        for d_key in raw_dict.keys():
            d_value = raw_dict[d_key]
            if isinstance(d_value, dict):
                if "ssm_key" in d_value and len(d_value.keys()) == 1:
                    result = get_parameter(d_value["ssm_key"], "ap-southeast-2")

                    raw_dict[d_key] = result
                else:
                    raw_dict[d_key] = populate_ssm_keys(d_value)

        return raw_dict

    except Exception as ex:
        raise ex

with open(Environment.config_path()) as config:
    config_dict = json.loads(config.read())
    config_dict = populate_ssm_keys(config_dict)
    CFG = ConfigModel(**config_dict)
