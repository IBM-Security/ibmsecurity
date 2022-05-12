import logging
import ibmsecurity.utilities.tools
from datetime import datetime
import json

performCertCheck = True
try:
    from dateutil import parser
    #pip install python-dateutil
    from OpenSSL.crypto import load_pkcs12, dump_certificate, load_certificate, FILETYPE_PEM
    # pip install pyOpenSSL
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
        warnings = ["Idempotency not available. Unable to extract existing certificate to compare with provided one.  Install Python modules python-dateutil and pyOpenSSL."]
    else:
        warnings = None
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
    requires additionally pyOpenSSL to load the p12 and extract the issuer, subject, etc
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
        _type = FILETYPE_PEM
        _enc = 'utf-8'
        with open(certificate, 'rb') as f:
            c = f.read()
        p = load_pkcs12(c, password)

        certificate = p.get_certificate()
        newCert['subject'] = ",".join(f"{str(name, 'utf-8')}={str(value, 'utf-8')}" for name, value in reversed(certificate.get_subject().get_components()))

        x509 = load_certificate(_type, dump_certificate(_type, certificate))

        newCert['issuer'] = ",".join(f"{str(name, _enc)}={str(value, _enc)}" for name, value in reversed(x509.get_issuer().get_components()))
        newCert['notafter'] = datetime.strptime(str(x509.get_notAfter(), _enc), "%Y%m%d%H%M%SZ").strftime("%Y-%m-%d")
        newCert['notbefore'] = datetime.strptime(str(x509.get_notBefore(), _enc), "%Y%m%d%H%M%SZ").strftime("%Y-%m-%d")

        curc = json.dumps(currentCert, skipkeys=True, sort_keys=True)
        logger.debug(f"\nSorted Current  Management Cert:\n {curc}\n")

        newc = json.dumps(newCert, skipkeys=True, sort_keys=True)
        logger.debug(f"\nSorted Desired  Management Cert:\n {newc}\n")

        if curc == newc:
            return True
        else:
            return False
    else:
        logger.info('Skipping management certificate check because pyOpenSSL or not available.  Install with pip install pyOpenSSL')
        return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare management authentication settings
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
