# Testing


## Requirements

Although this service is written in Python, in order to test it you only need `docker`, `make`, and an `sh`-compatible shell available on your host system.

The automation tools use `make` and `sh`, which configure and run docker containers via `docker-compose`. Test output is written to the console, and also produces html coverage reports

Dependencies:

- docker
- make
- sh

### Docker Images

The required docker images are noted in the `docker-compose.yml` file in the `test/` directory of the repo. 

The service images in the docker compose file should match those that are used in actual deployments (or perhaps the relationship is reversed - one should only deploy with versions that match the testing images.)

Generally, the required services are:

- ArangoDB 3.5.1+ with RocksDB as the storage engine
- Kafa 2.5.0+
- KBase Mock Services

### Divergence from SDK Tests

As noted elsewhere, this service is designed to be relatively compliant with those generated and managed by the [KBase SDK](https://github.com/kbase/kb_sdk). This assists those familiar with KBase App development. However, due to constraints of the KB-SDK, tests cannot currently be run by the standard mechanism.

### To Run Tests

Tests are divided into three sets: unit, integration, and system

- unit tests run only against code, requiring no services to be spun up
- integration tests run against service code, but do require one or more services to be running
- system tests operate solely against the public api of the sample service, and do not require access to source code

Each of these test suites may be run independently, or in sequence.

#### Run All Tests

You may run all tests with a single command

```shell
make host-test-all
```

#### Unit Tests

The basic invocation for unit tests is:

```shell
make host-test-unit-all
```

Note that the make task is prefixed with `host-`. This indicates that the task is meant to be run on a host machine (developer, CI, etc.) rather than within the service instance (i.e. within the container.)

This invocation with will:

- create the testing container, which is identical to the service container, except that it does not start the service, but rather runs the unit tests.
- run the unit tests inside the container
- capture coverage data in the standard Python location, `.coverage`
  - since the repo directory is volume-mounted into the container, the coverage data should be available

There are two make tasks which help with the preparation for tests and processing of coverage data.

`make host-test-begin` clears the coverage data first; this is important because coverage data is otherwise accumulated into a single location from multiple testing runs

`make host-test-end` creates both an LCOV-compatible file (`cov_profile.lcov` - for consumption by coverage tools, like CodeCov), and an html report (in `htmlcov` - suitable for a developer to inspect.)

### Testing Containers

The docker-compose files exist in the `test/` directory, in order to simplify the top level of the repo, and because they are only used for testing and development, not for deployment.

The docker-compose files are divided into three parts:

- `docker-compose.yml` provides the basic orchestration of the main sample_service service, as well as the runtime services it depends on: arangodb, kafka, workspace, auth. It also defines environment variables for services.
- docker-compose-test.yml may be run standalone to run unit tests; unit tests do not require any other services
- docker-compose-test-integration.yml 

### Makefile

All tests should be run through the provided `make` tasks, which are divided into host-run tasks (prefixed with `host-`), and container-run tasks (prefixed with `test-`). Only the `host-` tests should be run directly by the developer or GHA workflow; other make tasks are run by the entrypoint script within the container itself.

- make host-test-unit-all runs the unit tests, taking care of setting up for tests, running the tests, and finishing up after tests. It is composed of the following sub-tasks
  - `host-test-begin`, which runs the entrypoint with the `test-begin` command (defined in , which runs `make test-begin`, which in turn erases any test coverage data
  - `host-test-unit`,  which invokes the entrypoint with `test-unit`, which in turn runs `make test-unit`, which runs the unit tests via pytest.
  - `host-test-end`, which invokes the entrypoint with `test-end`, which in turn runs `make test-end`, which generates test coverage reports (html, lcov)
- `make host-test-all` runs unit, integration, and system tests, as well as the test preparation and finishing tasks.
  - `host-test-begin`
  - `host-test-unit`
  - `host-test-integration`, which invokes the entrypoint with `test-integration`, which in turn runs `make test-integration`, which runs the integration tests via pytest.
  - `host-test-system`, which invokes the entrypoint with `test-system`, which in turn runs `make test-system`, which runs the system tests via pytest.
  - `host-test-end`
  - `host-test-integration-stop`, which stops the associated service containers.

### Entrypoint

All tests run with a special entrypoint script, located in `test/scripts/entrypoint.sh`. This eliminates the mixing of the production and testing support within the entryoint, and simplifies each file (which have become more complex with the addition of entrypoint commands to invoke tests.)

#### Unit Tests

Unit tests require only the source code from the project and a suitable Python environment. They are run directly in the service container, and require only a simple docker-compose file, `test/docker-compose-unit.yml`, which creates and invokes a `test` container, which is based on the service image but does not run the sample service upon startup.

### Integration Tests

Integration tests require the source code as well as associated services. Therefore these tests require that the suite of dependent services by started before they are run. This requires the usage of `test/docker-compose.yml` which provides the basic orchestrated services startup including running the sample service, `test/docker-compose-test.yml` which overrides the entrypoint and brings in the test container, and `test/docker-compose-test-integration.yml` which creates a dependency between the test container and the sampleservice container.

### System Tests

System tests are similar to integration tests, but do not require access to the sample service source code. They test the public network interface to the service. They are run in the same manner as integration tests for simplicity, even though they do not require a test container which contains the sample service source code.

### Test Data

A major change to testing is the manner in which test data is configured and made available to tests. 

Before this change, test data is primarily available directly within test code, and in the case of dependent KBase services, instantiated into local binary instances of those services via their respective APIs.

After this change, most test data is provided via json files, most of which are utilized by the `kbase-mock-services` service, which provides mock endpoints for KBase services. Test data is available in `test/data`.

The replacement of host-installed binaries with their equivalent docker containers required a change like this.

One alternative considered was to run KBase services via "mini-kbase". However, after discussion it was felt that "mini-kbase" was not "mini enough" nor mature enough. In other words, it's host requirements are too large (too many containers, too much cpu and memory requirement to reasonably run on developer hardware) and it is not used enough  that we have confidence it is worth getting to work well (at this point in time.)

### 3rd Party Services

The sample service stores data in ArangoDB, and interfaces with Kafka to send and receive messages to coordinate with other KBase services.

These services are run in their respective containers defined in `test/docker-compose.yml`.

The ArangoDB instance is populated with collections at test beginning. These collections are cleared between tests. Removing and recreating collections is too slow. Other than collections, ArangoDB is utilzed during tests directly and via the sample service.

The Kafka instance is uilized in a subset of tests to ensure that the appropriate messages are generated and consumed.

### KBase Services Mock Endpoint

As opposed to 3rd party services, KBase services are mocked by a single mock service endpoint. This is done because:

- running actual services via mini-kbase is too resource intensive
- KBase service endpoint utilized are rather limited, simple, constrained and used in a deterministic manner, which is suitable for the usage of static test data.

The KBase Mock Services is a Deno server located at https://github.com/kbaseIncubator/kbase-mock-services. Deno was chosen because it supports *Typescript*, the language of choice for front end development at KBase, and requires very little configuration. The mock service started as a tool for usage in front end development, and repurposed for this project.

It is an incomplete projeect, but nevertheless works well in this case.

## GitHub Action Workflows

All of the tests are run in GitHub