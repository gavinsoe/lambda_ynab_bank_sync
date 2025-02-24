import pytest

from services.upbank_service import UpBankService
from utilities.config import CFG

source_configs = [(sc.name, sc.source) for sc in CFG.sync_configs]


@pytest.mark.parametrize(
    "source_config", [s[1] for s in source_configs], ids=[s[0] for s in source_configs]
)
def test_ping(source_config):
    upbank_service = UpBankService(source_config.access_token)

    response = upbank_service.ping()
    assert response["meta"]["statusEmoji"] == "⚡️"
