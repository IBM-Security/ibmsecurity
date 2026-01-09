# Contributing

Review the following guidelines for submitting questions, issues, or changes to this repository. One of the most impactful changes would be examples and documentation.

## Setup

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
# Add tests under `test/`
$ tox run -e lint,py
$ git add your new files
$ git commit -v
$ git push origin your-branch-name
```

You will then be able to create a pull request from your commit.

## Setup

### Local appliance

There is no mock code for testing against, unfortunately.
So you need a running IBM Verify Access/IBM Identity Verify Access appliance or container to be able to run the tests.

### Env

Create a .env file in the root directory of the project, with the details to connect to your IVIA appliance, for instance :

````properties
IVIA_ADMIN=admin@local
IVIA_PW=admin
IVIA_HOST=<ip address of lmi>
# IVIA_PORT = 80
IVIA_SECMASTER=sec_master
IVIA_SECMASTER_PW=<password for sec_master>
````

Optionally, you can configure a proxy (http_proxy or https_proxy)

````properties
IVIA_HTTPS_PROXY=http://localhost:3128
IVIA_HTTP_PROXY=http://127.0.0.1:3128
````

##  Coding Style

Automated tests will be run against all PRs, to run checks locally before
pushing commits, use [tox](https://tox.wiki/en/latest/).

Fix any issues

## Issues and Questions

If you encounter an issue, have a question or want to suggest an enhancement, you are welcome to submit a [request](/issues).
Before that, please search for similar issues. It's possible somebody has encountered this issue already.

## Pull Requests

If you want to contribute to the repository, here's a quick guide:

1. Fork the repository
2. Develop and test your code changes:
    * Follow the coding style as documented above.
    * Please add one or more tests to validate your changes.
3. Make sure everything builds/tests cleanly.
4. Commit your changes. Add a descriptive prefix to commits. The list allowed is as below:
   - `feat` for features
   - `fix` for bug fixes
   - `revert` for reversing a change
   - `docs` for documentation and examples
   - `style` for formatting and other related changes
   - `refactor` is self-explanatory
   - `test` for test case changes
   - `build` for build changes
   - `autogen` for any auto-generated code or documentation
   - `security` for any security fixes and enhancements
   - `ci` for changes to continuous integration
   - `chore` is self-explanatory
5. Push to your fork and submit a pull request to the `main` branch. Include the tests executed in the pull request.

### License header in source files

Each source file must include a license header for the Apache
Software License 2.0. Using the SPDX format is the simplest approach.
e.g.

```
/*
Copyright IBM Corp. All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
*/
```

### Sign your work

In accordance to the approach used by the Linux® Kernel [community](https://elinux.org/Developer_Certificate_Of_Origin) and described in the [Developer's Certificate of Origin 1.1 (DCO)](https://github.com/hyperledger/fabric/blob/master/docs/source/DCO1.1.txt), we request that each contributor signs off their change by adding a `Signed-off-by` line to each commit message.

Here is an example Signed-off-by line, which indicates that the submitter accepts the DCO:

```
Signed-off-by: John Doe <john.doe@example.com>
```

You can include this automatically when you commit a change to your
local git repository using the following command:

```
git commit -s
```

## Additional Resources

* [General GitHub documentation](https://help.github.com/)
* [GitHub pull request documentation](https://help.github.com/send-pull-requests/)
