import logging

logger = logging.getLogger(__name__)

uri = "/wga/reverseproxy"
requires_modules = "wga"
requires_version = None


def set(isamAppliance, id, isamUser, hostname, port, junction="/mga", reuse_certs=None, reuse_acls=None,
        check_mode=False, force=False):
    """
    Authentication and Context based access configuration for a reverse proxy
    """
    return isamAppliance.invoke_post("Authentication and Context based access configuration for a reverse proxy ",
                                     "{0}/{1}/authsvc_config".format(uri, id),
                                     {
                                         "username": isamUser.username,
                                         "password": isamUser.password,
                                         "hostname": hostname,
                                         "port": port,
                                         "junction": junction,
                                         "reuse_certs": reuse_certs,
                                         "reuse_acls": reuse_acls
                                     },
                                     requires_modules=requires_modules, requires_version=requires_version)
