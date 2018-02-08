import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/test"
requires_modules = ['wga']
requires_version = None


def test(isamAppliance, name, password, check_mode=False, force=False):
    """
    Verify Kerberos Authentication of the Web Server Principal
    """
    # Note: Check mode and force are not relevant for running a test
    ret_obj = isamAppliance.invoke_post(
        "Verify Kerberos Authentication of the Web Server Principal", uri,
        {
            "name": name,
            "password": password
        }, requires_modules=requires_modules, requires_version=requires_version)

    # Test will not cause a change
    if ret_obj['changed'] == True:
        ret_obj['changed'] = False

    return ret_obj
