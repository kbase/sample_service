# These tests cover the integration of the entire system and do not go into details - that's
# what unit tests are for. As such, typically each method will get a single happy path test and
# a single unhappy path test unless otherwise warranted.

# Tests of the auth user lookup and workspace wrapper code are at the bottom of the file.

import copy

from testing.shared.common import (
    create_link,
    create_sample_assert_result,
    rpc_call_result,
)
from testing.shared.test_cases import CASE_01

#
# Simple sample creation cases. Does not assume anything else --
# see later tests for more complex scenarios.
#
from testing.shared.test_constants import (
    TOKEN3,
    USER3,
)
from testing.shared.test_utils import assert_ms_epoch_close_to_now


#
# Create two samples, each with a single
#
#
def _create_sample_and_links_for_propagate_links(
    sample_service, token, user, case, upa1, upa2
):
    # create samples
    sample = create_sample_assert_result(
        sample_service["url"], token, case, {"version": 1}
    )

    # ver 2
    params = copy.deepcopy(case)
    params["sample"]["id"] = sample["id"]
    create_sample_assert_result(sample_service["url"], token, params, {"version": 2})

    # create links
    link_id_1 = create_link(
        sample_service["url"],
        token,
        {
            "id": sample["id"],
            "version": 1,
            "node": "root",
            "upa": upa1,
            "dataid": "column1",
        },
        user,
        debug=True,
    )
    link_id_2 = create_link(
        sample_service["url"],
        token,
        {
            "id": sample["id"],
            "version": 1,
            "node": "root",
            "upa": upa2,
            "dataid": "column2",
        },
        user,
    )

    return sample["id"], link_id_1, link_id_2


def _check_data_links(links, expected_links):
    assert len(links) == len(expected_links)
    for link in links:
        assert_ms_epoch_close_to_now(link["created"])
        del link["created"]

    for link in expected_links:
        assert link in links


def _check_sample_data_links(url, sample_id, version, expected_links, token):
    params = {"id": sample_id, "version": version}
    result = rpc_call_result(url, token, "get_data_links_from_sample", [params])

    links = result["links"]

    _check_data_links(links, expected_links)


def test_create_and_propagate_data_links(sample_service):
    upa1 = "3/1/1"
    upa2 = "3/2/1"

    sid, lid1, lid2 = _create_sample_and_links_for_propagate_links(
        sample_service, TOKEN3, USER3, CASE_01, upa1, upa2
    )

    # check initial links for both version
    expected_links = [
        {
            "linkid": lid1,
            "id": sid,
            "version": 1,
            "node": CASE_01["sample"]["node_tree"][0]["id"],
            "upa": upa1,
            "dataid": "column1",
            "createdby": USER3,
            "expiredby": None,
            "expired": None,
        },
        {
            "linkid": lid2,
            "id": sid,
            "version": 1,
            "node": CASE_01["sample"]["node_tree"][0]["id"],
            "upa": upa2,
            "dataid": "column2",
            "createdby": USER3,
            "expiredby": None,
            "expired": None,
        },
    ]
    _check_sample_data_links(sample_service["url"], sid, 1, expected_links, TOKEN3)
    _check_sample_data_links(sample_service["url"], sid, 2, [], TOKEN3)

    # # propagate data links from sample version 1 to version 2
    result = rpc_call_result(
        sample_service["url"],
        TOKEN3,
        "propagate_data_links",
        [{"id": sid, "version": 2, "previous_version": 1}],
        debug=True,
    )

    links = result["links"]

    new_link_ids = [i["linkid"] for i in links]
    expected_new_links = copy.deepcopy(expected_links)

    # propagated links should have new link id, dataid and version
    for idx, expected_link in enumerate(expected_new_links):
        expected_link["linkid"] = new_link_ids[idx]
        expected_link["dataid"] = expected_link["dataid"] + "_2"
        expected_link["version"] = 2

    _check_data_links(links, expected_new_links)

    # # check links again for sample version 1 and 2
    _check_sample_data_links(sample_service["url"], sid, 1, expected_links, TOKEN3)
    _check_sample_data_links(sample_service["url"], sid, 2, expected_new_links, TOKEN3)


def test_create_and_propagate_data_links_type_specific(sample_service):
    upa1 = "3/1/1"
    upa2 = "3/3/1"

    sid, lid1, lid2 = _create_sample_and_links_for_propagate_links(
        sample_service, TOKEN3, USER3, CASE_01, upa1, upa2
    )

    # check initial links for both version
    expected_links = [
        {
            "linkid": lid1,
            "id": sid,
            "version": 1,
            "node": CASE_01["sample"]["node_tree"][0]["id"],
            "upa": upa1,
            "dataid": "column1",
            "createdby": USER3,
            "expiredby": None,
            "expired": None,
        },
        {
            "linkid": lid2,
            "id": sid,
            "version": 1,
            "node": CASE_01["sample"]["node_tree"][0]["id"],
            "upa": upa2,
            "dataid": "column2",
            "createdby": USER3,
            "expiredby": None,
            "expired": None,
        },
    ]
    _check_sample_data_links(sample_service["url"], sid, 1, expected_links, TOKEN3)
    _check_sample_data_links(sample_service["url"], sid, 2, [], TOKEN3)

    # # propagate data links from sample version 1 to version 2
    result = rpc_call_result(
        sample_service["url"],
        TOKEN3,
        "propagate_data_links",
        [
            {
                "id": sid,
                "version": 2,
                "previous_version": 1,
                "ignore_types": ["Trivial.Object2"],
            }
        ],
        debug=True,
    )

    links = result["links"]

    new_link_ids = [i["linkid"] for i in links]
    expected_new_links = copy.deepcopy(expected_links)
    expected_new_links.pop()

    # propagated links should have new link id, dataid and version
    for idx, expected_link in enumerate(expected_new_links):
        expected_link["linkid"] = new_link_ids[idx]
        expected_link["dataid"] = expected_link["dataid"] + "_2"
        expected_link["version"] = 2

    _check_data_links(links, expected_new_links)

    # # check links again for sample version 1 and 2
    _check_sample_data_links(sample_service["url"], sid, 1, expected_links, TOKEN3)
    _check_sample_data_links(sample_service["url"], sid, 2, expected_new_links, TOKEN3)
