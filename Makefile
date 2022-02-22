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

test: host-test-all
	
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


# Startup, teardown

host-test-begin: 
	@echo "Beginning tests..."
	docker compose -f test/docker-compose-test.yml run --rm test begin

host-test-end: 
	@echo "Ending tests..."
	docker compose -f test/docker-compose-test.yml run --rm test end

host-test-stop:
	@echo "Stopping all test services"
	docker compose -f test/docker-compose-test.yml -f test/docker-compose-test-with-services.yml stop
	docker compose -f test/docker-compose-test.yml -f test/docker-compose-test-with-services.yml rm -f
	@echo "Test services stopped"

host-test-stop2:
	@echo "Stopping all test services"
	docker compose -f test/docker-compose-test.yml -f test/docker-compose-test-with-services.yml stop
	docker compose -f test/docker-compose-test.yml -f test/docker-compose-test-with-services.yml rm -f
	@echo "Test services stopped"

#
# Run test groups: unit, integration, system
#

host-test-unit: 
	@echo "Running unit tests..."
	docker compose -f test/docker-compose-test.yml run --rm test unit
	@echo "Unit tests done"

host-test-integration:
	@echo "Running integration tests..."
	docker compose \
		-f test/docker-compose-test.yml \
		-f test/docker-compose-test-with-services.yml \
		run --rm test integration
	@echo "Integration tests done."

host-test-system:
	@echo "Running system tests..."
	docker compose \
		-f test/docker-compose-test.yml \
		-f test/docker-compose-test-with-services.yml \
		-f test/docker-compose-test-system.yml \
		run --rm test system
	@echo "System tests done."


#
# Bundled tasks. Each one of these will handle test environment startup, teardown, and generation of 
# coverage reports
#
host-test-all: host-test-begin host-test-unit host-test-integration host-test-stop host-test-system host-test-stop2 host-test-end

host-test-unit-all: host-test-begin host-test-unit host-test-end

host-test-integration-all: host-test-begin host-test-integration host-test-stop host-test-end

host-test-system-all: host-test-begin host-test-system host-test-stop host-test-end

##
## Testing within container
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
	PYTHONPATH=$(TEST_PYPATH) python -c "from testing.shared.wait_for import wait_for_sample_service; wait_for_sample_service('$(SAMPLE_SERVICE_URL)', 60, 1) or sys.exit(1)"

test-integration:
	@echo "Running integration tests (pytest) in $(INTEGRATION_TEST_SPEC)"
	PYTHONPATH=$(TEST_PYPATH) SAMPLESERV_TEST_FILE=$(INTEGRATION_TEST_CONFIG) \
		coverage run \
			--rcfile=$(TEST_DIR)/coveragerc-integration \
			--module pytest --verbose $(INTEGRATION_TEST_SPEC)

# Note that coverage is through the sampleservice container
test-system:
	@echo "Running system tests (pytest) in $(SYSTEM_TEST_SPEC)"
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
