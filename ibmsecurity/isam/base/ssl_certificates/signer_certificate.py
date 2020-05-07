import logging
import os.path
from ibmsecurity.utilities.tools import files_same, get_random_temp_dir
import shutil

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


def load(isamAppliance, kdb_id, label, server, port, check_remote=False, check_mode=False, force=False):
    """
    Load a certificate from a server
    
    check_remote controls if ansible should check remote certificate by retrieving it or simply by 
    checking for existence of the label in the kdb
    """
    if check_remote:
      logger.debug("Compare remote certificate with the one on the appliance. Use check_remote=False to switch to simple label checking.")
      tmp_check = _check_load(isamAppliance, kdb_id, label, server, port)
    else:
      logger.debug("Check for existence of the label in the kdb. Use check_remote=True to switch to advanced remote certificate with appliance certificate checking.")
      tmp_check = _check(isamAppliance, kdb_id, label)
    
    if force is True or tmp_check is False:
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


def _check_expired(notafter_epoch):
    """
    Can be used to check for expired certs
    Returns True if expired, False otherwise
    """
    import time
    epoch_time = int(time.time())
    cert_epoch = int(notafter_epoch)
    return cert_epoch < epoch_time


def _check_load(isamAppliance, kdb_id, label, server, port):
    """
    Checks if certificate to be loaded on the Appliance exists and if so, whether it is different from
    the one on the remote host.

    If the certificate exists on the Appliance, but has a different label,
    we return True, so that load() takes no action.

    If the requested label matches an existing label on the appliance,
    but the certs are different, check to see if cert is expired.  If so, replace cert.
    If not, do not replace.
    """
    import ssl
    remote_cert_pem = ssl.get_server_certificate((server, port))

    # Look for remote_cert_pem on in the signer certs on the appliance
    ret_obj = get_all(isamAppliance, kdb_id)
    for cert_data in ret_obj['data']:
        cert_id = cert_data['id']
        cert_pem = get(isamAppliance, kdb_id, cert_id)['data']['contents']
        if cert_id == label:  # label exists on appliance already
            logger.debug("Comparing certificates: appliance[{0}] remote[{1}].".format(cert_pem,remote_cert_pem))
            if cert_pem == remote_cert_pem:  # certificate data is the same
                logger.debug("The certificate already exits on the appliance with the same label name and same content.")
                return True  # both the labels and certificates match
            else:
                # Labels match, but the certs are different, so we need to update it.
                # However, you cannot load a cert with the same label name onto the appliance, since you get
                #   CTGSK2021W A duplicate certificate already exists in the database.
                # We delete the cert from the appliance and return False to the load() function,
                # so that we can load the new one
                ret_obj = delete(isamAppliance, kdb_id, cert_id)
                logger.debug("Labels match, but the certs are different, so we need to update it.")
                return False
        else:
            if cert_pem == remote_cert_pem:  # cert on the appliance, but with a different name
                logger.info(
                    "The certifcate is already on the appliance, but it has a different label name. "
                    "The existing label name is {label} and requested label name is {cert_id}".format(
                        label=label, cert_id=cert_id))
                return True
    return False


def delete(isamAppliance, kdb_id, cert_id, check_mode=False, force=False):
    """
    Deleting a signer certificate from a certificate database
    """
    if force is True or _check(isamAppliance, kdb_id, cert_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            try:
                # Assume Python3 and import package
                from urllib.parse import quote
            except ImportError:
                # Now try to import Python2 package
                from urllib import quote

            # URL being encoded primarily to handle spaces and other special characers in them
            f_uri = "/isam/ssl_certificates/{0}/signer_cert/{1}".format(kdb_id, cert_id)
            full_uri = quote(f_uri)
            return isamAppliance.invoke_delete(
                "Deleting a signer certificate from a certificate database", full_uri)

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
    tmpdir = get_random_temp_dir()
    orig_filename = '%s.cer' % cert_id
    tmp_original_file = os.path.join(tmpdir, os.path.basename(orig_filename))
    if _check(isamAppliance, kdb_id, cert_id):
        export_cert(isamAppliance, kdb_id, cert_id, tmp_original_file, check_mode=False, force=True)
        logger.debug("file already exists on appliance")
        if files_same(tmp_original_file, filename):
            logger.debug("files are the same, so we don't want to do anything")
            shutil.rmtree(tmpdir)
            return False
        else:
            logger.debug("files are different, so we delete existing file in preparation for import")
            delete(isamAppliance, kdb_id, cert_id, check_mode=check_mode, force=True)
            shutil.rmtree(tmpdir)
            return True
    else:
        logger.debug("file does not exist on appliance, so we'll want to import")
        shutil.rmtree(tmpdir)
        return True


def compare(isamAppliance1, isamAppliance2, kdb_id):
    """
    Compare signer certificates in certificate database between two appliances
    """
    ret_obj1 = get_all(isamAppliance1, kdb_id)
    ret_obj2 = get_all(isamAppliance2, kdb_id)

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
