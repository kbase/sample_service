# Testing


## Requirements

Although this service is written in Python, in order to test it you only need `docker`, `make`, and an `sh`-compatible shell available on your host system.

The automation tools use `make` and `sh`, which configure and run docker containers via `docker-compose`. Test output is written to the console, and  produces html coverage reports

Dependencies:

- docker
- make
- sh

### Docker Images

The required docker images are noted in the `docker-compose.yml` file in the `test/` directory of the repo.

> Note that these docker-compose files are separate from the development docker compose file located in `dev`.

The service images specified in the docker compose file should match those that are used in actual deployments (or perhaps the relationship is reversed - one should only deploy with versions that match the testing images.)

Generally, the required services are:

- ArangoDB 3.5.1+ with RocksDB as the storage engine
- Kafa 2.5.0+
- KBase Mock Services

### Divergence from SDK Tests

As noted elsewhere, this service is designed to be relatively compliant with those generated and managed by the [KBase SDK](https://github.com/kbase/kb_sdk). This assists those familiar with KBase App development. However, due to constraints of the KB-SDK, tests cannot currently be run by the standard mechanism.

### To Run Tests

Tests are divided into three sets: unit, integration, and system

- _unit tests_ run only against code, requiring no services to be spun up
- _integration tests_ run local code which accesses dependent services
- _system tests_ run the public api of the sample service, and do not require access to source code other than tests

Each of these test suites may be run independently, or in sequence.

#### Run All Tests

You may run all tests with a single command

```shell
make host-test-all
```

##### macOS Note

Recent versions of macOS (starting with 12 - Monterey) utilize port 5000, which just happens to be the port KBase services use by tradition. It is also a reserved port more generally.

To avoid a conflict, you should use the `PORT` environment variable to choose another port, like `5001`:

```shell
PORT=5001 make host-test-all
```

#### Test task naming convention

You have probably noticed the somewhat awkward `host-` prefix for the make task above. This is due to the fact that the Makefile supports both host and container operations. This can be quite confusing to KBase newcomers (well, it was to me), and is a continual source of obscurity.

For instance, in `kb_sdk` based apps, `make compile` is designed to be run from the host (directly on one's development machine) as well as by the app registration service, but `make test` is only supposed to be run by `kb_sdk` itself - one should use `kb-sdk test` to invoke the testing process which runs within a container.

To help make the purpose of the new make tasks clear, the ones designed to be run by a developer (or GHA workflow) are prefixed with `host-`, and the ones designed to be run within a container are not.

### Testing Containers

The docker-compose files exist in the `test/` directory, in order to simplify the top level of the repo, and because they are only used for testing, not deployment or development.

(There is a separate `dev/docker-compose.yml` for development workflows.)

The docker-compose files are divided into three parts:

- `docker-compose.yml` provides the basic orchestration of the main sample_service service, as well as the runtime services it depends on: arangodb, kafka, workspace, auth. It also defines environment variables for service configuration.
- `docker-compose-test.yml` defines a `test` service for running test code; it uses the service image; it is used standalone to run unit tests.
- `docker-compose-test-with-services.yml` extends the `test` service to depend on the sample service container - which prompts the orchestrated launching of the sample service and all dependent services; it is used for running integration and system tests.

As used in the `Makefile`, the docker containers are layered. See `host-test-unit`, `host-test-integration`, `host-test-system`.

### Makefile

All tests should be run through the provided `make` tasks, which are divided into host-run tasks (prefixed with `host-`), and container-run tasks (prefixed with `test-`). Only the `host-` tests should be run directly by the developer or GHA workflow; other make tasks are run by the entrypoint script within the container itself.

Make tasks for preparation before and cleanup after tests:

- `make host-test-begin`: runs the entrypoint with the `test-begin` command (which runs `make test-begin`, which in turn erases any test coverage data)
- `make host-test-end`: runs the entrypoint with `test-end`, which in turn runs `make test-end`, which generates test coverage reports (_html_, _lcov_)
- `make host-test-stop`: stops all service containers.

Test runners:

- `host-test-unit`:  invokes the entrypoint with `test-unit`, which in turn runs `make test-unit`, which runs the unit tests via `pytest`.
- `host-test-integration`:  invokes the entrypoint with `test-integration`, which in turn runs `make test-integration`, which runs the integration tests via `pytest`.
- `host-test-system`: invokes the entrypoint with `test-system`, which in turn runs `make test-system`, which runs the system tests via `pytest`.

Test workflows:

Each of these workflows fully runs one type of test, producing coverage in `htmlcov` and `cov_profile.lcov`.

- `make host-test-unit-all` runs the unit tests, taking care of setting up, running, and finishing up after tests. It is composed of the following sub-tasks:
  - host-test-begin
  - host-test-unit
  - host-test-end
- `make host-test-integration-all` runs the integration tests, taking care of setting up, running, and finishing up after tests. It is composed of the following sub-tasks:
  - host-test-begin
  - host-test-integration
  - host-test-stop
  - host-test-end
- `make host-test-system-all` runs the system tests, taking care of setting up, running, and finishing up after tests. It is composed of the following sub-tasks:
  - host-test-begin
  - host-test-system
  - host-test-stop
  - host-test-end

Finally, one can run the whole shebang:

- `make host-test-all` runs the unit, integration and system tests, taking care of setting up, running, and finishing up after tests. It is composed of the following sub-tasks:
  - host-test-begin
  - host-test-unit
  - host-test-integration
  - host-test-system
  - host-test-stop
  - host-test-end

### Entrypoint

All tests run with a special entrypoint script, located in `test/scripts/entrypoint.sh`. This eliminates the mixing of the production and testing support within the entrypoint, and simplifies each file (which have become more complex with the addition of entrypoint commands to invoke tests.)

### Invoking test commands

Test "commands" are simply strings passed as the "COMMAND" to the "ENTRYPOINT" for the test container.

The basic invocation for test commands is via the Makefile:

```shell
make host-test-COMMAND
```

Where `COMMAND` corresponds to the command specified to the docker container.

```shell
docker compose -f test/docker-compose-test.yml run --rm test COMMAND
```

The available commands are:

- `begin`:
- `end`:
- `unit`:
- `integration`:
- `system`:

Note that this is a subset of the available make tasks.

### Other make tasks

[ discuss here make host-test-stop, and the host-test-TYPE-all ]

### Test Container

All tests are run in a `test` container which uses the regular sample service image. The reason for a separate container is that this allows us to expand the entrypoint without interfering with the service container. It also allows us to run the test container independently of the service, as unit tests require.

The test container is managed by two docker compose files.

`docker-compose-test.yml` provides the basic configuration for the test container, sets up the test entrypoint, maps the repo into the container.

This container is suitable as-is for unit tests.

`docker-compose-test-with-services` simply extends the docker compose configuration above with a dependency on the `sampleservice` container.

The resulting container is suitable for both integration and system tests, as it ensures that the associated services are running.

### Coverage

Coverage is collected with the Python _coverage_ package.

Each type of test uses its own `coveragerc` configuration file, located in the `test` directory:

- `test/coveragerc-unit`
- `test/coveragerc-integration`
- `test/coveragerc-system`

Coverage data is placed into files named after the tests, so `.coverage-unit`, `.coverage-integration`, and `.coverage-system-*` (system coverage is in multiple files, see below).

Since coverage is collected from all three tests independently, we can evaluate test coverage for unit, integration, and system tests separately.

When the reports are prepared with `make host-test-end`, all of the coverage data is merged into a single `.coverage` file.

Unit and integration test coverage is gathered from the `test` container, since those tests touch the tested code directly. 

System test coverage is gathered from the `sampleservice` container. System tests invoke the network endpoints only, so we need to instrument the service as it is running. 

This is arranged through the usage of `test/sitecustomize.py`, a standard Python mechanism to run code as the interpreter starts up, but before the server code is invoked. This behavior is automatic, triggered by the presence of `sitecustomize.py` in the Python path.

Since `sitecustomize.py` is in the `test` directory, it is not invoked by the production run of the sample service, since the Python path only includes the `test` directory when running tests.

In addition, the `COVERAGE_PROCESS_START` environment variable is set to `test/coveragerc-system`, to indicate that this is the coverage configuration file to utilize.

### Unit Tests

Unit tests require only the source code from the project and a suitable Python environment. They are run directly in the service container, and require only a simple docker-compose file, `test/docker-compose-unit.yml`, which creates and invokes a test container.

The test container is based on the service image but does not run the sample service upon startup.

Note that the make task is prefixed with `host-`. This indicates that the task is meant to be run on a host machine (developer, CI, etc.) rather than within the service instance (i.e. within the container.)

To run unit tests alone:

```shell
make host-test-unit-all
```

This invocation will:

- create the testing container
- run the unit tests inside the container
- create coverage a human-readable coverage report in `htmlcov` and an _lcov_ compatible file `cov_profile.lcov`

### Integration Tests

Integration tests require the source code as well as associated services, but not the sample service itself. Therefore these tests require that the suite of dependent services by started before they are run. The distinguishing feature of integration tests is that they exercise aspects of the codebase which in turn communicate with services other than the _sampleservice_.

The basic invocation for integration tests is:

```shell
make host-test-integration-all
```

Which will

- create the test container
- ensure that sample service and dependent services are started
- run the integration tests inside the container
- create coverage a human-readable coverage report in `htmlcov` and an _lcov_ compatible file `cov_profile.lcov`

Note that although the _sampleservice_ is started as part of the docker compose orchestration, it is not actually utilized by integration tests.

### System Tests

System tests are similar to integration tests, in that they require services to be running, but differ in that they do not directly invoke service source code. Rather, they invoke service network endpoints - sending parameters, inspecting results.

Since the code we are interested in for system tests is in the running sample service itself, coverage is configured for the `sampleservice` container via `sitecustomize.py` as well as the `test` entrypoint command for the 

In truth, system tests could be run from any language.

### Test Data

A major change to testing is the manner in which test data is configured and made available to tests. 

Before this change, test data is primarily available directly within test code, and in the case of dependent KBase services, instantiated into local binary instances of those services via their respective APIs.

After this change, most test data is provided via json files, most of which are utilized by the `kbase-mock-services` service, which provides mock endpoints for KBase services. Test data is available in `test/data`.

The replacement of host-installed binaries with their equivalent docker containers required a change like this.

One alternative considered was to run KBase services via "mini-kbase". However, after discussion it was felt that "mini-kbase" was not "mini enough" nor mature enough. In other words, it's host requirements are too large (too many containers, too much cpu and memory requirement to reasonably run on developer hardware) and it is not used enough  that we have confidence it is worth getting to work well (at this point in time.)

### 3rd Party Services

The sample service stores data in ArangoDB, and interfaces with Kafka to send and receive messages to coordinate with other KBase services.

These services are run in their respective containers defined in `test/docker-compose.yml`.

The ArangoDB instance is populated with collections at test beginning. These collections are cleared between tests. Removing and recreating collections is too slow. Other than collections, ArangoDB is utilized during tests directly and via the sample service.

The Kafka instance is utilized in a subset of tests to ensure that the appropriate messages are generated and consumed.

### KBase Services Mock Endpoint

As opposed to 3rd party services, KBase services are mocked by a single mock service endpoint. This is done because:

- running actual services via mini-kbase is too resource intensive
- KBase service endpoint utilized are rather limited, simple, constrained and used in a deterministic manner, which is suitable for the usage of static test data.

The KBase Mock Services is a Deno server located at https://github.com/kbaseIncubator/kbase-mock-services. Deno was chosen because it supports *Typescript*, the language of choice for front end development at KBase, and requires very little configuration. The mock service started as a tool for usage in front end development, and repurposed for this project.

It is an incomplete project, but nevertheless works well in this case.

## GitHub Action Workflows

All tests are run in GitHub Action workflows. See [GitHub Action Workflows](./github-action-workflows.md) for details.

## Coverage

Coverage is collected from all three tests independently. This allows us to evaluate test coverage for unit, integration, and system tests separately, which can be useful for evaluating the coverage of those styles of tests.

For the overall coverage, all coverage collection databases are combined together, and reports created for humans (html) and `lcov`-formatted data created for the "CodeCov" service.

### Server Coverage

The system tests collect coverage from the running sample service server, rather from the codebase accessed by the test code.

This is arranged through the usage of `test/sitecustomize.py`. Since `sitecustomize.py` is in the `test` directory, it is not invoked by the production run of the sample service.

In `test/docker-compose.yml`, the sample service is invoked with the `test` entrypoint option. This causes `entrypoint.sh` to include the `test` directory in the Python path, and thus invoke `sitecustomize.py`.

In addition, it sets the `COVERAGE_PROCESS_START` environment variable to `test/coveragerc-system`, to indicate that this is the coverage configuration file to utilize.
