# Testing


## Requirements

Although this service is written in Python, in order to test it you only need `docker`, `make`, and an `sh`-compatible shell.

The automation tools use `make` and `sh`, which configure and run docker containers via docker-compose. Test output is written to the console, and also produces html coverage reports

- docker
- make

### Docker Images

The required docker images are noted in the `docker-compose.yml` file in the root of the repo. 

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
make host-test-unit
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



The Sample Service requires only 

The Sample Service requires ArangoDB 3.5.1+ with RocksDB as the storage engine.

If Kafka notifications are enabled, the Sample Service requires Kafka 2.5.0+.

To run tests, MongoDB 3.6+ and the KBase Jars file repo are also required. Kafka is always
required to run tests.

See `.travis.yml` for an example of how to set up tests, including creating a `test.cfg` file
from the `test/test.cfg.example` file.

Once the dependencies are installed, run:

```shell
pipenv install --dev
pipenv shell
make test-sdkless
```

`kb-sdk test` does not currently pass.