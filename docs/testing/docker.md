# Testing with Docker

All tests and test tasks are run inside a docker container. This container uses the image defined in the service Dockerfile located at the root of the project. The container is defined in `test/docker-compose-test.yml`. This container is identical to the service container, other than overriding the entrypoint to use one dedicated to testing tasks.

In addition to the test-runner container, there are several other containers utilized in integration and system tests:

- arangodb - the database used by the sample service and other KBase services (Relation Engine)
- kafka - an event streaming service used by KBase services
- zookeeper - required by kafka; a distributed configuration service.
- mock services - a kbase project which provides mock endpoints for jsonrpc 1.1, 2.0, and REST-style services such as workspace and auth.

The test containers are managed by three docker compose files:

`docker-compose-test.yml` provides the basic configuration for the test container, sets up the test entrypoint, maps the repo into the container.

This container is suitable as-is for unit tests.

`docker-compose-test-with-services` adds the sample service itself, all containers for required services. It creates a dependency from the testing container to the sampleservice container (which in turn depends on the arangodb, kafka, and mock services containers.)

`docker-compose-test-system` simply alters the sampleservice container to add the command "coverage" to ensure that coverage is collected for the service.

## Layered docker-compose

`docker compose` supports using more than one "docker-compose.yml" configuration file. Each additional file is merged with the previous one. This allows a "layering" of docker compose files, reducing duplication.

Let's repeat the description of the testing compose files,with an emphasis on their layering:

- `docker-compose-test.yml` defines the testing container

- `docker-compose-test-with-services` defines the sampleservice, arangodb, kafka, zookeeper, and mock services containers; and creates a dependency from the testing container to the sampleservice container.

- `docker-compose-test-system` simply alters the command for the sampleservice container to collect source code coverage.


> TODO: add diagram of container orchestration