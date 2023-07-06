import logging
import ibmsecurity.utilities.tools
from datetime import datetime
import json

performCertCheck = True
try:
    from dateutil import parser
    #pip install python-dateutil
    import cryptography.hazmat.primitives.serialization.pkcs12
    import cryptography.x509
    # pip install cryptography
except:
    performCertCheck = False

logger = logging.getLogger(__name__)

def get(isamAppliance, check_mode=False, force=False):
    """
    Get management ssl certificate information
    """
    return isamAppliance.invoke_get("Get management ssl certificate information",
                                    "/isam/management_ssl_certificate/")


def set(isamAppliance, certificate, password, check_mode=False, force=False):
    """
    Import certificate database
    """
    if not performCertCheck:
        warnings = ["Idempotency not available. Unable to extract existing certificate to compare with provided one.  Install Python modules python-dateutil and cryptography."]
    else:
        warnings = []
    if force is True or not _check(isamAppliance, certificate, password):
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_post_files(
                "Import certificate database",
                "/isam/management_ssl_certificate",
                [
                    {
                        'file_formfield': 'cert',
                        'filename': certificate,
                        'mimetype': 'application/x-pkcs12'
                    }
                ],
                {
                    'password': password
                },
                json_response=False, warnings=warnings)

    return isamAppliance.create_return_object()


def _check(isamAppliance, certificate, password):
    """
    requires additionally cryptography to load the p12 and extract the issuer, subject, etc
    Comparing issuer, subject, notafter (date only) and notbefore (date only)
    This DOES NOT check if the certificate is newer , just that it's different from the one that is deployed.
    """
    if performCertCheck:
        currentCert = get(isamAppliance)
        currentCert = currentCert['data']

        # remove values that are not checked
        del currentCert['keysize']
        del currentCert['version']

        # use date only to compare.  this simplifies the logic here, Python is not very strong with comparing dates in different timezones
        currentCert['notbefore'] = parser.parse(currentCert['notbefore'], ignoretz=True).strftime("%Y-%m-%d")
        currentCert['notafter'] = parser.parse(currentCert['notafter'], ignoretz=True).strftime("%Y-%m-%d")

        newCert = {}

        _enc = 'utf-8'
        with open(certificate, 'rb') as f:
            c = f.read()
        password = password.encode()
        p = cryptography.hazmat.primitives.serialization.pkcs12.load_pkcs12(c, password)

        x509 = p.cert.certificate
        newCert['subject'] = x509.subject.rfc4514_string()

        newCert['issuer'] = x509.issuer.rfc4514_string()
        newCert['notafter'] = x509.not_valid_after.strftime("%Y-%m-%d")
        newCert['notbefore'] = x509.not_valid_before.strftime("%Y-%m-%d")

        curc = json.dumps(currentCert, skipkeys=True, sort_keys=True)
        logger.debug(f"\nSorted Current  Management Cert:\n {curc}\n")

        newc = json.dumps(newCert, skipkeys=True, sort_keys=True)
        logger.debug(f"\nSorted Desired  Management Cert:\n {newc}\n")

        if curc == newc:
            return True
        else:
            return False
    else:
        logger.info('Skipping management certificate idempotency check because cryptography not available.  Install with pip install cryptography')
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
