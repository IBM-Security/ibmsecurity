# Manual change log

## Latest

- fix: certificate_databases : python syntax (indentation)
- fix: policy_attachments.py : idempotency and handle applications correctly
-

## 2025.6.3.0

- feature: base/management_authentication.py - type federation
- build: test setup
- feature: web/reverse_proxy/oauth_configuration.py - add new parameters in 10.0.8
- feature: web/reverse_proxy/oauth2_configuration.py - OAuth2 IBM Security Verify OIDC Provider configuration (new in 10.0.4)
- feature: aac/server_connections/sms.py - SMS Server Connection (new in 10.0.8)
- fix: base/admin_ssh_keys.py - Ignore error when same ssh key exists under different name
- pylint: change format() to f-strings
- feature: base/tracing.py - Get tracing configuration (new in 10.0.8)
- fix: add ignore_errors to cli.py - incoming change
- feature: add publish parameter (for use in containers) (new in 10.0.8)
- feature: new function in tools `json_equals`
- feature: tuning_parameters.py - set multiple runtime parameters in 1 call
- fix: new parameter includeIssInAuthResp for oidc definitions (new in 10.0.8)
- feature: export a kerberos keytab file (new in 10.0.8)
- feature: get all audit configurations (new in 10.0.8)
- feature: update network certificate database (WIP)

## 2025.3.28.0

- fix: base/extensions.py - improve idempotency #441
- fix: base/container_ext/repo.py - user and secret are not required (although documentation states they are)
- feature: base/admin.py - improve idempotency, support for new parameters in IVIA 11
- feature: base/ssl_certificates/personal_certificate.py - support label parameter in IVIA 11
- PEP 639: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license

## 2025.3.14.0

- build: add pylint configuration
- fix: fed/federations.py set_file

## 2024.12.6.0

- deprecated: set personal certificate as default
- deprecated: `base/audit_configuration.py`.  Use `base/audit/configuration.py` instead
- feature: base/audit/configuration.py added
- feature: base/audit/components.py added

## 2024.10.11.0

- fix: corrections in test script
- fix: base/extensions.py
- feature: base/container functions (image,volume,metadata,repo,container)
- build: add pre-commit configuration

## 2024.9.30.0

- features: enhancements on pip and personal certificates (#430)
- fix: cache in policy_attachments (#432)

## 2024.6.24.0

- fix: isdsappliance.py missing cert variable initialization

## 2024.6.10.0

- fix: base/cluster/configuration.py - idempotency
- feature: fed/federations.py - wsfed
- fix: web/api_access_control/utilities - credential check update
- fix: documentation
- fix: web/reverse_proxy/junctions - add priority for 10.0.2 if not present
- fix: isdsappliance.py missing cert variable initialization

## 2024.6.7.0

- fix: uninitialized 'warnings' variable in junctions_server.py (#419)
- fix: add preserve_label in signer_certificates (from kg)
- fix: added condition check in aac/attributes.py (#422)
- feature: forward python requests connection error messages to ibmerror (#423)

## 2024.4.5.0

- fix: update stanza.py (#414)
- fix: remove curly braces from get_config_data function (#417)
- security fix: enable verify ssl (V-94) (#416)
- security fix: show a warning about not verifying tls for connections to the LMI (V-93) (#416)
- security fix: remove hardcoded usernames and passwords (V-95) (#416)
- security fix: uninitialized variables (V-96) (#416)
- documentation: update readme with info on how to handle the tls verification

## 2024.2.26.0

- feature: set_all function for reverse proxy junctions
- fix: ignore_if_down cannot be set to False (#410)
- fix: resolve issues created in reverse proxy junctions (set() function)
- refactor: change email address for author

## 2023.11.10.0

- fix: available_updates.py state is no longer available in 10.0.5 or higher, and too many variables in post request
- fix: ssh_keys api added proper idempotency (#395)
- feature: json input and output for aac authentication policies (#399)
- feature: json input and output for aac access control policies (#400)
- feature: add use_json flag in audit configuration

## 2023.7.6.0

- feature: new acl api (v10.0.6)
- feature: ssh keys admin and sysaccount (v10.0.6)
- feature: waf and waf_config api (v10.0.5)
- feature: ivg configuration (v10.0.2)
- feature: fido metadata services (v10.0.4)

## 2023.7.4.0

- fix: management_ssl_certificate.py warnings cannot be None
- known_issue: management_ssl_certificate.py idempotency checks do not always work (issuer contains oid for email=)

## 2023.6.30.0

- fix: state parameter no longer exists in v10.0.5 in available_updates.py (#385)
- critical change: case_sensitive_url -> case_insensitive_url in v10.0.6 (#386)

## 2023.4.26.0

- fix: remove pyOpenSSL dependency in management_ssl_certificate.py (#366)
- fix: setuptools does not support pip -e - previous build is wrong (#383)

## 2023.4.25.0

- fix: add id parameter to ibmsecurity/isam/aac/fido2/relying_parties.py (#377)
- fix: add `__init__.py` in ibmsecurity/isvg sub folders (#380)

### Build & Deploy

- move to pyproject.toml for building

## 2023.4.21.0

- new: Add domain parameter to delete method. (#374)
- fix: indentation in add method. (#373)
- new: Add get_all method to ibmsecurity/isam/web/authorization_server/cleanup.py (#375)
- new: Add http transform from content (#319)
- fix: syntax in test_isam.py (no pull request)

## 2023.3.10.0

- new: testisam_cmd.py test script (accepts parameters)
- update: add variable local_interface_only to web/runtime/process.py (new in v10.0.4)
- new: web/iag/export function for v10.0.4
- update: add detailed option to get_all() in web/reverse_proxy/junctions.py (new in v10.0.4)
- update: add parameter ignore_if_down to federated_directories (new in v10.0.4)
- feature: support for ISAM 10 (#364)
- fix: typo in api_access_control resources (#371)
- feature: ISVG appliance (#364)
- fix: idempotency for policies in api_access_control (#368)
- fix: scim merge back from pypi (#332)
- feature: Add scim custom schema extension api (#363)
- feature: Extension enhancements (#369)
- feature: close temp file before delete in runtime_template root (#370)

## 2022.8.22.0

- fix: admin.py (#356)
- fix: priority junction option (#359)
