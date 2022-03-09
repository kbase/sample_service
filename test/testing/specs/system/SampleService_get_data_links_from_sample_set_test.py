# These tests cover the integration of the entire system and do not go into details - that's
# what unit tests are for. As such, typically each method will get a single happy path test and
# a single unhappy path test unless otherwise warranted.
import uuid
import time

from testing.shared.common import (
    create_duplicate_samples,
    create_generic_sample,
    create_link,
    get_current_epochmillis,
    get_links_from_sample_set_assert_error,
    rpc_call_result,
)
from testing.shared.test_cases import CASE_01
from testing.shared.test_constants import (
    TOKEN1,
    TOKEN3,
    TOKEN4,
    USER1,
)


def test_get_links_from_sample_set(sample_service):
    """
    test timing for fetching batch of links from list of samples
    """

    #
    # requirements:
    # a user (USER1, TOKEN1)
    # workspace: a ws object owned by USER1 (8/1/1)
    #
    sample_count = 100

    sample_ids = create_duplicate_samples(
        sample_service["url"], TOKEN1, CASE_01["sample"], sample_count
    )

    start = time.perf_counter()
    link_ids = [
        create_link(
            sample_service["url"],
            TOKEN1,
            {
                "id": sample_id,
                "version": 1,
                "node": "root",
                "upa": "8/1/1",
                "dataid": f"data_id_${i + 1}",
            },
            USER1,
        )
        for i, sample_id in enumerate(sample_ids)
    ]
    singular_elapsed = time.perf_counter() - start
    assert len(link_ids) == 100
    print(f"singular: {singular_elapsed}")

    start = time.perf_counter()
    effective_time = get_current_epochmillis()
    response = rpc_call_result(
        sample_service["url"],
        TOKEN1,
        "get_data_links_from_sample_set",
        [
            {
                "sample_ids": [
                    {"id": sample_id, "version": 1} for sample_id in sample_ids
                ],
                "as_admin": False,
                "effective_time": effective_time,
            }
        ],
        None,
    )
    assert len(response["links"]) == 100
    assert response["effective_time"] == effective_time
    plural_elapsed = time.perf_counter() - start
    print(f"plural: {plural_elapsed}")

    # The plural form of get_data_links should take less time
    # than the singular.
    assert plural_elapsed < singular_elapsed

    # It should take no more than 20ms per sample link.
    # TODO: I don't know where this perf metric comes from;
    # it was originally actually 10ms, but the test allowed it
    # to take twice as long, so might as well just state 20ms.
    # and will be sensitive to where the tests are run.
    # I think it should be more like 1ms, but in actuality the
    # links should be fetched by a single query, and will probably
    # be paged, etc., so per-link metrics won't be as meaningful other
    # than in that context.
    # DISABLED: is not deterministic enough, can fail randomly if the
    # system is under load.
    # expected_maximum_time_per_link = 20  # ms
    # expected_maximum_elapsed_time = (
    #     sample_count * expected_maximum_time_per_link
    # ) / 1000
    # assert plural_elapsed < expected_maximum_elapsed_time


def test_get_links_from_sample_set_fail(sample_service):
    """
    Various error conditions
    """
    sample_id = create_generic_sample(sample_service["url"], TOKEN3)

    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN3,
        {},
        'Missing "sample_ids" field - Must provide a list of valid sample ids.',
    )
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN3,
        {"sample_ids": [{"id": sample_id}]},
        "Malformed sample accessor - each sample must provide both an id and a version.",
    )
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN3,
        {"sample_ids": [{"id": sample_id, "version": 1}]},
        'Missing "effective_time" parameter.',
    )
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN3,
        {"sample_ids": [{"id": sample_id, "version": 1}], "effective_time": "foo"},
        "Sample service error code 30001 Illegal input parameter: key 'effective_time' "
        + "value of 'foo' is not a valid epoch millisecond timestamp",
    )
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN4,
        {
            "sample_ids": [{"id": sample_id, "version": 1}],
            "effective_time": get_current_epochmillis() - 500,
        },
        f"Sample service error code 20000 Unauthorized: User user4 cannot read sample {sample_id}",
    )
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        None,
        {
            "sample_ids": [{"id": sample_id, "version": 1}],
            "effective_time": get_current_epochmillis() - 500,
        },
        (
            "Sample service error code 20000 Unauthorized:"
            f" Anonymous users cannot read sample {sample_id}"
        ),
    )
    bad_id = uuid.uuid4()
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN3,
        {
            "sample_ids": [{"id": str(bad_id), "version": 1}],
            "effective_time": get_current_epochmillis() - 500,
        },
        (
            f"Sample service error code 50010 No such sample: "
            f"Could not complete search for samples: ['{bad_id}']"
        ),
    )

    # admin tests
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        TOKEN4,
        {
            "sample_ids": [{"id": sample_id, "version": 1}],
            "effective_time": get_current_epochmillis() - 500,
            "as_admin": 1,
        },
        "Sample service error code 20000 Unauthorized: User user4 does not have the "
        + "necessary administration privileges to run method get_data_links_from_sample",
    )
    get_links_from_sample_set_assert_error(
        sample_service["url"],
        None,
        {
            "sample_ids": [{"id": sample_id, "version": 1}],
            "effective_time": get_current_epochmillis() - 500,
            "as_admin": 1,
        },
        "Sample service error code 20000 Unauthorized: Anonymous users "
        + "may not act as service administrators.",
    )
