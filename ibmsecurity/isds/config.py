import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isdsAppliance, check_mode=False, force=False):
    """
    Get current configured server type
    """
    return isdsAppliance.invoke_get("Retrieving Server Type", "/servertype_object")


def set(isdsAppliance, serverType="RDBM", check_mode=False, force=False):
    """
    Update Directory Server "server type"
    """
    if force is True or _check(isdsAppliance, serverType) is False:
        if check_mode is True:
            return isdsAppliance.create_return_object(changed=True)
        else:
            return isdsAppliance.invoke_post(
                "Setting Server Type",
                "/servertype_object",
                {
                    "serverType": serverType
                })

    return isdsAppliance.create_return_object()


def _check(isdsAppliance, serverType):
    """
    Check if configured server type already set to specificed serverType
          Values           serverType
      ==================   ==========
      "Directory Server"     RDBM
      "Directory Proxy"      PROXY
      "Virtual Directory"    VD
    """
    ret_obj = get(isdsAppliance)

    if ret_obj['data']['DirectoryServerType'] == 'Directory Server':
        if serverType == 'RDBM':
            return True
        else:
            return False
    elif ret_obj['data']['DirectoryServerType'] == 'Directory Proxy':
        if serverType == 'PROXY':
            return True
        else:
            return False
    elif ret_obj['data']['DirectoryServerType'] == 'Virtual Directory':
        if serverType == 'VD':
            return True
        else:
            return False
    else:
        return True


def compare(isdsAppliance1, isdsAppliance2):
    """
    Compare server type values between two appliances
    """
    ret_obj1 = get(isdsAppliance1)
    ret_obj2 = get(isdsAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2)
