# Makefile support for testing

First let me caveat by saying that I don't think make is a particularly good tool for running tests. I'd actually go further and state that using `make` as a task runner is a mistake, as it is designed to "make" static resources like object files and executables, we we do no such thing with it.

In this document, we will refer to make "tasks". These are the labeled sets of recipes which we can invoke through an invocation of `make` (e.g. `make build`) and which are actually referred to as "targets". This is because make is designed to expect the target to be an actual file. However, we do not utilize them as files, but rather as tasks or commands, so we will refer to them that way.

With that out of the way, let us describe how we do use `make` and it's loyal companion `Makefile` to support running of tests.

## Tasks

First, let us simply catalog all make tasks related to testing:

### Top Level Tasks

First, there are the tasks which a developer is expected to run in the normal course of development:

- host-test-all
- host-test-unit-all
- host-test-integration-all
- host-test-system-all

The tasks are suffixed with "-all" because they do not just run tests, but set up the tests, run the tests, generate coverage reports, and then clean up afterwards.

Each of these "-all" tasks will setup for tests, run tests, and then clean up afterwards.

`host-test-all` is the canonical, do-it-all test. It runs all the tests, and should be run prior to pushing up commits, and is run in the GitHub action workflow.

The rest of the "-all" tests run the respective types of tests - unit, integration, system. It can be useful to run these tests separately, especially when adding or updating tests, as it can make iteration quicker.

- Unit tests are much quicker to run than the integration and system tests, and should be updated with any new or changed functionality to ensure that it is covered.
- Integration tests are primarily dedicated to testing code which interacts with Arango or Kafka, and should be updated for code which interacts with them
- System tests run against the public api endpoints and should be updated when new api endpoints are added, or existing ones updated.

#### Components of Top Level Tasks

These "-all" tasks are composed of the following sub-tasks:

- test runners:
  - host-test-unit
  - host-test-integration
  - host-test-system
- test lifecycle support
  - host-test-begin
  - host-test-stop
  - host-test-stop2
  - host-test-end

All of these tasks run commands through a container.

The "test runner" tasks invoke the actual python tests. These tests are run inside a container. See [tests in docker](./docker.md) for a description of these tests.

The "lifecycle support" tasks support 3 basic tasks for test support:

##### Test Begin

The `host-test-begin` task prepares for a testing run by removing coverage files from previous test runs

##### Test Stop

The `host-test-stop` task stops the running test containers after tests have completed.

##### Test End

The `host-test-end` tasks merges the separate coverage data runs and generates coverage reports

#### Internal Test Tasks

