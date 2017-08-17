import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/silent_config/create"
requires_modules = None
requires_version = None


def create_image(isamAppliance, image_type, network_hostname, network_1_1_ipv4_address=None,
                 network_1_1_ipv4_netmask=None, network_1_1_ipv4_gateway=None, network_1_1_ipv6_address=None,
                 network_1_1_ipv6_prefix=None, network_1_1_ipv6_gateway=None, include_policy="false", check_mode=False,
                 force=False):
    """
    create a silent configuration image, image_type is either "usb" or "cd"
    """
    global uri

    if not (image_type == "usb" or image_type == "cd"):
        return isamAppliance.create_return_object(
            warnings="Image type needs to be either usb or cd, and not: {0}".format(image_type))

    if image_type == "usb":
        filename = "{0}.img".format(network_hostname)
        uri = "{0}/usb".format(uri)
    if image_type == "cd":
        filename = "{0}.iso".format(network_hostname)
        uri = "{0}/iso".format(uri)

    # create the request header for the post first
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Content-type": "application/x-www-form-urlencoded"
               }

    input_data = {
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
    for k, value in input_data.iteritems():
        if value is not None:
            post_data = "{0}{1}={2}&".format(post_data, k, value)

    # strip the last & added
    post_data = post_data[:-1]

    ret_obj = isamAppliance.invoke_request("Creating a silent configuration file", "post", uri=uri, filename=filename,
                                           requires_modules=requires_modules, requires_version=requires_version,
                                           data=post_data, headers=headers, stream=True)
    # HTTP POST calls get flagged as changes - but no changes here
    if ret_obj['changed'] is True:
        ret_obj['changed'] = False

    return ret_obj
