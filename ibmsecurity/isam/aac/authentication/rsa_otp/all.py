import logging

logger = logging.getLogger(__name__)

uri = "/iam/access/v8/otp/config/rsa"
requires_modules = ["mga"]
requires_version = "8.0.0.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of configuration files for RSA
    """
    return isamAppliance.invoke_get("Retrieve a list of configuration files for RSA",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)
