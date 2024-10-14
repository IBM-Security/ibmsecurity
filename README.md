# IBM Sample Code

This repository contains Python code to manage IBM Security Appliances using their respective REST APIs.
ISAM appliance has the most mature code.

Code for ISDS appliance is under development.

Code for ISVG appliance is brand new (tested with 10.0.1.0 and higher only).

## Requirements

Python v3.7 and above is required for this package.

The following Python Packages are required:
1. requests - for making REST API calls
2. PyYAML - for the sample code to work
3. jmespath - is required for sample code

The following Python Packages are optional:
1. cryptography - to perform action on certificates (used for idempotency in management_ssl_certificate)
2. python-dateutil - date utilities (used for idempotency in management_ssl_certificate)

Appliances need to have an ip address defined for their LMI. This may mean that appliances have had their initial setup
done with license acceptance.

## TLS verification enabled (v2024.4.5)

These changes are backwards compatible. We default to not verifying but always display a notice:

````markdown
Certificate verification has been disabled. Python is NOT verifying the SSL
certificate of the host appliance and InsecureRequestWarning messages are

being suppressed for the following host:

https://{0}:{1}

To use certificate verification:

1. When the certificate is trusted by your Python environment:
   Instantiate all instances of ISAMAppliance with verify=True or set
   the environment variable IBMSECLIB_VERIFY_CONNECTION=True.
2. When the certificate is not already trusted in your Python environment:
   Instantiate all instances of ISAMAppliance with the verify parameter
   set to the fully qualified path to a CA bundle.

See the following URL for more details:
https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
````
To remediate this cert validation warning, consider the instructions below:

Correct usage:

If you have the cert on disk somewhere,
instantiate the ISAMAppliance with:

    ISAMAppliance(…, verify=<path to cert>)

You can retrieve this from appliance using a command like:

    openssl s_client -connect ${HOSTNAME}:${PORT} </dev/null 2>/dev/null | openssl x509 -outform pem >  isamAppliance.pem

If the cert is already trusted in your Python environment,
instantiate the ISAMAppliance with:

    ISAMAppliance(…, verify=True)

or set the environment variable: `IBMSECLIB_VERIFY_CONNECTION=true`

If you receive errors about the hostname not matching the certificate:

This might look like:
````
<stack trace>

…

    raise CertificateError("hostname %r doesn't match %r" % (hostname, dnsnames[0]))

urllib3.util.ssl_match_hostname.CertificateError: hostname '192.168.42.111' doesn't match 'appliance.ibm.com'

````

Ensure the hostname used when instantiating your ISAMAppliance matches the Subject Alternative Name of the cert.

Check with:

    openssl x509 -in <cert-pem-file> -text

Example:

    $ openssl x509 -in /path/to/appliance.pem -text

Certificate:

    Data:
        Version: 3 (0x2)
        …
            X509v3 Subject Alternative Name:
                DNS:appliance.ibm.com
…

The following will generate errors:

    ISAMAppliance(host=”192.168.42.111”, lmi_port=443, verify=/path/to/appliance.pem)

as host does not match the Subject Alternative Name.
Instead, use:

    ISAMAppliance(host=”appliance.ibm.com”, lmi_port=443, verify=/path/to/appliance.pem)

## Versioning

This package uses a date for versioning. For example: "2017.03.18.0"

It is the date when the package is released with a sequence number at the end to handle when there are
multiple releases in one day (expected to be uncommon).

## Features

This python package provides the following features:
1. Easy to use - the details of making a REST call are handled within an appliance class
2. Intuitive layout of code package and naming maps to the GUI interface of appliance
3. Idempotency - functions that make updates will query the appliance to compare given data to see if a
changes is required before making the actual change.
4. Commit and Deploy steps are provided separately to allow for flexibility in invoking them
5. Standard logging is included - with the ability to set logging levels.
6. Parameters to function will use standard default values wherever possible.
7. A force option is provided to override idempotency.
8. Compare functions are provided - takes JSON output and provide a meaningful comparison.

## Example Code

A sample `testisam.py` and `testisds.py` is provided. Provide details of your appliance and a user/password to authenticate.
Then call the functions needed. Run the code like you would any other Python script.

e.g.: `python testisam.py`

Note: the code requires PyYAML (for printing output in YAML) and importlib (dynamically load all packages) packages to work.

### Function Data Return Format
~~~~
{
    rc:       <0 for success, higher for errors>
    changed:  <True or False>
    warnings: <List of strings with warnings - e.g. incompatible version>
    data:     <JSON data returned by appliance REST API that the function called>
}
~~~~

Note: it is preferred to return warnings rather than send back a non-zero rc.

### Generic test script

For simple tests, a modified version is provided that takes the username, password, hostname, method and options as arguments, with the option to perform a commit or not.
This makes sense for simple tests but for pytest or unittests, this is not useful.

This avoids having to store credentials in a script and allows easier repeat of tests.

Example:

~~~~
python testisam_cmd.py --hostname 192.168.1.1 --method "ibmsecurity.isam.web.iag.export.features.get" --commit
~~~~

## Organization of code

### Appliance Classes

An abstract `ibmappliance` class is extended to create a class for each appliance supported here.
Currently that is ISAM and ISDS appliances.

### User Classes

An abstract `User` is extended for each type of user needed. For ISAM that is an user for appliance access
 and another for authenticating to Web Runtime (Policy Server).

### Layout of ISAM packages

There are four primary ISAM packages - `base`, `web`, `aac` and `fed`. `web` contains all the components needed
for setting up the web functionality including embedded ldap, runtime and features that are activated as part of the
`wga` module. `aac` contains features activated as part of the `mga` module and `fed` that of `federation`. `base`
contains everything else - including `aac` and `fed` `runtime` and `Audit Configuration` (these are common to `aac` and `fed`
 and thus in `base`).

### Package and File Names

The package and file names were created with the following intention:
1. Maintain names that match what is in the GUI interface (LMI for ISAM appliance).
2. Each file should contain just one of each function type (see list below) - i.e. just one add().
3. Group related function - one of each type - in a file.
4. The URI for the REST API calls with a file will be the same and manage a "feature" of the appliance.

### Utilities

Contains miscellaneous functions that are generic and independent of any IBM Appliance, e.g. `json_compare()`.

## Function Types

### `get_all()`
This function typically will return all objects related to that feature.
### `get()`
This function returns the details of one particular object.
### `set()`
This function will determine if the object to be manipulated exists, if not then it calls add() otherwise it will call update().
In cases where there is no update() then it will compare to see if there is a difference between existing value on the appliance
to that being set via the function - if different then it `delete()`'s the object before calling add().
### `add()`
Check and see if the object already exists - if so then skip, otherwise add it.
### `update()`
Check and see if the object already exists - if so then check if update is needed before making a change, otherwise do nothing.
### `delete()`
Check and see if the object already exists - if so then delete, otherwise do nothing.
### `import_<>()`
"import" is a reserved word, so there is a suffix to indicate what to import (e.g. file or key). This will check if the object exists
before importing it.
### `export_<>()`
Export will check if exists before exporting it - when exporting to a file, and the file already exists it will not re-export.
Export
### `compare()`
Compare takes JSON output from the get_all() functions and compares it. It will strip data from JSON that
are unique to each appliance (e.g. UUID values). The deleted_keys value returned lists the JSON keys that were deleted before comparison.

## Function Parameters

### Appliance object
Create an appliance object and pass it to the function. Appliance and the User object needed are classes to allow for
future extensions like authentication using certificate instead of username/password.
### `check_mode`
This defaults to False, pass True to return and not make a change. The "changed" flag will be set to True if changes are detected.
### `force`
This defaults to False, pass True to override the idempotency logic.
### Other Parameters
The other parameters will match the REST API documentation verbatim. The intention was to reference the REST API documentation
and not have to repeat it. Please reference REST API documentation for details.

## Adding and Making Changes
Please raise an issue in github when a bug is discovered or there are REST APIs not covered by this package.
Provide detailed notes along with trace logs when a bug is reported.

# License

The contents of this repository are open-source under the Apache 2.0 licence.

```
Copyright 2017 International Business Machines

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
