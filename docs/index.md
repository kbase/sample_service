# KBase Sample Service

## Overview

The Sample Service stores information regarding experimental samples taken from the environment.
It supports Access Control Lists for each sample, subsample trees, and modular metadata
validation.

The SDK API specification for the service is contained in the `SampleService.spec` file. An indexed interactive version is [also available](http://htmlpreview.github.io/?https://github.com/kbaseIncubator/sample_service/blob/master/SampleService.html).

## Contents

- [Configuration](./configuration.md)
- [Testing](./testing/index.md)
- Development
  - [With Docker Containers](./development/local-docker.md)
  - [MyPy](./development/mypy.md)
- Design and Operation
  - [API Errors](./design/errors.md)
  - [Validation](./design/validation.md)
  - [Built-in Validators](./design/built-in-validators.md)
  - [Kafka Notifications](./design/kafka.md)
  - [Implementation Notes](./design/implementation_notes.md)
  - [Sample Service / Relation Engine data linking](./design/link_ws_data_to_sample_in_RE.md)
  - [Linking workspace data to samples](./design/link_ws_data_to_sample.md)
- [GitHub Action Workflow](./github-action-workflow.md)
- [Additional Info](./additional.md)
- [TODO](./TODO.md)