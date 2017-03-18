import logging
import os.path
from ibmsecurity.utilities.tools import files_same
import tempfile

logger = logging.getLogger(__name__)


def get_all(isamAppliance, kdb_id, check_mode=False, force=False):
    """
    Retrieving signer certificate names and details in a certificate database
    """
    return isamAppliance.invoke_get("Retrieving signer certificate names and details in a certificate database",
                                    "/isam/ssl_certificates/{0}/signer_cert".format(kdb_id))


def get(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Retrieving a signer certificate from a certificate database
    """
    return isamAppliance.invoke_get("Retrieving a signer certificate from a certificate database",
                                    "/isam/ssl_certificates/{0}/signer_cert/{1}".format(kdb_id, cert_id))


def load(isamAppliance, kdb_id, label, server, port, check_mode=False, force=False):
    """
    Load a certificate from a server
    """
    if force is True or _check(isamAppliance, kdb_id, label) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Load a certificate from a server",
                "/isam/ssl_certificates/{0}/signer_cert".format(kdb_id),
                {
                    "operation": 'load',
                    "label": label,
                    "server": server,
                    "port": port
                })

    return isamAppliance.create_return_object()


def delete(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Deleting a signer certificate from a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, cert_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a signer certificate from a certificate database",
                "/isam/ssl_certificates/{0}/signer_cert/{1}".format(kdb_id, cert_id))

    return isamAppliance.create_return_object()


def export_cert(isamAppliance, kdb_id, cert_id, filename, check_mode=False, force=False):
    """
    Exporting a signer certificate from a certificate database
    """
    import os.path

    if force is True or _check(isamAppliance, kdb_id, cert_id) is True:
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a certificate database",
                "/isam/ssl_certificates/{0}/signer_cert/{1}?export".format(kdb_id, cert_id),
                filename)

    return isamAppliance.create_return_object()


def import_cert(isamAppliance, kdb_id, cert, label, check_mode=False, force=False):
    """
    Importing a signer certificate into a certificate database
    """
    if force is True or _check_import(isamAppliance, kdb_id, label, cert, check_mode=check_mode):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Importing a signer certificate into a certificate database",
                "/isam/ssl_certificates/{0}/signer_cert".format(kdb_id),
                [
                    {
                        'file_formfield': 'cert',
                        'filename': cert,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {'label': label})

    return isamAppliance.create_return_object()


def _check(isamAppliance, kdb_id, cert_id):
    """
    Check if signer certificate already exists in certificate database
    """
    ret_obj = get_all(isamAppliance, kdb_id)

    for certdb in ret_obj['data']:
        if certdb['id'] == cert_id:
            return True

    return False


def _check_import(isamAppliance, kdb_id, cert_id, filename, check_mode=False):
    """
    Checks if certificate on the Appliance  exists and if so, whether it is different from
    the one stored in filename
    """
    tmpdir = tempfile.gettempdir()
    orig_filename = '%s.cer' % cert_id
    tmp_original_file = os.path.join(tmpdir, os.path.basename(orig_filename))
    if _check(isamAppliance, kdb_id, cert_id):
        export_cert(isamAppliance, kdb_id, cert_id, tmp_original_file, check_mode=False, force=True)
        logger.debug("file already exists on appliance")
        if files_same(tmp_original_file, filename):
            logger.debug("files are the same, so we don't want to do anything")
            return False
        else:
            logger.debug("files are different, so we delete existing file in preparation for import")
            delete(isamAppliance, kdb_id, cert_id, check_mode=check_mode, force=True)
            return True
    else:
        logger.debug("file does not exist on appliance, so we'll want to import")
        return True


def compare(isamAppliance1, isamAppliance2, kdb_id):
    """
    Compare signer certificates in certificate database between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, kdb_id)
    ret_obj2 = get_all(isamAppliance2, kdb_id)

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
