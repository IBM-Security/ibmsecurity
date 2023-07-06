---
# Manual change log

## Unreleased

- feature: new acl api (v10.0.6)
- feature: ssh keys admin and sysaccount (v10.0.6)
- feature: waf and waf_config api (v10.0.5)
- feature: ivg configuration (v10.0.2)
- feature: fido metadata services (v10.0.4)

## 2023.4.26.0

- fix: remove pyOpenSSL dependency in management_ssl_certificate.py (#366)
- fix: setuptools does not support pip -e - previous build is wrong (#383)

## 2023.4.25.0

- fix: add id parameter to ibmsecurity/isam/aac/fido2/relying_parties.py (#377)
- fix: add __init__.py in ibmsecurity/isvg sub folders (#380)

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