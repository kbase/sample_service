# Coverage

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

## Server Coverage

The system tests collect coverage from the running sample service server, rather from the codebase accessed by the test code.

This is arranged through the usage of `test/sitecustomize.py`. Since `sitecustomize.py` is in the `test` directory, it is not invoked by the production run of the sample service.

In `test/docker-compose.yml`, the sample service is invoked with the `test` entrypoint option. This causes `entrypoint.sh` to include the `test` directory in the Python path, and thus invoke `sitecustomize.py`.

In addition, it sets the `COVERAGE_PROCESS_START` environment variable to `test/coveragerc-system`, to indicate that this is the coverage configuration file to utilize.