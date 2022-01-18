# These tests cover the integration of the entire system and do not go into details - that's
# what unit tests are for. As such, typically each method will get a single happy path test and
# a single unhappy path test unless otherwise warranted.

# Tests of the auth user lookup and workspace wrapper code are at the bottom of the file.
import uuid

from testing.shared.common import (
    check_kafka_messages,
    clear_kafka_messages,
    create_sample_assert_result,
    get_samples_assert_error,
    get_samples_assert_result,
    sample_params_to_sample,
)
from testing.shared.test_cases import CASE_01, CASE_02
from testing.shared.test_constants import (
    TOKEN1,
    TOKEN2,
    USER1,
)


def test_get_samples_fail_missing_param(sample_service):
    bad_sample_id = str(uuid.uuid4())
    error = get_samples_assert_error(
        sample_service["url"],
        TOKEN2,
        {"id": bad_sample_id, "version": 1, "as_admin": False},
    )
    assert error["message"] == ("The 'samples' parameter is required")


def test_get_samples_fail_no_samples_provided(sample_service):
    error = get_samples_assert_error(sample_service["url"], TOKEN2, {"samples": []})
    assert error["message"] == ("The 'samples' parameter is required")


def test_create_and_get_samples(sample_service, kafka_host):
    clear_kafka_messages(kafka_host)

    # first sample
    sample1 = create_sample_assert_result(
        sample_service["url"], TOKEN1, CASE_01, {"version": 1}
    )

    # second sample
    sample2 = create_sample_assert_result(
        sample_service["url"], TOKEN1, CASE_02, {"version": 1}
    )

    # get both samples
    get_samples_assert_result(
        sample_service["url"],
        TOKEN1,
        {
            "samples": [
                {"id": sample1["id"], "version": 1},
                {"id": sample2["id"], "version": 1},
            ]
        },
        [
            sample_params_to_sample(
                CASE_01, {"user": USER1, "id": sample1["id"], "version": 1}
            ),
            sample_params_to_sample(
                CASE_02, {"user": USER1, "id": sample2["id"], "version": 1}
            ),
        ],
    )

    check_kafka_messages(
        kafka_host,
        [
            {"event_type": "NEW_SAMPLE", "sample_id": sample1["id"], "sample_ver": 1},
            {"event_type": "NEW_SAMPLE", "sample_id": sample2["id"], "sample_ver": 1},
        ],
    )


def test_get_samples_fail_sample_version_not_found(sample_service, kafka_host):
    # first sample
    sample1 = create_sample_assert_result(
        sample_service["url"], TOKEN1, CASE_01, {"version": 1}
    )

    error = get_samples_assert_error(
        sample_service["url"],
        TOKEN1,
        {
            "samples": [
                {"id": sample1["id"], "version": 2},
            ]
        },
    )
    assert error["message"] == (
        f"Sample service error code 50010 No such sample: {sample1['id']} ver 2"
    )


# TODO: The implementation of get_samples does not actually trigger this error condition.
# The check for ACLs conducted before the actual call to get_samples will throw if there
# is an error attempting to fetch all samples.
# At the same time, this sort of defeats the purpose of the get_samples call, as it does
# an individual sample fetch in any case.

# def test_get_samples_fail_non_existent_sample(sample_service):
#     sample_id = str(uuid.uuid4())
#     error = get_samples_assert_error(
#         sample_service["url"],
#         TOKEN2,
#         {
#             "samples": [
#                 {"id": sample_id, "version": 1},
#             ]
#         },
#     )
#     assert error["message"] == (
#         f"Could not complete search for samples: {str(uuid.uuid4())}"
#     )
