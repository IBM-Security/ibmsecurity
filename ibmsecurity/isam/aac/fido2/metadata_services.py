import logging
import json
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/fido2/metadata-services"
requires_modules = ["mga"]
requires_version = "10.0.4.0"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of FIDO2 Metadata Services
    """
    return isamAppliance.invoke_get("Retrieving the list of FIDO2 Metadata Services", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)

def get(isamAppliance, url, id=None, check_mode=False, force=False):
    """
    Retrieve a specific FIDO2 Metadata Service
    """
    if id is None:
        ret_obj = search(isamAppliance, url=url, check_mode=check_mode, force=force)
        id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 Metadata Service {0} had no match, skipping retrieval.".format(url))
        return isamAppliance.create_return_object()
    else:
        return _get(isamAppliance, id)

def search(isamAppliance, url, force=False, check_mode=False):
    """
    Search FIDO2 Metadata Service id by url
    """
    ret_obj = get_all(isamAppliance)
    return_obj = isamAppliance.create_return_object()

    for obj in ret_obj['data']:
        if obj['url'] == url:
            logger.info("Found FIDO2 Metadata Service {0} id: {1}".format(url, obj['id']))
            return_obj['data'] = obj['id']
            return_obj['rc'] = 0

    return return_obj

def delete(isamAppliance, url, check_mode=False, force=False):
    """
    Delete a FIDO2 Metadata Service
    """
    ret_obj = search(isamAppliance, url, check_mode=check_mode, force=force)
    id = ret_obj['data']

    if id == {}:
        logger.info("FIDO2 Metadata Service {0} not found, skipping delete.".format(url))
    else:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete a FIDO2 Metadata Service",
                "{0}/{1}".format(uri, id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def set(isamAppliance, url, retryInterval=3600, truststore="", jwsTruststore="",
        username="", password="", keystore="", certificate="", protocol="", timeout=5, proxy="", headers=[],
        check_mode=False, force=False):
    """
    Create or Update a FIDO2 Metadata Service
    """
    if (search(isamAppliance, url=url))['data'] == {}:
        # Force the add - we already know FIDO2 Metadata Service does not exist
        logger.info("FIDO2 metadata service {0} had no match, requesting to add new one.".format(url))
        return add(isamAppliance, url=url, retryInterval=retryInterval, truststore=truststore, jwsTruststore=jwsTruststore,
                   username=username, password=password, keystore=keystore, certificate=certificate, protocol=protocol,
                   timeout=timeout, proxy=proxy, headers=headers, check_mode=check_mode, force=force)
    else:
        # Update request
        logger.info("FIDO2 metadata service {0} exists, requesting to update.".format(url))
        return update(isamAppliance, url=url, retryInterval=retryInterval, truststore=truststore, jwsTruststore=jwsTruststore,
                   username=username, password=password, keystore=keystore, certificate=certificate, protocol=protocol,
                   timeout=timeout, proxy=proxy, headers=headers, check_mode=check_mode, force=force)

def add(isamAppliance, url, retryInterval=3600, truststore="", jwsTruststore="",
        username="", password="", keystore="", certificate="", protocol="", timeout=5, proxy="", headers=[],
        check_mode=False, force=False):
    """
    Create a new FIDO2 Metadata Service
    """
    if force is False:
        ret_obj = search(isamAppliance, url)
    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post(
                "Create a new FIDO2 metadata service", uri,
                {
                    "url": url,
                    "retryInterval": retryInterval,
                    "truststore": truststore,
                    "jwsTruststore": jwsTruststore,
                    "username": username,
                    "password": password,
                    "keystore": keystore,
                    "certificate": certificate,
                    "protocol": protocol,
                    "timeout": timeout,
                    "proxy": proxy,
                    "headers": headers
                }, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()

def update(isamAppliance, url="", retryInterval=3600, truststore="", jwsTruststore="",
           username="", password="", keystore="", certificate="", protocol="", timeout=5, proxy="", headers=[],
           check_mode=False, force=False):
    """
    Update a specific FIDO2 Metadata Service
    """
    mds_id, update_required, json_data = _check(isamAppliance, url, retryInterval, truststore, jwsTruststore,
                                                username, password, keystore, certificate, protocol,
                                                timeout, proxy, headers)
    if mds_id is None:
        from ibmsecurity.appliance.ibmappliance import IBMError
        raise IBMError("999", "Cannot update data for unknown FIDO2 relying party: {0}".format(name))

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update a specific FIDO2 relying party",
                "{0}/{1}".format(uri, mds_id), json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()

def _get(isamAppliance, id):
    return isamAppliance.invoke_get("Retrieve a specific FIDO2 Metadata Service by id",
                                    f"{uri}/{id}",
                                    requires_modules=requires_modules, requires_version=requires_version)

def _check(isamAppliance, url, retryInterval, truststore, jwsTruststore, username, password,
            keystore, certificate, protocol, timeout, proxy, headers):
    """
    Check if FIDO2 metadata service configuration is identical with server
    """
    update_required = False
    json_data = {}
    ret_obj = get(isamAppliance, url)
    if ret_obj['data'] == {}:
        logger.info("FIDO2 Metadata Service not found, returning update required.")
        return None, update_required, json_data
    else:
        logger.debug("Comparing server FIDO2 metadata service configuration with desired configuration.")

        # Converting python ret_obj['data'] dict to valid JSON (RFC 8259)
        # e.g. converts python boolean 'True' -> to JSON literal lowercase value 'true'
        cur_cfg = ret_obj['data']
        cur_cfg_id = cur_cfg['id']
        del cur_cfg['id']
        cur_json_string = json.dumps(cur_cfg)
        cur_sorted_json = tools.json_sort(cur_json_string)
        logger.debug("Server JSON : {0}".format(cur_sorted_json))

        new_cfg = {
            'url': url,
            'retryInterval': retryInterval,
            'truststore': truststore,
            'jwsTruststore': jwsTruststore,
            'username': username,
            'password': password,
            'keystore': keystore,
            'certificate': certificate,
            'protocol': protocol,
            'timeout': timeout,
            'proxy': proxy,
            'headers': headers
        }
        given_json_string = json.dumps(new_cfg)
        given_sorted_json = tools.json_sort(given_json_string)
        logger.debug("Desired JSON: {0}".format(given_sorted_json))

        if cur_sorted_json != given_sorted_json:
            logger.debug("Changes detected!")
            update_required = True
            json_data = new_cfg
        else:
            logger.debug("Server configuration is identical with desired configuration. No change necessary.")
            update_required = False
            json_data = new_cfg

        return cur_cfg_id, update_required, json_data
