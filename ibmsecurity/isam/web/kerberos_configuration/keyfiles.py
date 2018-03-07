import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/kerberos/keytab"
requires_modules = ['wga']
requires_version = None


def get(isamAppliance, recursive='yes', includeValues='yes', addParent='yes', check_mode=False, force=False):
    """
    Retrieve Kerberos: Keytab
    """
    return isamAppliance.invoke_get("Retrieve Kerberos: Keytab", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def compare(isamAppliance1, isamAppliance2):
    """
    Compare kerberos keytab files between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
def add (isamAppliance, keytab_file, force=False):
    """
    add keytab file
    """     
    return isamAppliance.invoke_post_files("Add Kerberos: Keytab", uri,
            [
                {
                    'file_formfield': 'keytab_file',
                    'filename': keytab_file,
                    'mimetype': 'application/octet-stream'
                }
            ],{})
