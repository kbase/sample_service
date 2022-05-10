# Workflows

Of the 9 workflow files comprising the GHA support, 3 are [_reusable workflows_](https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/reusing-workflows) containing the primary workflow logic, and 7 are _controlling workflows_ (my term) which invoke reusable workflows and are triggered by specific conditions.

> GitHub Actions supports a type of workflow termed a [_reusable workflow_](https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/reusing-workflows). Such workflows may only be run by being included in another workflow. They differ from a normal workflow in that they can only use a special triggering condition `on.workflow_call`, and they may define a set of input parameters.

## Reusable Workflows

### `reusable_test-python.yml`

This workflow will run the Python tests defined for the repo. Although the steps in the workflow are not specific to the Sample Service, it is unlikely that other workflows are set up in a compatible manner. 

- check out repo
- set up Python 3.7 in the GHA runtime
- installs pipenv, as the Sample Service is uses pipenv for dependency management and the virtual environment
- set up tests via make task
- run tests via make task
- produce a coverage summary report for easy inspection in the GHA log
- send coverage data to CodeCov

#### inputs

none

#### outputs

none

### `reusable_validate-release-tag.yml` 

This is a simple workflow whose purpose is to ensure that a release tag is in compliance with the expected form. At present that form is the basic semantic version format `#.#.#`. The string is passed in as the input `release_tag`. The workflow will fail (exit with error code 1) if the release tag is not compliant. This prevents a release with a non-compliant tag.

The workflow is implemented in Javascript.

#### inputs

- `release_tag` - the tag used for the release

#### outputs

_none_

#### effects

Will exit the controlling workflow if validation fails

### `reusable_build.yml`

This workflow builds an image from the project's primary Dockerfile. This is useful for including in workflows which need to prove that a service image can be built successfully, but in which the image is not needed, and thus does not need to be stored.

#### inputs

_none_

#### outputs

_none_ 

#### effects

Will exit the controlling workflow if the build fails

### `reusable_build-push.yml`

This workflow captures the process of building the service image and pushing the resulting image to GitHub Container Registry (GCHR) with a given tag. It primarily uses standard, commonly used third party workflows from GitHub and Docker, in addition to custom scripts.

- check out repo
- get and save current date as a timestamp
- setup the build
- log into GHCR with standard secrets
- create tags appropriate usage in next step
- build and push image
  - build image
  - push the image to GHCR with a given name and one or more tags

#### inputs

- `name` - the image name
- `tags` - the image tags; a string, using a comma (`,`) as a list separator

#### outputs

_none_

#### effects

- saves image to GHCR
- will exit the controlling workflow if the build fails, login fails, push fails

## Controlling Workflows

Note that in the diagrams below, only major events are shown. For example, there are numerous additional possible error conditions, but only the most common and interesting ones are shown.

### `pull-request-develop.yml`  
  
Triggered by opening, reopening, or synchronizing a pull request (`opened`, `reopened`, and `synchronize` event) against the `develop` branch. This workflow does not push an image to GHCR.

![pull request to develop opened sequence diagram](./images/pull-request-develop-opened-sequence.png)

### `pull-request-develop-merged.yml`  

Triggered by closing and merging a pull request against the `develop` branch. This workflow  creates an image with name `sample_service-develop` and the tag `latest`.

![pull request to develop merged sequence diagram](./images/pull-request-develop-merged-sequence.png)

### `pull-request-master-opened.yml`  
   
Triggered by opening a pull request (`opened` event)  against the `master` branch. This workflow  creates an image with name `sample_service` and a tag like `pr#`, where `#` is the pull request number.

![pull request master opened sequence diagram](./images/pull-request-master-opened-sequence.png)


### `pull-request-master-merged.yml`  
   
Triggered by closing and merging a pull request against the `master` branch. This workflow  creates an image with name `sample_service` and the tag `latest-rc`.

![pull request master merged sequence diagram](./images/pull-request-master-merged-sequence.png)


### `release-master`  
   
Triggered by the creation (`published` event) of a GitHub release against the `master` branch. This workflow creates an image with the name `sample_service` and applies two tags - the release tag, which is typically a semver `#.#.#`, and `latest-rc`

![release against master published sequence diagram](./images/release-master-sequence.png)


### `manual.yml`  
   
triggered by `workflow_dispatch`, so can be run by the GitHub UI button. It runs both test and image build/push, and a tag which is the branch name. The supports the use case of generating an image from any branch. E.g. in order to preview changes in a feature or fix branch, one may run this workflow specifying a branch which is either the source for a PR or may become one, generating an image that may be previewed and verifying through shared test results that the changes are non-breaking.

![manual sequence diagram](./images/manual-sequence.png)
