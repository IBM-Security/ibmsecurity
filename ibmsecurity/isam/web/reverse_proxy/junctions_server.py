import logging
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools
import ibmsecurity.isam.web.reverse_proxy.junctions

logger = logging.getLogger(__name__)

uri = "/wga/reverseproxy"


def search(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port):
    ret_obj_new = isamAppliance.create_return_object()
    ret_obj = ibmsecurity.isam.web.reverse_proxy.junctions.get(isamAppliance, reverseproxy_id, junction_point)
    for s in ret_obj['data']['servers']:
        logger.debug("Servers in Junction server: {0} port: {1}".format(s['server_hostname'], s['server_port']))
        if str(server_hostname) == str(s['server_hostname']) and str(server_port) == str(s['server_port']):
            ret_obj_new['data'] = s['server_uuid']
            break

    return ret_obj_new


def add(isamAppliance, reverseproxy_id, junction_point, server_hostname, junction_type, server_port, server_dn=None,
        stateful_junction='no', case_sensitive_url='no', windows_style_url='no', virtual_hostname=None,
        virtual_https_hostname=None, query_contents=None, https_port=None, http_port=None, proxy_hostname=None,
        proxy_port=None, sms_environment=None, vhost_label=None, server_uuid=None, priority=None, server_cn=None,
        case_insensitive_url=None, check_mode=False, force=False):
    """
    Adding a back-end server to an existing standard or virtual junctions

    :param isamAppliance:
    :param reverseproxy_id:
    :param junctionname:
    :param server_hostname:
    :param junction_type:
    :param server_port:
    :param virtual_hostname:
    :param virtual_https_hostname:
    :param server_dn:
    :param query_contents:
    :param stateful_junction:
    :param case_sensitive_url:
    :param case_insensitive_url:  #v1.0.6+
    :param windows_style_url:
    :param https_port:
    :param http_port:
    :param proxy_hostname:
    :param proxy_port:
    :param sms_environment:
    :param vhost_label:
    :param server_uuid:
    :param priority:
    :param server_cn:
    :param check_mode:
    :param force:
    :return:
    """
    # Search for the UUID of the junctioned server
    if force is False:
        ret_obj = search(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port)

    if force is True or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            jct_srv_json = {
                "junction_point": junction_point,
                "junction_type": junction_type,
                "server_hostname": server_hostname,
                "server_port": server_port,
                "stateful_junction": stateful_junction,
                "windows_style_url": windows_style_url,
            }
            if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
                # If no case_insensitive_url is passed, we take the old one and invert it.
                # Who thinks it's a good idea to make changes in an API like this ?
                if case_insensitive_url is None:
                    if case_sensitive_url.lower() == 'yes':
                        jct_srv_json["case_insensitive_url"] = 'no'
                    else:
                        jct_srv_json["case_insensitive_url"] = 'yes'
                else:
                    jct_srv_json["case_insensitive_url"] = case_insensitive_url
            else:
                jct_srv_json["case_sensitive_url"] = case_sensitive_url
            if https_port is not None:
                jct_srv_json["https_port"] = https_port
            if http_port is not None:
                jct_srv_json["http_port"] = http_port
            if proxy_hostname is not None:
                jct_srv_json["proxy_hostname"] = proxy_hostname
            if proxy_port is not None:
                jct_srv_json["proxy_port"] = proxy_port
            if sms_environment is not None:
                jct_srv_json["sms_environment"] = sms_environment
            if vhost_label is not None:
                jct_srv_json["vhost_label"] = vhost_label
            if server_dn is not None:
                jct_srv_json["server_dn"] = server_dn
            if virtual_hostname:
                jct_srv_json["virtual_hostname"] = virtual_hostname
            if virtual_https_hostname is not None:
                jct_srv_json["virtual_https_hostname"] = virtual_https_hostname
            if query_contents is not None:
                jct_srv_json["query_contents"] = query_contents
            if server_uuid is not None and server_uuid != '':
                jct_srv_json["server_uuid"] = server_uuid
            if server_cn is not None:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, server_cn: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring server_cn for this call.".format(
                            isamAppliance.facts["version"], server_cn))
                    server_cn = None
                else:
                    jct_srv_json["server_cn"] = server_cn
            if priority is not None:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, priority: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring priority for this call.".format(
                            isamAppliance.facts["version"], priority))
                    priority = None
                else:
                    jct_srv_json["priority"] = priority

            return isamAppliance.invoke_put(
                "Adding a back-end server to an existing standard or virtual junctions",
                "{0}/{1}/junctions".format(uri, reverseproxy_id), jct_srv_json)

    return isamAppliance.create_return_object()


def delete(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port, check_mode=False, force=False):
    """
    Deleting a standard or virtual junction's server

    :param isamAppliance:
    :param reverseproxy_id:
    :param junction_point:
    :param check_mode:
    :param force:
    :return:
    """
    # Search for the UUID of the junctioned server
    if force is False:
        ret_obj = search(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port)

    if force is True or ret_obj['data'] != {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a standard or virtual junction's server",
                "{0}/{1}/junctions?junctions_id={2}&servers_id={3}".format(uri, reverseproxy_id, junction_point,
                                                                           ret_obj['data']))

    return isamAppliance.create_return_object()
