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