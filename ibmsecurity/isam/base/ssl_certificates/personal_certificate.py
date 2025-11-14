import logging
import os.path

import ibmsecurity.utilities.tools
from ibmsecurity.utilities.tools import json_equals
from io import open

logger = logging.getLogger(__name__)

performCertCheck = True
try:
    from dateutil import parser
    #pip install python-dateutil
    import cryptography.hazmat.primitives.serialization.pkcs12
    import cryptography.x509
    from cryptography.x509 import Name, NameAttribute, NameOID
    from cryptography.x509.oid import ObjectIdentifier
    # pip install cryptography
except:
    performCertCheck = False


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
    certexists, certsubject = _check(isamAppliance, kdb_id, label=label)
    if force or not certexists:
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
        certexists, certsubject = _check(isamAppliance, kdb_id, label=cert_id)
        newcertexists, nse = _check(isamAppliance, kdb_id, label=new_id)
        if force or (certexists and not newcertexists):
            if check_mode:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Renaming a personal certificate in a certificate database",
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
    certexists, certsubject = _check(isamAppliance, kdb_id, label=label)
    if force or not certexists:
        if check_mode:
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


def delete(isamAppliance, kdb_id, cert_id, check_mode=False, force=False, ignore_error=False):
    """
    Deleting a personal certificate from a certificate database
    """
    certexists, certsubject = _check(isamAppliance, kdb_id, label=cert_id)
    if force or certexists:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a personal certificate from a certificate database",
                f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}",
                ignore_error=ignore_error
            )

    return isamAppliance.create_return_object()


def export_cert(isamAppliance, kdb_id, cert_id, filename, check_mode=False, force=False):
    """
    Exporting a personal certificate from a certificate database
    """
    certexists, certsubject = _check(isamAppliance, kdb_id, label=cert_id)
    if force or (not certexists and not os.path.exists(filename)):
        if not check_mode:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Exporting a personal certificate from a certificate database",
                f"/isam/ssl_certificates/{kdb_id}/personal_cert/{cert_id}?export",
                filename)

    return isamAppliance.create_return_object()


def import_cert(isamAppliance, kdb_id, cert, label=None, password=None, check_mode=False, force=False):
    """
    Importing a personal certificate into a certificate database
    Remark: you can add a label, but it's only used for a half-hearted check if the certificate already exists for versions < 11
            so it's NOT used to actually create the certificate !
    """
    warnings = []
    # certexists means that the SAME certificate exists
    certexists, certsubject = _check(isamAppliance, kdb_id, label=label, certificate=cert, password=password, simple_check=False)
    if certsubject is not None:
        logger.debug(f"Subject from new certificate {certsubject}")
    if force or not certexists:
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
            # This is a very normal error if you want to update an existing certificate
            # text: {"message":"CTGSK2021W A duplicate certificate already exists in the database."}
            #
            try:
                retObj = isamAppliance.invoke_post_files(
                             "Importing a personal certificate into a certificate database",
                             f"/isam/ssl_certificates/{kdb_id}/personal_cert",
                             [
                                 post_data
                             ],
                             json_data,
                             warnings=warnings
                         )
            except:
                # Delete the previous certificate and add the new.
                # The certificate exists with these values; so we want to overwrite it
                retObjDel = delete(isamAppliance, kdb_id, label, force=True, ignore_error=True)
                logger.debug(f"First try deleting {label}\n\n{retObjDel.get("rc", 200)}\n")
                if retObjDel.get("rc", 200) > 400:
                    # Delete using the subject as label
                    retObjDel = delete(isamAppliance, kdb_id, certsubject, force=True, ignore_error=True)
                    logger.debug(f"Second try at deleting using the new subject {certsubject}\n\n{retObjDel.get("rc", 200)}\n")
                # Try again
                retObj = isamAppliance.invoke_post_files(
                             "Retry Importing a personal certificate into a certificate database",
                             f"/isam/ssl_certificates/{kdb_id}/personal_cert",
                             [
                                 post_data
                             ],
                             json_data,
                             warnings=warnings
                         )
            return retObj

    return isamAppliance.create_return_object()


def extract_cert(isamAppliance, kdb_id, cert_id, password, filename, check_mode=False, force=False):
    """
    Extracting a personal certificate from a certificate database
    """
    if force or (_check(isamAppliance, kdb_id, label=cert_id) and not os.path.exists(filename)):
        if check_mode:
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


def _check(isamAppliance, kdb_id, label=None, certificate=None, password=None, simple_check=True):
    """
    Check if personal certificate already exists in certificate database
    This is idempotent now; using the subject of the incoming certificate (if you installed cryptography and dateutils
    Returns true or false and also the subject (in case of true)
    """
    if label is None:
        logger.debug("No label passed, so return false")
        if not performCertCheck:
            return False, None
        if simple_check:
            # This is to cater for current usage where the full idempotency is not requested
            return False, None

    if (not simple_check):
        if performCertCheck and (certificate is not None) and (password is not None):
            newCert = {}

            _enc = 'utf-8'
            with open(certificate, 'rb') as f:
                c = f.read()
            password = password.encode()
            p = cryptography.hazmat.primitives.serialization.pkcs12.load_pkcs12(c, password)

            x509 = p.cert.certificate

            # Define a mapping to fix some OIDs with "MAIL"
            attr_name_overrides = {
                ObjectIdentifier("0.9.2342.19200300.100.1.3"): "MAIL", # MAIL
                ObjectIdentifier("1.2.840.113549.1.9.1"): "MAIL",  # EMAIL_ADDRESS
                # Add other OIDs as needed
            }

            try:
                newCert['subject'] = x509.subject.rfc4514_string(attr_name_overrides=attr_name_overrides)
                newCert['issuer'] = x509.issuer.rfc4514_string(attr_name_overrides=attr_name_overrides)
            except:
                newCert['subject'] = x509.subject.rfc4514_string()
                newCert['issuer'] = x509.issuer.rfc4514_string()
                logger.info(
                    'Upgrade cryptography to version 36.0.0.  Install with pip install cryptography')

            newCert['notafter'] = x509.not_valid_after_utc.strftime("%Y-%m-%d")
            newCert['notbefore'] = x509.not_valid_before_utc.strftime("%Y-%m-%d")
            logger.debug(f"\nLOADING SUBJECT:\n {newCert['subject']}\n")
            ret_obj = get_all(isamAppliance, kdb_id)
            currentCert = None
            for certdb in ret_obj['data']:
                if certdb['id'] == label:
                      currentCert = certdb
                elif certdb['id'] == newCert['subject']:
                      currentCert = certdb
                elif certdb['subject'] == newCert['subject']:
                      currentCert = certdb
            if currentCert is None:
                logger.debug(f"\nNo match for:\n {certdb['subject']}\n")
                return False, newCert['subject']
            logger.debug(f"\nCurrent cert:\n {currentCert}\n")
            # remove values that are not checked
            currentCert.pop("keysize", None)
            currentCert.pop("version", None)

            # use date only to compare.  this simplifies the logic here, Python is not very strong with comparing dates in different timezones
            currentCert['notbefore'] = parser.parse(currentCert['notbefore'], ignoretz=True).strftime("%Y-%m-%d")
            currentCert['notafter'] = parser.parse(currentCert['notafter'], ignoretz=True).strftime("%Y-%m-%d")

            if json_equals(currentCert, newCert):
                # No updates needed
                return True, newCert['subject']
            else:
                return False, newCert['subject']
        else:
            logger.info(
                'Skipping management certificate full idempotency check, probably because cryptography>=36.0.0 is not available.  Install with pip install cryptography')

    # Do simple check
    ret_obj = get_all(isamAppliance, kdb_id)
    for certdb in ret_obj['data']:
        if certdb['id'] == label:
           return True, certdb.get('subject', label)
    return False, None


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
