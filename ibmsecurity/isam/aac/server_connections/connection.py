import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving a list of all server connections
    """
    return isamAppliance.invoke_get("Retrieving a list of all server connections",
                                    "/mga/server_connections/v1")


def test(isamAppliance, connectionType, hostName, port, userName, password, isSSL, keystorename=None, authKeyLabel=None,
         check_mode=False, force=False):
    """
    Test Connection
    """
    if check_mode is True:
        return isamAppliance.create_return_object()

    json_data = {
        'connectionType': connectionType,
        'hostName': hostName,
        'port': port,
        'userName': userName,
        'password': password,
        'isSSL': isSSL,
    }
    if keystorename is not None:
        json_data['keystorename'] = keystorename
    if authKeyLabel is not None:
        json_data['authKeyLabel'] = authKeyLabel

    ret_obj = isamAppliance.invoke_post("Test Connection", "/iam/access/v8/testconnection", json_data)

    # Assumed POST is for changes, this is just a test so indicate no change
    ret_obj['changed'] = False

    return ret_obj


def compare(isamAppliance1, isamAppliance2):
    """
    Compare all Connections between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    # Some connection types may not exist
    if ret_obj1.get('smtp') is not None:
        for obj in ret_obj1['data']['smtp']:
            del obj['uuid']
    if ret_obj1.get('jdbc') is not None:
        for obj in ret_obj1['data']['jdbc']:
            del obj['uuid']
    if ret_obj1.get('ldap') is not None:
        for obj in ret_obj1['data']['ldap']:
            del obj['uuid']
    if ret_obj2.get('smtp') is not None:
        for obj in ret_obj2['data']['smtp']:
            del obj['uuid']
    if ret_obj2.get('jdbc') is not None:
        for obj in ret_obj2['data']['jdbc']:
            del obj['uuid']
    if ret_obj2.get('ldap') is not None:
        for obj in ret_obj2['data']['ldap']:
            del obj['uuid']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['uuid'])
