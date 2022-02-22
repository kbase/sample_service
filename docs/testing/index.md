# Testing



## Contents

- [Quick Start](#quick-start)
- [Requirements - what you need on your machine first](#requirements)
- [Docker](#docker)
- [Divergence from SDK Tests](#divergence-from-sdk-tests)
- [Running Tests](#running-tests)
- [Makefile](#makefile)
- [Entrypoint](#entrypoint)

## Quick Start

### Dependencies

Ensure you have `docker`, `make` and a `sh`-compatible shell installed on your machine. 

### Run Tests

Run all tests with a single command

```shell
make host-test-all
```

Open `htmlcov/index.html` to bask in the coverage report.

## Requirements

Although this service is written in Python, in order to run its tests you only need `docker`, `make`, and an `sh`-compatible shell available on your host system.

The automation tools use `make` and `sh`, which configure and run docker containers via `docker-compose`. Test output is written to the console, and  produces html coverage reports.

The default shell on your machine should be fine.

## Docker

The required docker images are noted in the `docker-compose-*.yml` files in the `test/` directory of the repo.

> Note that these docker-compose files are separate from the development docker compose file located in `dev`.

The service images specified in the docker compose file should match those that are used in actual deployments (or perhaps the relationship is reversed - one should only deploy with versions that match the testing images.)

Generally, the required services are:

- ArangoDB 3.5.1+ with RocksDB as the storage engine
- Kafa 2.5.0+
- KBase Mock Services

## Divergence from SDK Tests

As noted elsewhere, this service is designed to be relatively compliant with those generated and managed by the [KBase SDK](https://github.com/kbase/kb_sdk). This assists those familiar with KBase App development. However, due to constraints of the KB-SDK, tests cannot currently be run by the standard mechanism. In fact, the test structure and mechanisms are completely different than those used by kb-sdk.

## Running Tests

Tests are divided into three sets: unit, integration, and system

- _unit tests_ run only against local service code, requiring no services to be spun up
- _integration tests_ run local service code which accesses dependent services
- _system tests_ run the public api of the sample service, and do not require access to source code other than tests

Each of these test suites may be run independently, or in sequence via a pre-built recipe.

### Invoking test commands

Each test task has an associated "command". These commands are used in different ways to invoke the tests through the container stack:

The available commands are:

- `begin`
- `stop`
- `end`
- `unit`
- `integration`
- `system`

(a `stop2`, identical to `stop` is utilized to resolve a make issue.)

Test "commands" are utilized in the following ways:

- for host-based make task name `make host-test-COMMAND`
- for container-based make task name `make test-COMMAND`
- for the testing entrypoint; passed as the "COMMAND" to the "ENTRYPOINT" for the test container.

The developer invocation of test commands is via the Makefile:

```shell
make host-test-COMMAND
```

For example 

```shell
make host-test-begin
```

which in turn runs

```shell
docker compose -f test/docker-compose-test.yml run --rm test begin
```

Note how the make `host-test-begin` task calls `docker compose -f test/docker-compose-test.yml run --rm test` passing the command `begin`.

#### The "-all" tasks

Although it is useful to have the Makefile define tasks (recipes) for each test running stage, in day-to-day usage, a developer will actually run one of the tasks with the "-all" suffix. These tasks run all subtasks in order to complete an entire test run.

- host-test-all
  - also `make test`
- host-test-unit-all
- host-test-integration-all
- host-test-system-all

### Run All Tests

You may run all tests with a single command

```shell
make host-test-all
```

or 

```shell
make test
```

### Test task naming convention

You may have noted the somewhat awkward `host-` prefix for the make task above. This is due to the fact that the Makefile supports both host and container operations. This can be quite confusing to KBase newcomers, and is a continual source of obscurity.

For instance, in `kb_sdk` based apps, `make compile` is designed to be run from the host (directly on one's development machine) as well as by the app registration service, but `make test` is only supposed to be run by `kb_sdk` itself - one should use `kb-sdk test` to invoke the testing process which runs within a container.

To help make the purpose of the testing make tasks clear, the ones designed to be run by a developer (or GHA workflow) are most prefixed with `host-`, and the ones designed to be run within a container are not.

## Makefile

All tests should be run through the provided `make` tasks, which are divided into host-run tasks (prefixed with `host-`), and container-run tasks (prefixed with `test-`). Only the `host-` tests should be run directly by the developer or GHA workflow; other make tasks are run by the entrypoint script within the container itself.

Please see the [makefile](./makefile) document for a breakdown of all the make tasks.

## Entrypoint

All tests run with a special entrypoint script, located in `test/scripts/entrypoint.sh`, overriding the service entrypoint located in `scripts/entrypoint.sh`.

This eliminates the mixing of the production and testing support within the entrypoint, and simplifies each entrypoint file (which have become more complex with the addition of entrypoint commands to invoke tests.)

## Test Container

All tests are run in a `test` container which uses the  sample service image. The reason for a separate container is that this allows us to expand the entrypoint without interfering with the service container. It also allows us to run the test container independently of the service, as unit tests require.

Please see [docker](./docker.md) for details.

## Running Tests

### Unit Tests

To run unit tests alone:

```shell
make host-test-unit-all
```

See [unit tests](./unit-tests.md) for details

### Integration Tests

Integration tests require the source code as well as associated services, but not the sample service itself. Therefore these tests require that the suite of dependent services by started before they are run. The distinguishing feature of integration tests is that they exercise aspects of the codebase which in turn communicate with services other than the _sampleservice_.

The basic invocation for integration tests is:

```shell
make host-test-integration-all
```

See [integration tests](./integration-tests.md) for details

### System Tests

System tests are similar to integration tests, in that they require services to be running, but differ in that they do not directly invoke service source code. Rather, they invoke service network endpoints - sending parameters, inspecting results.

```shell
make host-test-system-all
```

See [system tests](./system-tests.md) for details

Since the code we are interested in for system tests is in the running sample service itself, coverage is configured for the `sampleservice` container via `sitecustomize.py` as well as the `test` entrypoint command for the 

In truth, system tests could be run from any language.

### Test Data

A major feature to testing is the manner in which test data is configured and made available to tests.

In a previous incarnation of testing, test data was created directly within test code, and in the case of dependent KBase services, instantiated into local binary instances of those services via their respective APIs.

Now most test data is provided via json files, most of which are utilized by the `kbase-mock-services` service, which provides mock endpoints for KBase services. Test data is available in `test/data`.

### 3rd Party Services

The sample service stores data in ArangoDB, and interfaces with Kafka to send and receive messages to coordinate with other KBase services.

These services are run in their respective containers defined in `test/docker-compose-test-with-services.yml`.

The ArangoDB instance is populated with collections at test beginning. These collections are cleared between tests. (Removing and recreating collections is more straightforward, but too slow.) ArangoDB is utilized during tests directly and via the sample service.

The Kafka instance is utilized in a subset of tests to ensure that the appropriate messages are generated and consumed.

### KBase Services Mock Endpoint

As opposed to 3rd party services, KBase services are mocked by a single mock service endpoint. This is done because:

- running actual services via mini-kbase is too resource intensive
- KBase service endpoints utilized are rather limited, simple, constrained and used in a deterministic manner, which is suitable for the usage of static test data.

The KBase Mock Services is a Deno server located at `https://github.com/kbaseIncubator/kbase-mock-services`. Deno was chosen because it supports *TypeScript*, the language of choice for front end development at KBase, and requires very little configuration and no direct dependency installation. The mock service project started as a tool for usage in front end development, and repurposed for this project.

It is an incomplete project, but nevertheless works well in this case.

## GitHub Action Workflow

All tests are run in a GitHub Action workflow. See [GitHub Action Workflow](./github-action-workflo/index.md) for details.

## Coverage

Coverage is collected from all three tests independently. This allows us to evaluate test coverage for unit, integration, and system tests separately, which can be useful for evaluating the coverage of those styles of tests.

For the overall coverage, all coverage collection databases are combined together, and reports created for humans (html) and `lcov`-formatted data created for the "CodeCov" service.

To inspect coverage results for locally-run tests, open `htmlcov/index.html`. 

Coverage run in the GHA workflow are made available at the ["CodeCov" service](https://app.codecov.io/gh/kbase/sample_service).

> If working from a fork, you may find the CodeCov results in your codecov space under the url `https://app.codecov.io/gh/YOUR_GITHUB_ACCOUNT/sample_service`. This can be useful especially when developing new tests or altering the test runner code in order to ensure CodeCov correctly captures coverage.

For details see [coverage](./coverage.md).
