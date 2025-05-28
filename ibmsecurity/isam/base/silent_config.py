import logging

logger = logging.getLogger(__name__)

# URI for this module
module_uri = "/silent_config"
requires_modules = None
requires_version = None
requires_model = "Appliance"


def get(isamAppliance, check_mode=False, force=False):
    """
    Getting the silent configuration flag
    """
    return isamAppliance.invoke_get("Getting the silent configuration flag", f"{module_uri}/flag",
                                    requires_version=requires_version, requires_modules=requires_modules,
                                    requires_model=requires_model)


def update(isamAppliance, flag, check_mode=False, force=False):
    """
    Setting the silent configuration flag
    """
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']
    if 'flag' in ret_obj['data']:
        if ret_obj['data']['flag'] != flag:
            check_value = True
        else:
            check_value = False
    else:
        check_value = False

    if force is True or check_value is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            json_data = {"flag": flag}
            return isamAppliance.invoke_put("Setting the silent configuration flag", f"{module_uri}/flag",
                                            json_data, requires_version=requires_version,
                                            requires_modules=requires_modules,
                                            requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)


def _export(isamAppliance, uri, network_hostname, filename, network_1_1_ipv4_address, network_1_1_ipv4_netmask,
            network_1_1_ipv4_gateway, network_1_1_ipv6_address, network_1_1_ipv6_prefix, network_1_1_ipv6_gateway,
            include_policy, check_mode=False, force=False):
    """
    Generating a silent configuration
    """
    # create the request header for the post first
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Content-type": "application/x-www-form-urlencoded"
              }

    json_data = {
        "network.hostname": network_hostname,
        "network.1.1.ipv4.address": network_1_1_ipv4_address,
        "network.1.1.ipv4.netmask": network_1_1_ipv4_netmask,
        "network.1.1.ipv4.gateway": network_1_1_ipv4_gateway,
        "network.1.1.ipv6_address": network_1_1_ipv6_address,
        "network.1.1.ipv6.prefix": network_1_1_ipv6_prefix,
        "network.1.1.ipv6.gateway": network_1_1_ipv6_gateway,
        "include_policy": include_policy
    }

    post_data = ""
    for k, value in json_data.items():
        if value is not None:
            post_data = f"{post_data}{k}={value}&"

    # strip the last & added
    post_data = post_data[:-1]
    import os.path

    if force is True or os.path.exists(filename) is False:
        if check_mode is False:  # No point downloading a file if in check_mode

            ret_obj = isamAppliance.invoke_request("Generating a silent configuration", "post", uri=uri,
                                                   filename=filename, requires_modules=requires_modules,
                                                   requires_version=requires_version, data=post_data, headers=headers,
                                                   stream=True, requires_model=requires_model)
            # HTTP POST calls get flagged as changes - but no changes here
            if ret_obj['changed'] is True:
                ret_obj['changed'] = False

            return ret_obj

    return isamAppliance.create_return_object()


def export_iso(isamAppliance, network_hostname, filename=None, network_1_1_ipv4_address=None,
               network_1_1_ipv4_netmask=None, network_1_1_ipv4_gateway=None, network_1_1_ipv6_address=None,
               network_1_1_ipv6_prefix=None, network_1_1_ipv6_gateway=None, include_policy="false", check_mode=False,
               force=False):
    logger.info("Generating an ISO file for silent configuration.")
    uri = f"{module_uri}/create/iso"
    if filename is None:
        filename = f"{network_hostname}.iso"
        logger.debug(f"Using filename as: {filename}")

    return _export(isamAppliance, uri, network_hostname, filename, network_1_1_ipv4_address, network_1_1_ipv4_netmask,
                   network_1_1_ipv4_gateway, network_1_1_ipv6_address, network_1_1_ipv6_prefix,
                   network_1_1_ipv6_gateway, include_policy, check_mode, force)


def export_img(isamAppliance, network_hostname, filename=None, network_1_1_ipv4_address=None,
               network_1_1_ipv4_netmask=None, network_1_1_ipv4_gateway=None, network_1_1_ipv6_address=None,
               network_1_1_ipv6_prefix=None, network_1_1_ipv6_gateway=None, include_policy="false", check_mode=False,
               force=False):
    logger.info("Generating an IMG file for silent configuration.")

    uri = f"{module_uri}/create/usb"
    if filename is None:
        filename = f"{network_hostname}.img"
        logger.debug(f"Using filename as: {filename}")

    return _export(isamAppliance, uri, network_hostname, filename, network_1_1_ipv4_address, network_1_1_ipv4_netmask,
                   network_1_1_ipv4_gateway, network_1_1_ipv6_address, network_1_1_ipv6_prefix,
                   network_1_1_ipv6_gateway, include_policy, check_mode, force)
