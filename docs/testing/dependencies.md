# Test Dependencies

These host programs and their respective requirements and systems need to be available for testing to proceed:

- wget
- java >= 1.8 
- docker
- python 3.7
- pipenv

Unless noted above, the version is probably not important; you should just use the most recent version.

Since tests are run directly on the developer host system, a working **Python 3.7 interpreter** is required. The requirement for version 3.7 is based on the common requirement for all KBase Python services. In addition, since the **pipenv** package manager is used, it must be installed and available (see [developer documentation for using pipenv](../development/using-pipenv.md)).

The **wget** http client is required in order to install KBase jars.

**Java** version 1.8 and above is required to run the **workspace** and **auth** services.

Finally, **docker** is required in order to run, via **docker compose**, the suite of 3rd party services required by the sample service, workspace, and auth.

## Installation

> TODO: complete the installation section; there are many alternatives, but we should provide at least ONE working method of installation for each dependency.

### `wget`

#### macOS

##### macports

```shell
sudo port install wget
```

transitively will install:

- gnutls
- libtasn1
- nettle
- p11-kit

#### Linux

> TODO

#### Windows

> TODO?