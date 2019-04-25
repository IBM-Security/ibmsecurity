import logging
import os.path

logger = logging.getLogger(__name__)


def get_all(isamAppliance, kdb_id, check_mode=False, force=False):
    """
    Retrieving certificate request names and details in a certificate database
    """
    return isamAppliance.invoke_get("Retrieving certificate request names and details in a certificate database",
                                    "/isam/ssl_certificates/{0}/cert_request".format(kdb_id))


def get(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Retrieving a certificate request from a certificate database
    """
    return isamAppliance.invoke_get("Retrieving a certificate request from a certificate database",
                                    "/isam/ssl_certificates/{0}/cert_request/{1}".format(kdb_id, cert_id))


def add(isamAppliance, kdb_id, label, dn, size='1024', check_mode=False, force=False):
    """
    Creating a certificate request in a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, label) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Creating a certificate request in a certificate database",
                "/isam/ssl_certificates/{0}/cert_request".format(kdb_id),
                {
                    "label": label,
                    "dn": dn,
                    'size': size
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Deleting a certificate request from a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, cert_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a certificate request from a certificate database",
                "/isam/ssl_certificates/{0}/cert_request/{1}".format(kdb_id, cert_id))

    return isamAppliance.create_return_object()


def export_cert(isamAppliance, kdb_id, cert_id, filename, check_mode=False, force=False):
    """
    Exporting a certificate request from a certificate database
    """
    if force is True or (_check(isamAppliance, kdb_id, cert_id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Exporting a certificate request from a certificate database",
                "/isam/ssl_certificates/{0}/cert_request/{1}?export".format(kdb_id, cert_id),
                filename)

    return isamAppliance.create_return_object()


def _check(isamAppliance, kdb_id, cert_id):
    """
    Check if personal certificate already exists in certificate database
    """
    ret_obj = get_all(isamAppliance, kdb_id)

    for certdb in ret_obj['data']:
        if certdb['id'] == cert_id:
            return True

    return False


def compare(isamAppliance1, isamAppliance2, kdb_id):
    """
    Compare signer certificates in certificate database between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, kdb_id)
    ret_obj2 = get_all(isamAppliance2, kdb_id)

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
