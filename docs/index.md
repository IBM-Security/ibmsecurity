# IBMSecurity Documentation

## About ibmsecurity

This repository contains Python code to manage IBM Security Appliances using their respective REST APIs.
ISAM appliance has the most mature code.

Code for ISDS appliance is under development.

Code for ISVG appliance is brand new (tested with 10.0.1.0 and higher only).

## Example Code

A sample `testisam.py` and `testisds.py` is provided. Provide details of your appliance and a user/password to authenticate.
Then call the functions needed. Run the code like you would any other Python script.

e.g.: `python testisam.py`

Note: the code requires PyYAML (for printing output in YAML) and importlib (dynamically load all packages) packages to work.

### Generic test script

For simple tests, a modified version is provided that takes the username, password, hostname, method and options as arguments, with the option to perform a commit or not.
This makes sense for simple tests but for pytest or unittests, this is not useful.

This avoids having to store credentials in a script and allows easier repeat of tests.

Example:

~~~~
python testisam_cmd.py --hostname 192.168.1.1 --method "ibmsecurity.isam.web.iag.export.features.get" --commit
~~~~
