# GitHub Action Workflows

GitHub Action Workflows are in place to run tests and, should they succeed, build and store an image.

## Build - Test - Push

The primary action is `.github/workflows/build-test-push.yml`. This workflow is run for:

 - any push to the `master` branch, or branches preceded with `feature-` or `fix-`,
 - activity on a pull request to the master branch
 - publication of a release against the master branch
 - manually via `workflow_dispatch`

This workflow runs all tests, and should they succeed, builds an image, tagged appropriately (described below), and stored at GitHub Container Registry (GHCR).

### Required Environment

In order to push the resulting image to the GitHub Container Registry, the following secrets must be provided:

- `GHCR_USERNAME` - the GitHub username for which permission is granted to push images to GHCR
- `GHCR_TOKEN` - the GitHub auth token for the above username, with the appropriate permissions

####  Usage in Fork

In order to test changes to the workflows, in some circumstances one must and in other cases probably one should use a fork of the repo.

Using a fork allows one to set `GHCR_USERNAME` and `GCHR_TOKEN` directly, without worrying about compromising the shared secrets used by the KBase organization.

For example, `GHCR_USERNAME` can be set to your own username, and a Personal Access Token (PAT) generated with `write:packages` permission scope, which also provides `repo` scope (full control of private repos)

### Test Coverage Reporting

[ TODO ]

### GHCR Image Tagging

Images are tagged according to the manner of their triggering condition.

#### Push to branch

If the triggering condition is a push to `master`, or a branch prefixed with `feature-` or `fix-`, the image tag will be the `CI_REF_NAME_SLUG` variable set by the `FranzDiebold/github-env-vars-action@v2` GHA.

This variable is a version of the branch name which may be used in URLs. Any characters not allowed in a URL path segment will be replaced with dashes (see https://github.com/FranzDiebold/github-env-vars-action/blob/20f2d338e3f2dbc2dc891a19f826fcdb69a7eb0f/index.js#L12)

E.g. 

- push to master: `ghcr.io/kbase/sample-service:master`
- push to feature branch: `ghcr.io/kbase/sample-service:feature-sam-96-docker-compose`
- push to fix branch: `ghcr.io/kbase/sample-service:fix-sam-99-broken`

#### Pull Request

Pull requests against master result in an image tagged with `pull_request-#`, where `pull_request-` is fixed, and `#` is the pull request number.

E.g.
- activity on PR 5 results in: `ghcr.io/kbase/sample-service:pull_request-5`

#### Release

A GitHub release publication will result in an image tagged with `release-#`, where `release-` is fixed, and `#` is the release version.

E.g.
- For release 1.0.0: `ghcr.io/kbase/sample-service:release-v1.0.0`


#### Manually

The workflow may be run manually as well. This can be useful for triggering build, test, push for arbitrary branches not covered by the triggering conditions.

## Run Tests

A small workflow is available purely for running tests. This workflow is a subset of "build-test-push", and may only be run manually.

This can be useful to ensure tests pass with a given branch, without creating an actual deployment image.

## TODO

- use sub-workflow for tests to eliminate duplication between workflows
- code quality checks - get full suite running, document
- add workflow to remove pull request images after they are closed