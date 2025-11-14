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
