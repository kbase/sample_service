SERVICE_CAPS = SampleService
SPEC_FILE = SampleService.spec
LIB_DIR = lib
SCRIPTS_DIR = scripts
TEST_DIR = test
TEST_CONFIG_FILE = test.cfg
LBIN_DIR = bin
WORK_DIR = /kb/module/work/tmp
# see https://stackoverflow.com/a/23324703/643675
MAKEFILE_DIR:=$(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))

# Override TEST_SPEC when running make test-sdkless to run different tests
TEST_SPEC := $(TEST_DIR)  

UNIT_TEST_SPEC ?= $(TEST_DIR)/testing/specs/unit
INTEGRATION_TEST_SPEC ?= $(TEST_DIR)/testing/specs/integration
SYSTEM_TEST_SPEC ?= $(TEST_DIR)/testing/specs/system

PYPATH=$(MAKEFILE_DIR)/$(LIB_DIR):$(MAKEFILE_DIR)/$(TEST_DIR)
TEST_PYPATH=$(MAKEFILE_DIR)/$(LIB_DIR):$(MAKEFILE_DIR)/$(TEST_DIR)


TSTFL=$(MAKEFILE_DIR)/$(TEST_DIR)/$(TEST_CONFIG_FILE)

INTEGRATION_TEST_CONFIG=$(MAKEFILE_DIR)/$(TEST_DIR)/testing/specs/integration/$(TEST_CONFIG_FILE)
SYSTEM_TEST_CONFIG=$(MAKEFILE_DIR)/$(TEST_DIR)/testing/specs/system/$(TEST_CONFIG_FILE)
UNIT_TEST_CONFIG=$(MAKEFILE_DIR)/$(TEST_DIR)/testing/specs/unit/$(TEST_CONFIG_FILE)

.PHONY: test

default: compile

all: compile build build-startup-script build-executable-script build-test-script

compile:
# Don't compile server automatically, overwrites fixes to error handling
# Temporarily add the next line to the command line args if recompiliation is needed to add
# methods.
#		--pysrvname $(SERVICE_CAPS).$(SERVICE_CAPS)Server \

	kb-sdk compile $(SPEC_FILE) \
		--out $(LIB_DIR) \
		--pyclname $(SERVICE_CAPS).$(SERVICE_CAPS)Client \
		--dynservver release \
		--pyimplname $(SERVICE_CAPS).$(SERVICE_CAPS)Impl;
	- rm $(LIB_DIR)/$(SERVICE_CAPS)Server.py

	kb-sdk compile $(SPEC_FILE) \
		--out . \
		--html \

test:
	echo Use test-sdkless

clean:
	rm -rfv $(LBIN_DIR)

#
# HOST SCRIPTS
# All tasks prefixed with "host-" are designed to be run on the host machine;
# All others are designed to be run within a container or on a host machine fully configured.
#

# Managing development container orchestration

host-start-dev-server:
	source scripts/dev-server-env.sh && sh scripts/start-dev-server.sh

host-stop-dev-server:
	source scripts/dev-server-env.sh && sh scripts/stop-dev-server.sh

host-remove-dev-server:
	source scripts/dev-server-env.sh && sh scripts/remove-dev-server.sh

# Running tests

host-test-begin: 
	@echo "Beginning tests..."
	docker compose -f test/docker-compose-test.yml run --rm test test-begin

host-test-end: 
	@echo "Ending tests..."
	docker compose -f test/docker-compose-test.yml run --rm test test-end

host-test-unit: 
	@echo "Running unit tests..."
	docker compose -f test/docker-compose-test.yml run --rm test test-unit
	@echo "Unit tests done"



#
# docker-compose-test.yml adds the testing container
# docker-compose-test-integration.yml adds support for integrating with the main docker compose services

host-test-integration-stop:
	@echo "Stopping integration test stack"
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services docker compose -f test/docker-compose.yml stop
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services docker compose -f test/docker-compose.yml rm -f
	@echo "Integration test stack stopped"

host-test-stop-sampleservice:
	@echo "Stopping sampleservice container"
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services docker compose -f test/docker-compose.yml stop sampleservice
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services docker compose -f test/docker-compose.yml rm -f sampleservice
	@echo "sampleservice stopped"

host-test-stop-arangodb:
	@echo "Stopping arango container"
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services docker compose -f test/docker-compose.yml stop arangodb
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services docker compose -f test/docker-compose.yml rm -f arangodb
	@echo "arango stopped"

host-test-integration:
	@echo "Running integration tests..."
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services \
	docker compose \
		-f test/docker-compose.yml \
		-f test/docker-compose-test.yml \
		-f test/docker-compose-test-integration.yml \
		run --rm test test-integration
	@echo "Integration tests done."

host-test-system:
	@echo "Running system tests..."
	MOCK_DATASET_PATH=${PWD}/test/data/mock_services \
	docker compose \
		-f test/docker-compose.yml \
		-f test/docker-compose-test.yml \
		-f test/docker-compose-test-system.yml \
		run --rm test test-system
	@echo "System tests done."


# Note need to stop the sampleservice between integration and system tests since we need to instrument the sample service just for system tests
host-test-all: host-test-begin host-test-unit host-test-integration host-test-stop-sampleservice host-test-stop-arangodb host-test-system host-test-integration-stop host-test-end

host-test-unit-all: host-test-begin host-test-unit host-test-end

##
## Testing
##

test-begin:
	- coverage erase
	- rm cov_profile.lcov
	- rm -rf htmlcov

test-end:
	@echo "Combining coverage files"
	coverage combine .coverage-*
	@echo "Creating html coverage report"
	coverage html
	@echo "Converting coverage to lcov"
	coverage-lcov --data_file_path .coverage --output_file_path cov_profile.lcov

wait-for-sample-service:
	@echo "Waiting for SampleService to be available"
	@[ "${SAMPLE_SERVICE_URL}" ] || (echo "! Environment variable SAMPLE_SERVICE_URL must be set"; exit 1)
	PYTHONPATH=$(TEST_PYPATH) python -c "from testing.shared.wait_for import wait_for_sample_service; wait_for_sample_service('$(SAMPLE_SERVICE_URL)', 60, 1)"

test-integration:
	@echo "Running integration tests (pytest) in $(INTEGRATION_TEST_SPEC)"
	PYTHONPATH=$(TEST_PYPATH) SAMPLESERV_TEST_FILE=$(INTEGRATION_TEST_CONFIG) \
		coverage run \
			--rcfile=$(TEST_DIR)/coveragerc-integration \
			--module pytest --verbose $(INTEGRATION_TEST_SPEC)

# Note that coverage is through the sampleservice container
test-system:
	@echo "Running service tests (pytest) in $(SYSTEM_TEST_SPEC)"
	PYTHONPATH=$(TEST_PYPATH) SAMPLESERV_TEST_FILE=$(SYSTEM_TEST_CONFIG) \
		pytest --verbose $(SYSTEM_TEST_SPEC)

test-unit:
	@echo "Running unit tests (pytest) in $(UNIT_TEST_SPEC) with path $(TEST_PYPATH)"
	PYTHONPATH=$(TEST_PYPATH) SAMPLESERV_TEST_FILE=$(UNIT_TEST_CONFIG) \
		coverage run \
			--rcfile=$(TEST_DIR)/coveragerc-unit \
			--module pytest --verbose $(UNIT_TEST_SPEC)

install-sdk: 
	scripts/install-sdk.sh