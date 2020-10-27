import logging
import os.path
import ibmsecurity.utilities.tools
from io import open

logger = logging.getLogger(__name__)


def get_all(isamAppliance, kdb_id, check_mode=False, force=False):
    """
    Retrieving personal certificate names and details in a certificate database
    """
    return isamAppliance.invoke_get("Retrieving personal certificate names and details in a certificate database",
                                    "/isam/ssl_certificates/{0}/personal_cert".format(kdb_id))


def get(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Retrieving a personal certificate from a certificate database
    """
    return isamAppliance.invoke_get("Retrieving a personal certificate from a certificate database",
                                    "/isam/ssl_certificates/{0}/personal_cert/{1}".format(kdb_id, cert_id))


def generate(isamAppliance, kdb_id, label, dn, expire='365', default='no', size='1024', signature_algorithm='',
             check_mode=False, force=False):
    """
    Generating a self-signed personal certificate in a certificate database
    """

    warnings = []

    if signature_algorithm is not None:
        if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "9.0.2.0") < 0:
            warnings.append("Appliance at version: {0}, signature_algorithm is not supported. Needs 9.0.2.0 or higher. "
                            "Ignoring signature_algorithm for this call".format(isamAppliance.facts["version"]))
            json_obj = {
                "operation": 'generate',
                "label": label,
                "dn": dn,
                "expire": expire,
                'default': default,
                'size': size
            }
        else:
            json_obj = {
                "operation": 'generate',
                "label": label,
                "dn": dn,
                "expire": expire,
                'default': default,
                'size': size,
                'signature_algorithm': signature_algorithm
            }

    if force is True or _check(isamAppliance, kdb_id, label) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Generating a self-signed personal certificate in a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert".format(kdb_id),
                json_obj,
                warnings=warnings
            )

    return isamAppliance.create_return_object(changed=False, warnings=warnings)


def set(isamAppliance, kdb_id, cert_id, default='no', check_mode=False, force=False):
    """
    Setting a personal certificate as default in a certificate database
    """
    if force is True or _check_default(isamAppliance, kdb_id, cert_id, default) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Setting a personal certificate as default in a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert/{1}".format(kdb_id, cert_id),
                {
                    'default': default
                })

    return isamAppliance.create_return_object()


def receive(isamAppliance, kdb_id, label, cert, default='no', check_mode=False, force=False):
    """
    Receiving a personal certificate into a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, label) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Receiving a personal certificate into a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert".format(kdb_id),
                [
                    {
                        'file_formfield': 'cert',
                        'filename': cert,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    'default': default,
                    'operation': 'receive'
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Deleting a personal certificate from a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, cert_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a personal certificate from a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert/{1}".format(kdb_id, cert_id))

    return isamAppliance.create_return_object()


def export_cert(isamAppliance, kdb_id, cert_id, filename, check_mode=False, force=False):
    """
    Exporting a personal certificate from a certificate database
    """
    if force is True or (_check(isamAppliance, kdb_id, cert_id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Exporting a personal certificate from a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert/{1}?export".format(kdb_id, cert_id),
                filename)

    return isamAppliance.create_return_object()


def import_cert(isamAppliance, kdb_id, label, cert, password, check_mode=False, force=False):
    """
    Importing a personal certificate into a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, label) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a personal certificate into a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert".format(kdb_id),
                [
                    {
                        'file_formfield': 'cert',
                        'filename': cert,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {
                    'password': password,
                    'operation': 'import'
                })

    return isamAppliance.create_return_object()


def extract_cert(isamAppliance, kdb_id, cert_id, password, filename, check_mode=False, force=False):
    """
    Extracting a personal certificate from a certificate database
    """
    if force is True or (_check(isamAppliance, kdb_id, cert_id) is True and os.path.exists(filename) is False):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = isamAppliance.invoke_post(
                "Extracting a personal certificate from a certificate database",
                "/isam/ssl_certificates/{0}/personal_cert/{1}".format(kdb_id, cert_id),
                {
                    'operation': 'extract',
                    'type': 'pkcs12',
                    'password': password
                })
            extracted_file = open(filename, 'wb')
            extracted_file.write(ret_obj['data'])
            extracted_file.close()

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


def _check_default(isamAppliance, kdb_id, cert_id, default):
    """
    Check if personal certificate already exists in certificate database
    """
    ret_obj = get_all(isamAppliance, kdb_id)

    for certdb in ret_obj['data']:
        if certdb['id'] == cert_id:
            if (certdb['default'].lower() == 'true' and default.lower() == 'no') or (
                    certdb['default'].lower() == 'false' and default.lower() == 'yes'):
                return True

    return False


def compare(isamAppliance1, isamAppliance2, kdb_id):
    """
    Compare signer certificates in certificate database between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, kdb_id)
    ret_obj2 = get_all(isamAppliance2, kdb_id)

    for cert in ret_obj1['data']:
        del cert['issuer']
        del cert['notafter']
        del cert['notafter_epoch']
        del cert['notbefore']
        del cert['notbefore_epoch']
        del cert['serial_number']
        del cert['sha1_fingerprint']
        del cert['subject']
    for cert in ret_obj2['data']:
        del cert['issuer']
        del cert['notafter']
        del cert['notafter_epoch']
        del cert['notbefore']
        del cert['notbefore_epoch']
        del cert['serial_number']
        del cert['sha1_fingerprint']
        del cert['subject']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2,
                                                    deleted_keys=['issuer', 'notafter', 'notafter_epoch', 'notbefore',
                                                                  'notbefore_epoch', 'serial_number',
                                                                  'sha1_fingerprint', 'subject'])
