---
# Manual change log

## Build & Deploy

- move to pyproject.toml for building 

## 2023.4.25.0

- fix: add id parameter to ibmsecurity/isam/aac/fido2/relying_parties.py (#377)
- fix: add __init__.py in ibmsecurity/isvg sub folders (#380)

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

## 2023.8.22.0

- fix: admin.py (#356)
- fix: priority junction option (#359)