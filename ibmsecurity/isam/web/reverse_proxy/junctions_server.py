import logging
import ibmsecurity.utilities.tools
from ibmsecurity.utilities import tools
import ibmsecurity.isam.web.reverse_proxy.junctions
from ibmsecurity.isam.web.reverse_proxy.junctions_config import server_fields
import json

logger = logging.getLogger(__name__)

uri = "/wga/reverseproxy"
requires_modules = ["wga"]
requires_version = None

def search(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port):
    ret_obj_new = isamAppliance.create_return_object()
    ret_obj = ibmsecurity.isam.web.reverse_proxy.junctions.get(isamAppliance, reverseproxy_id, junction_point)
    for s in ret_obj['data']['servers']:
        logger.debug("Servers in Junction server: {0} port: {1}".format(s['server_hostname'], s['server_port']))
        if str(server_hostname) == str(s['server_hostname']) and str(server_port) == str(s['server_port']):
            ret_obj_new['data'] = s['server_uuid']
            break

    return ret_obj_new

def get(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port):
    ret_obj_new = isamAppliance.create_return_object()
    ret_obj = ibmsecurity.isam.web.reverse_proxy.junctions.get(isamAppliance, reverseproxy_id, junction_point)
    for s in ret_obj['data']['servers']:
        logger.debug("Servers in Junction server: {0} port: {1}".format(s['server_hostname'], s['server_port']))
        if str(server_hostname) == str(s['server_hostname']) and str(server_port) == str(s['server_port']):
            ret_obj_new['data'] = s
            break
    return ret_obj_new

def add(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port, junction_type="tcp", check_mode=False, force=False, warnings=[],
        **optionargs):
    """
    Adding a back-end server to an existing standard or virtual junctions

    :param isamAppliance:
    :param reverseproxy_id:
    :param junction_point:
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
    if not force:
        ret_obj = search(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port)

    if force or ret_obj['data'] == {}:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            jct_srv_json = {
                "junction_point": junction_point,
                "junction_type": junction_type,
                "server_hostname": server_hostname,
                "server_port": server_port
            }
            for _k, _v in optionargs.items():
                if _v is not None:
                    jct_srv_json[_k] = _v
            if jct_srv_json.get('stateful_junction', None) is None:
                jct_srv_json['stateful_junction'] = 'no'
            if jct_srv_json.get('windows_style_url', None) is None:
                jct_srv_json['windows_style_url'] = 'no'

            # case_insensitive/case_sensitive
            if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
                # If no case_insensitive_url is passed, we take the old one and invert it.
                # Who thinks it's a good idea to make changes in an API like this ?
                if jct_srv_json.get('case_insensitive_url', None) is None:
                    case_sensitive_url = jct_srv_json.get('case_sensitive_url', None)
                    if case_sensitive_url is not None and case_sensitive_url.lower() == 'no':
                        jct_srv_json["case_insensitive_url"] = 'yes'
                    else:
                        jct_srv_json["case_insensitive_url"] = 'no' # default
                    jct_srv_json.pop("case_sensitive_url", None)
            else:
                jct_srv_json.pop("case_insensitive_url", None)

            if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                if jct_srv_json.get('server_cn', None) is not None:
                    warnings.append(
                        "Appliance at version: {0}, server_cn: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring server_cn for this call.".format(
                            isamAppliance.facts["version"], server_cn))
                    jct_srv_json.pop("server_cn", None)

            if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                if jct_srv_json.get('priority', None) is not None:
                    warnings.append(
                        "Appliance at version: {0}, priority: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring priority for this call.".format(
                            isamAppliance.facts["version"], priority))
                    jct_srv_json.pop("priority", None)
            else:
                if jct_srv_json.get('priority', None) is None:
                    warnings.append(
                        "Appliance at version: {0}, priority is required on 10.0.2 or higher".format(
                            isamAppliance.facts["version"]))
                    jct_srv_json['priority'] = "9"
            return isamAppliance.invoke_put(
                "Adding a back-end server to an existing standard or virtual junctions",
                "{0}/{1}/junctions".format(uri, reverseproxy_id), jct_srv_json)

    return isamAppliance.create_return_object()

def set(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port, junction_type="tcp", check_mode=False, force=False, warnings=[],
        **optionargs):
    """
    Adding a back-end server to an existing standard or virtual junctions

    :param isamAppliance:
    :param reverseproxy_id:
    :param junction_point:
    :param server_hostname:
    :param junction_type:
    :param server_port:
    :param virtual_hostname:
    :param virtual_https_hostname:
    :param server_dn:
    :param query_contents:
    :param stateful_junction:
    :param case_sensitive_url:
    :param windows_style_url:
    :param https_port:
    :param http_port:
    :param proxy_hostname:
    :param proxy_port:
    :param sms_environment:
    :param vhost_label:
    :param server_uuid:
    :param server_cn:
    :param priority:
    :param check_mode:
    :param force:
    :return:
    """
    # load option args
    #   server_dn=None,
    #   stateful_junction='no', case_sensitive_url='no', windows_style_url='no', virtual_hostname=None,
    #   virtual_https_hostname=None, query_contents=None, https_port=None, http_port=None, proxy_hostname=None,
    #   proxy_port=None, sms_environment=None, vhost_label=None, server_uuid=None,
    #   server_cn=None, priority='9'

    # Search an existing server
    ret_obj = get(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port)
    exist_jct = {}
    jct_srv_json = {}
    if ret_obj:
        exist_jct = ret_obj.get('data', {})
        exist_jct.pop('current_requests', None)
        exist_jct.pop('total_requests', None)
        exist_jct.pop('operation_state', None)
        exist_jct.pop('server_state', None)
        exist_jct.pop('query_contents', None)

    for _k, _v in optionargs.items():
        # only keep valid arguments
        if _k in list(server_fields.keys()):
            jct_srv_json[_k] = _v
        else:
            logger.debug(f"Invalid input parameter used {_k}")
            warnings.append(f"Invalid input parameter used in function junctions_server.set() : {_k}")
    # add defaults
    #defaults_no = ["stateful_junction", "case_sensitive_url", "windows_style_url"]
    #for d in defaults_no:
    #    if jct_srv_json.get(d, None) is None:
    #        jct_srv_json[d] = 'no'
    # 10.0.0.2
    if jct_srv_json.get('priority', None) is not None:
        if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
            warnings.append(
                "Appliance at version: {0}, priority: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring description for this call.".format(
                    isamAppliance.facts["version"], priority))
            jct_srv_json.pop('priority', None)
    else:
        if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") >= 0:
            warnings.append(
                "Appliance at version: {0}, priority is required".format(
                    isamAppliance.facts["version"]))
            jct_srv_json['priority'] = "9"

    # only compare values that are in the new request
    exist_jct = {k: v for k, v in exist_jct.items() if k in jct_srv_json.keys()}

    newJSON = json.dumps(jct_srv_json, skipkeys=True, sort_keys=True)
    logger.debug(f"\nSorted Desired  Junction {junction_point} - {server_hostname}:\n\n {newJSON}\n")

    oldJSON = json.dumps(exist_jct, skipkeys=True, sort_keys=True)
    logger.debug(f"\nSorted Current  Junction {junction_point} - {server_hostname}:\n\n {oldJSON}\n")

    jct_srv_json["junction_point"] = junction_point
    jct_srv_json["junction_type"] = junction_type
    jct_srv_json["server_hostname"] = server_hostname
    jct_srv_json["server_port"] = server_port

    if force or (newJSON != oldJSON):
        logger.debug(f"The JSONs are different.  We're going to add the servers.")
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Adding a back-end server to an existing standard or virtual junctions",
                "{0}/{1}/junctions".format(uri, reverseproxy_id), data=jct_srv_json, warnings=warnings)
    else:
        logger.debug("Servers are the same")
        return isamAppliance.create_return_object(warnings=warnings)


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
