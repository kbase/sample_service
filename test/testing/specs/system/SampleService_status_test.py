# These tests cover the integration of the entire system and do not go into details - that's
# what unit tests are for. As such, typically each method will get a single happy path test and
# a single unhappy path test unless otherwise warranted.

from testing.shared.common import (
    VER,
    rpc_call_result,
)
from testing.shared.test_utils import assert_ms_epoch_close_to_now


def test_status(sample_service):
    status = rpc_call_result(sample_service["url"], None, "status", [])

    assert_ms_epoch_close_to_now(status["servertime"])
    assert status["state"] == "OK"
    assert status["message"] == ""
    assert status["version"] == VER
    # ignore git url and hash, can change
