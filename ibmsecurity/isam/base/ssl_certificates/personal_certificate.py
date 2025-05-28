import logging
import os.path
import ibmsecurity.utilities.tools
from io import open

logger = logging.getLogger(__name__)


def get_all(isamAppliance, kdb_id, check_mode=False, force=False):
    """
    Retrieving personal certificate names and details in a certificate database
    """
    return isamAppliance.invoke_get(
        "Retrieving personal certificate names and details in a certificate database",
        f"/isam/ssl_certificates/{kdb_id}/personal_cert"
    )


def get(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Retrieving a personal certificate from a certificate database
    """
    return isamAppliance.invoke_get(
        "Retrieving a personal certificate from a certificate database",
        f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}"
    )


def generate(isamAppliance, kdb_id, label, dn, expire='365', default='no', size='2048', signature_algorithm='',
             check_mode=False, force=False):
    """
    Generating a self-signed personal certificate in a certificate database
    """
    warnings = []

    if signature_algorithm is not None:
        if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "9.0.2.0") < 0:
            warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, signature_algorithm is not supported. Needs 9.0.2.0 or higher. Ignoring signature_algorithm for this call")
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
                f"/isam/ssl_certificates/{kdb_id}/personal_cert",
                json_obj,
                warnings=warnings
            )

    return isamAppliance.create_return_object(changed=False, warnings=warnings)


def rename(isamAppliance, kdb_id, cert_id, new_id,
           check_mode=False, force=False):
    """
    Rename a personal certificate.  New in 10.0.7
    """
    warnings = []

    if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.7.0") < 0:
        warnings.append(
            f"Appliance is at version: {isamAppliance.facts['version']}. Renaming a certificate requires at least 10.0.7.0"
        )
    else:
        if force or (_check(isamAppliance, kdb_id, cert_id) and not _check(isamAppliance, kdb_id, new_id)):
            if check_mode:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Renaming a personal certificate as default in a certificate database",
                    f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}",
                    {
                        'new_id': new_id
                    })


def set(isamAppliance, kdb_id, cert_id, default='no', check_mode=False, force=False):
    """
    Setting a personal certificate as default in a certificate database

    Obsolete since 10.0.3
    """
    warnings = []

    if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.3.0") > 0:
        warnings.append(
            f"Appliance is at version: {isamAppliance.facts['version']}. Setting certificates as default is no longer supported."
        )
    else:
        if force or _check_default(isamAppliance, kdb_id, cert_id, default):
            if check_mode:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Setting a personal certificate as default in a certificate database",
                    f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}",
                    {
                        'default': default
                    })

    return isamAppliance.create_return_object(warnings=warnings)


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
                f"/isam/ssl_certificates/{kdb_id}/personal_cert",
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
    if force or _check(isamAppliance, kdb_id, cert_id):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a personal certificate from a certificate database",
                f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}")

    return isamAppliance.create_return_object()


def export_cert(isamAppliance, kdb_id, cert_id, filename, check_mode=False, force=False):
    """
    Exporting a personal certificate from a certificate database
    """
    if force is True or (_check(isamAppliance, kdb_id, cert_id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Exporting a personal certificate from a certificate database",
                f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}?export",
                filename)

    return isamAppliance.create_return_object()


def import_cert(isamAppliance, kdb_id, cert, label=None, password=None, check_mode=False, force=False):
    """
    Importing a personal certificate into a certificate database
    Remark: you can add a label, but it's only used for a half-hearted check if the certificate already exists for versions < 11
    """
    warnings = []
    if force or not _check(isamAppliance, kdb_id, label):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            iviaVersion = isamAppliance.facts['version']
            post_data = {
                'file_formfield': 'cert',
                'filename': cert,
                'mimetype': 'application/octet-stream'
            }
            json_data = {
                'operation': 'import'
            }
            if password is not None:
                json_data['password'] = password
            if label is not None:
                if ibmsecurity.utilities.tools.version_compare(iviaVersion, "10.0.9.0") < 0:
                    warnings.append(f"Appliance at version: {iviaVersion}, label: {label} is not supported. Needs 10.0.9 or higher. Ignoring.")
                else:
                    logger.debug(f"Adding label: {label}")
                    json_data['label'] = label
            logger.debug(f"Posting json data: {json_data}")
            return isamAppliance.invoke_post_files(
                "Importing a personal certificate into a certificate database",
                f"/isam/ssl_certificates/{kdb_id}/personal_cert",
                [
                    post_data
                ],
                json_data,
                warnings=warnings
            )

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
                f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}",
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
    if cert_id is None:
        logger.debug("No label passed, so return false")
        return False
    else:
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
