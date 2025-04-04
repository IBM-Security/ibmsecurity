# Contributing to ibmsecurity WIP

To contribute to ibmsecurity, please use pull requests on a branch of your own
fork.

After [creating your fork on GitHub], you can do:

```shell-session
$ git clone --recursive git@github.com:your-name/ibmsecurity
$ cd ibmsecurity
$ # Recommended: Initialize and activate a Python virtual environment
$ pip install --upgrade pip
$ pip install -e '.[test]'       # Install testing dependencies
$ tox run -e lint
$ git checkout -b your-branch-name
# DO SOME CODING HERE
$ tox run -e lint
$ git add your new files
$ git commit -v
$ git push origin your-branch-name
```

You will then be able to create a pull request from your commit.

Feel free to raise issues in the repo if you feel unable to contribute a code
fix.

## Setup

### Local appliance

There is no mock code for testing, unfortunately.
So you need a running IBM Verify Access/IBM Identity Verify Access appliance or container to be able to run the tests.

### Env

Create a .env file in the root directory of the project, with the details to connect to your IVIA appliance, for instance :

````properties
IVIA_ADMIN=admin@local
IVIA_PW=admin
IVIA_HOST=<ip address of lmi>
# IVIA_PORT = 80
````

## Standards

Automated tests will be run against all PRs, to run checks locally before
pushing commits, just use [tox](https://tox.wiki/en/latest/).

## Talk to us


## Code of Conduct



## Module dependency graph



## Documentation changes

To build the docs, run `tox -e docs`. At the end of the build, you will see the
local location of your built docs.
