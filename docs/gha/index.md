# GitHub Action (GHA) Workflow

This project uses a GitHub Action workflow to

- run unit and integration tests,
- build an image containing the service,
- tag the image appropriately, and 
- publish the image to GitHub Container Registry

under a variety of conditions

This is accomplished with a set of 6 workflow files located in `./github/workflows`.

Of these workflow files, 2 are "reusable workflows" containing the primary workflow logic, and 7 are "controlling workflows" which invoke the reusable workflows and indicate triggering conditions and, optionally, an image tag.

GitHub Actions supports a type of workflow termed a "reusable workflow". Such workflows may be included in another workflow. They differ from a normal workflow in that they can only use a special triggering condition "on.workflow_call", and they may define a set of input parameters.

The reusable workflows are:

- `reusable_test-python.yml` - sets up and runs all tests
  - parameters: none
- `reusable_build-push.yml` - builds the service image, and pushes it to GHCR 
  - parameters
    - `name` - the image name 
    - `tag` - the tag for the image
  - secrets
    - `ghcr_username` - the username for the GHCR push
    - `ghcr_token` - the token associated with the username to authorize GHCR push


Each controlling work runs all tests and creates an image.

The controlling workflows are: 

- `pull-request-develop-opened.yml` - triggered by opening a pull request (`opened` event)  against the `develop` branch. This workflow  creates an image with name `sample_service-develop` and a tag like `pr#`, where `#` is the pull request number. Results in an image reference like ``.

- `pull-request-develop-merged.yml` - triggered by closing and merging a pull request against the `develop` branch. This workflow  creates an image with name `sample_service-develop` and the tag `latest`.

- `pull-request-master-opened.yml` - triggered by opening a pull request (`opened` event)  against the `master` branch. This workflow  creates an image with name `sample_service` and a tag like `pr#`, where `#` is the pull request number.

- `pull-request-master-merged.yml` - triggered by closing and merging a pull request against the `master` branch. This workflow  creates an image with name `sample_service` and the tag `latest-rc`.

- `release-master-version` - triggered by the creation (`published` event) of a GitHub release against the `master` branch. This workflow creates an image with the name `sample_service` and the image tag the same as the release tag, which is typically a semver `#.#.#`.

- `release-master-latest` - identical to above, except that the image tag is `latest`.

- `manual.yml` - triggered by `workflow_dispatch`, so can be run by the GitHub UI button. It runs both test and image build/push, and a tag which is the branch name. The supports the use case of generating an image from any branch. E.g. in order to preview changes in a feature or fix branch, one may run this workflow specifying a branch which is either the source for a PR or may become one, generating an image that may be previewed and verifying through shared test results that the changes are non-breaking.


## Image name and taging requirements

- An image named `{REPONAME}-develop:pr#` is created when a PR to develop is first created.
- An image named `{REPONAME}-develop:latest` is created/tagged when a PR to develop is merged.
- An image named `{REPONAME}:pr#` is created when a PR to main (master) is first created.
- An image named `{REPONAME}:latest-rc` is created/tagged when a PR to main (master) is merged.
- A final release image is published using the Draft a new release functionality, which results in an imaged tagged as `{REPONAME}:x.x.x` and `{REPONAME}:latest`.
- An optional on-demand workflow can be used to trigger image builds from any branch at any time if desired.