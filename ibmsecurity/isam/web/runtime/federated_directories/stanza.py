import logging
import ibmsecurity.utilities.tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the list of federated directories
    """
    return isamAppliance.invoke_get("Retrieving the list of federated directories",
                                    "/isam/runtime_components/federated_directories/v1")


def get(isamAppliance, id, check_mode=False, force=False):
    """
    Retrieving the details for a particular federated directory
    """
    return isamAppliance.invoke_get("Retrieving the details for a particular federated directory",
                                    "/isam/runtime_components/federated_directories/{0}/v1".format(id))


def set(isamAppliance, id, hostname, port, bind_dn, bind_pwd, suffix, use_ssl=False, client_cert_label=None,
        check_mode=False, force=False):
    if _exists(isamAppliance, id) is False:
        return add(isamAppliance, id=id, hostname=hostname, port=port, bind_dn=bind_dn, bind_pwd=bind_pwd,
                   suffix=suffix, use_ssl=use_ssl, client_cert_label=client_cert_label, check_mode=check_mode,
                   force=True)
    else:
        return update(isamAppliance, id=id, hostname=hostname, port=port, bind_dn=bind_dn, bind_pwd=bind_pwd,
                      suffix=suffix, use_ssl=use_ssl, client_cert_label=client_cert_label, check_mode=check_mode,
                      force=force)


def add(isamAppliance, id, hostname, port, bind_dn, bind_pwd, suffix, use_ssl=False, client_cert_label=None,
        check_mode=False, force=False):
    """
    Create a new federated directory
    """
    if (isinstance(suffix, basestring)):
        import ast
        suffix = ast.literal_eval(suffix)

    if force is True or _exists(isamAppliance, id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                'id': id,
                'hostname': hostname,
                'port': port,
                'bind_dn': bind_dn,
                'bind_pwd': bind_pwd,
                'use_ssl': use_ssl,
                'suffix': suffix
            }
            # Do not pass if there is no value - call fails otherwise
            if client_cert_label is not None:
                json_data['client_cert_label'] = client_cert_label
            return isamAppliance.invoke_post(
                "Create a new federated directory",
                "/isam/runtime_components/federated_directories/v1", json_data)

    return isamAppliance.create_return_object()


def update(isamAppliance, id, hostname, port, bind_dn, bind_pwd, suffix, use_ssl=False, client_cert_label=None,
           check_mode=False, force=False):
    """
    Update an existing federated directory
    """
    if force is True or (
            _exists(isamAppliance, id) is True and _check(isamAppliance, id, hostname, port, bind_dn, bind_pwd,
                                                          use_ssl, client_cert_label, suffix) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                'hostname': hostname,
                'port': port,
                'bind_dn': bind_dn,
                'bind_pwd': bind_pwd,
                'use_ssl': use_ssl,
                'suffix': suffix
            }
            # Do not pass if there is no value - call fails otherwise
            if client_cert_label is not None:
                json_data['client_cert_label'] = client_cert_label
            return isamAppliance.invoke_put(
                "Update an existing federated directory",
                "/isam/runtime_components/federated_directories/{0}/v1".format(id), json_data)

    return isamAppliance.create_return_object()


def delete(isamAppliance, id, check_mode=False, force=False):
    """
    Remove an existing federated directory
    """
    if force is True or _exists(isamAppliance, id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Remove an existing federated directory",
                "/isam/runtime_components/federated_directories/{0}/v1".format(id))

    return isamAppliance.create_return_object()


def _exists(isamAppliance, id):
    """
    Check if federated directory exists

    :param isamAppliance:
    :param id:
    :return:
    """
    exists = False
    ret_obj = get_all(isamAppliance)

    for snmp in ret_obj['data']:
        if snmp['id'] == id:
            exists = True
            break

    return exists


def _check(isamAppliance, id, hostname, port, bind_dn, bind_pwd, use_ssl, client_cert_label, suffix):
    """
    Check if parameters match given federated directory

    Note: This does not check bind_pwd
    """

    set_value = {
        'id': id,
        'hostname': hostname,
        'port': str(port),
        'bind_dn': bind_dn,
        'use_ssl': use_ssl,
        'client_cert_label': client_cert_label,
        'suffix': suffix
    }
    if use_ssl is False:
        del set_value['client_cert_label']

    set_value = ibmsecurity.utilities.tools.json_sort(set_value)

    ret_obj = get(isamAppliance, id)
    if ibmsecurity.utilities.tools.json_sort(ret_obj['data']) == set_value:
        return True
    else:
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare federated directory stanze entries between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
