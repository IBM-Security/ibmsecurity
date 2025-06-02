import logging
from ibmsecurity.utilities import tools
import ibmsecurity.isam.web.reverse_proxy.junctions_server as junctions_server
import json
from ibmsecurity.isam.web.reverse_proxy.junctions_config import server_fields
from ibmsecurity.utilities.tools import jsonSortedListEncoder

try:
    basestring
except NameError:
    basestring = (str, bytes)

# does not work anymore in Python 3.11+
logger = logging.getLogger(__name__)


# URI for this module
uri = "/wga/reverseproxy"
requires_modules = ["wga"]
requires_version = None



def get_all(isamAppliance, reverseproxy_id, detailed=None, check_mode=False, force=False, warnings=[]):
    """
    Retrieving a list of standard and virtual junctions

    :param isamAppliance:
    :param reverseproxy_id:
    :param detailed: Set to True if you want a detailed junction list (new in v10.0.4)
    :param check_mode:
    :param force:
    :return:
    """
    if detailed and tools.version_compare(isamAppliance.facts["version"], "10.0.4") >= 0:
        try:
            returnValue = isamAppliance.invoke_get("Retrieving a list of standard and virtual junctions",
                                        "{0}/{1}/junctions?detailed=true".format(uri, reverseproxy_id),
                                        requires_modules=requires_modules,
                                        requires_version=requires_version)
        except:
            warnings.append("Detailed retrieval of junctions failed unexpectedly.  Falling back to simple version.")
            returnValue = isamAppliance.invoke_get("Retrieving a list of standard and virtual junctions (fallback)",
                                    "{0}/{1}/junctions".format(uri, reverseproxy_id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version,
                                    warnings=warnings
            )
            returnValue['warnings'] = warnings
        return returnValue
    else:
      #ignore detailed for older versions
      return isamAppliance.invoke_get("Retrieving a list of standard and virtual junctions",
                                    "{0}/{1}/junctions".format(uri, reverseproxy_id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, reverseproxy_id, junctionname, check_mode=False, force=False, warnings=[]):
    """
    Retrieving the parameters for a single standard or virtual junction

    :param isamAppliance:
    :param reverseproxy_id:
    :param junctionname:
    :param check_mode:
    :param force:
    :param warnings
    :return:
    """
    logger = isamAppliance.logger
    ret_obj = isamAppliance.invoke_get("Retrieving the parameters for a single standard or virtual junction",
                                       "{0}/{1}/junctions?junctions_id={2}".format(uri, reverseproxy_id,
                                                                                   junctionname),
                                       requires_modules=requires_modules,
                                       requires_version=requires_version,
                                       warnings=warnings)
    # servers are provided as a single string, here we parse it out into a list + dict
    servers = []
    if tools.version_compare(isamAppliance.facts["version"], "9.0.1.0") > 0:
        srv_separator = '#'
    else:
        srv_separator = '&'
    srvs = ret_obj['data']['servers'].split(srv_separator)
    logger.debug("Servers in raw string: {0}".format(ret_obj['data']['servers']))
    logger.debug("Number of servers in junction: {0}".format(len(srvs)))
    for srv in srvs:
        logger.debug("Parsing Server: {0}".format(srv))
        server = {}
        for s in srv.split(';'):
            if s != '':
                kv = s.split('!')
                server[kv[0]] = kv[1]
        servers.append(server)

    ret_obj['data']['servers'] = servers
    return ret_obj


def _check(isamAppliance, reverseproxy_id, junctionname, currentJunctions=None):
    """ CurrentJunctions is the output of get_all.
        This avoids constantly having to call the get_all function.
    """
    if currentJunctions is None:
        ret_obj = get_all(isamAppliance, reverseproxy_id)
    else:
        ret_obj = currentJunctions

    for jct in ret_obj['data']:
        if jct['id'] == junctionname:
            return True

    return False


def add(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port, junction_type="tcp",
        virtual_hostname=None, server_dn=None, query_contents=None, stateful_junction=None, case_sensitive_url=None,
        windows_style_url=None, https_port=None, http_port=None, proxy_hostname=None, proxy_port=None,
        sms_environment=None, vhost_label=None, junction_hard_limit=None, junction_soft_limit=None,
        basic_auth_mode=None, tfim_sso=None, remote_http_header=None, preserve_cookie=None, cookie_include_path=None,
        transparent_path_junction=None, mutual_auth=None, insert_session_cookies=None, request_encoding=None,
        enable_basic_auth=None, key_label=None, gso_resource_group=None, junction_cookie_javascript_block=None,
        client_ip_http=None, version_two_cookies=None, ltpa_keyfile=None, authz_rules=None, fsso_config_file=None,
        username=None, password=None, server_uuid=None, local_ip=None, ltpa_keyfile_password=None,
        delegation_support=None, scripting_support=None, insert_ltpa_cookies=None, check_mode=False, force=False,
        http2_junction=None, http2_proxy=None, sni_name=None, description=None,
        priority=None, server_cn=None, silent=None,
        case_insensitive_url=None,
        servers=None,
        warnings=[]):
    """
    Creating a standard or virtual junction

    :param isamAppliance:
    :param reverseproxy_id:
    :param junction_point:
    :param server_hostname:
    :param server_port:
    :param junction_type:
    :param virtual_hostname:
    :param server_dn:
    :param query_contents:
    :param stateful_junction:
    :param case_sensitive_url:
    :param case_insensitive_url: #v10.0.6
    :param windows_style_url:
    :param https_port:
    :param http_port:
    :param proxy_hostname:
    :param proxy_port:
    :param sms_environment:
    :param vhost_label:
    :param junction_hard_limit:
    :param junction_soft_limit:
    :param basic_auth_mode:
    :param tfim_sso:
    :param remote_http_header:
    :param preserve_cookie:
    :param cookie_include_path:
    :param transparent_path_junction:
    :param mutual_auth:
    :param insert_session_cookies:
    :param request_encoding:
    :param enable_basic_auth:
    :param key_label:
    :param gso_resource_group:
    :param junction_cookie_javascript_block:
    :param client_ip_http:
    :param version_two_cookies:
    :param ltpa_keyfile:
    :param authz_rules:
    :param fsso_config_file:
    :param username:
    :param password:
    :param server_uuid:
    :param local_ip:
    :param ltpa_keyfile_password:
    :param delegation_support:
    :param scripting_support:
    :param insert_ltpa_cookies:
    :param check_mode:
    :param force:
    :param http2_junction:
    :param http2_proxy:
    :param sni_name:
    :param description:
    :param priority:
    :param server_cn:
    :param silent:
    :return:
    """
    # See if it's a virtual or standard junction
    isVirtualJunction = True
    logger = isamAppliance.logger
    if junction_point[:1] == '/':
        isVirtualJunction = False
    if force is True or _check(isamAppliance, reverseproxy_id, junction_point) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the main junction attributes
            jct_json = {
                "junction_point": junction_point,
                "junction_type": junction_type.lower(),
                "server_hostname": server_hostname,
                "server_port": server_port,
                "force": force
            }
            # Add attributes that have been supplied... otherwise skip them.
            if junction_hard_limit is not None:
                jct_json["junction_hard_limit"] = junction_hard_limit
            if junction_soft_limit is not None:
                jct_json["junction_soft_limit"] = junction_soft_limit
            if basic_auth_mode is not None:
                jct_json["basic_auth_mode"] = basic_auth_mode
            if tfim_sso is not None:
                jct_json["tfim_sso"] = tfim_sso
            if remote_http_header is not None:
                jct_json["remote_http_header"] = remote_http_header
            if stateful_junction is not None:
                jct_json["stateful_junction"] = stateful_junction
            if not isVirtualJunction and preserve_cookie:
                jct_json["preserve_cookie"] = preserve_cookie
            if not isVirtualJunction and cookie_include_path:
                jct_json["cookie_include_path"] = cookie_include_path
            if not isVirtualJunction and transparent_path_junction:
                jct_json["transparent_path_junction"] = transparent_path_junction
            if mutual_auth is not None:
                jct_json["mutual_auth"] = mutual_auth
            if insert_ltpa_cookies is not None:
                jct_json["insert_ltpa_cookies"] = insert_ltpa_cookies
            if insert_session_cookies is not None:
                jct_json["insert_session_cookies"] = insert_session_cookies
            if request_encoding is not None:
                jct_json["request_encoding"] = request_encoding
            if enable_basic_auth is not None:
                jct_json["enable_basic_auth"] = enable_basic_auth
            if key_label is not None:
                jct_json["key_label"] = key_label
            if gso_resource_group is not None:
                jct_json["gso_resource_group"] = gso_resource_group
            if junction_cookie_javascript_block is not None and junction_cookie_javascript_block != '':
                jct_json["junction_cookie_javascript_block"] = junction_cookie_javascript_block
            if client_ip_http is not None:
                jct_json["client_ip_http"] = client_ip_http
            if version_two_cookies is not None:
                jct_json["version_two_cookies"] = version_two_cookies
            if ltpa_keyfile is not None:
                jct_json["ltpa_keyfile"] = ltpa_keyfile
            if authz_rules is not None:
                jct_json["authz_rules"] = authz_rules
            if fsso_config_file is not None:
                jct_json["fsso_config_file"] = fsso_config_file
            if username is not None:
                jct_json["username"] = username
            if password is not None:
                jct_json["password"] = password
            if server_uuid is not None:
                jct_json["server_uuid"] = server_uuid
            if virtual_hostname is not None:
                jct_json["virtual_hostname"] = virtual_hostname
            if server_dn is not None:
                jct_json["server_dn"] = server_dn
            if local_ip is not None:
                jct_json["local_ip"] = local_ip
            if query_contents is not None:
                jct_json["query_contents"] = query_contents
            if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
                # If no case_insensitive_url is passed, we take the old one and invert it.
                # Who thinks it's a good idea to make changes in an API like this ?
                if case_insensitive_url is not None:
                    jct_json["case_insensitive_url"] = case_insensitive_url
                elif case_sensitive_url is not None:
                    if case_sensitive_url.lower() == 'no':
                        jct_json["case_insensitive_url"] = 'yes'
                    else:
                        jct_json["case_insensitive_url"] = 'no' # default
                else:
                    jct_json["case_insensitive_url"] = 'no'
            elif case_sensitive_url is not None:
                jct_json['case_sensitive_url'] = case_sensitive_url
            if windows_style_url is not None:
                jct_json["windows_style_url"] = windows_style_url
            if ltpa_keyfile_password is not None:
                jct_json["ltpa_keyfile_password"] = ltpa_keyfile_password
            if https_port is not None:
                jct_json["https_port"] = https_port
            if http_port is not None:
                jct_json["http_port"] = http_port
            if proxy_hostname is not None:
                jct_json["proxy_hostname"] = proxy_hostname
            if proxy_port is not None:
                jct_json["proxy_port"] = proxy_port
            if isVirtualJunction and sms_environment is not None:
                jct_json["sms_environment"] = sms_environment
            if isVirtualJunction and vhost_label is not None:
                jct_json["vhost_label"] = vhost_label
            if delegation_support is not None:
                jct_json["delegation_support"] = delegation_support
            if scripting_support is not None:
                jct_json["scripting_support"] = scripting_support
            if http2_junction is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, http2_junction: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring http2_junction for this call.".format(
                            isamAppliance.facts["version"], http2_junction))
                else:
                    jct_json["http2_junction"] = http2_junction
            if http2_proxy is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, http2_proxy: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring http2_proxy for this call.".format(
                            isamAppliance.facts["version"], http2_proxy))
                else:
                    jct_json['http2_proxy'] = http2_proxy
            if sni_name is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, sni_name: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring sni_name for this call.".format(
                            isamAppliance.facts["version"], sni_name))
                else:
                    jct_json['sni_name'] = sni_name
            if description is not None:
                if tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, description: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring description for this call.".format(
                            isamAppliance.facts["version"], description))
                else:
                    jct_json['description'] = description
            if priority is not None:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, priority: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring priority for this call.".format(
                            isamAppliance.facts["version"], priority))
                else:
                    jct_json['priority'] = priority
            else:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") >= 0:
                    warnings.append(
                        "Appliance at version: {0}, priority is required".format(
                            isamAppliance.facts["version"]))
                    jct_json['priority'] = "9"
                else:
                    priority = None
            if server_cn is not None:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") < 0:
                    warnings.append(
                        "Appliance at version: {0}, server_cn: {1} is not supported. Needs 10.0.2.0 or higher. Ignoring server_cn for this call.".format(
                            isamAppliance.facts["version"], server_cn))
                else:
                    jct_json['server_cn'] = server_cn
            if isVirtualJunction and silent:
                jct_json['silent'] = silent
            return isamAppliance.invoke_post(
                "Creating a standard or virtual junction",
                "{0}/{1}/junctions".format(uri, reverseproxy_id), jct_json,
                requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete(isamAppliance, reverseproxy_id, junctionname, check_mode=False, force=False):
    """
    Deleting a standard or virtual junction

    :param isamAppliance:
    :param reverseproxy_id:
    :param junctionname:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or _check(isamAppliance, reverseproxy_id, junctionname) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a standard or virtual junction",
                "{0}/{1}/junctions?junctions_id={2}".format(uri, reverseproxy_id, junctionname),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object()


def set(isamAppliance, reverseproxy_id, junction_point, server_hostname, server_port, junction_type="tcp",
        virtual_hostname=None, server_dn=None, query_contents=None, stateful_junction=None, case_sensitive_url=None,
        windows_style_url=None, https_port=None, http_port=None, proxy_hostname=None, proxy_port=None,
        sms_environment=None, vhost_label=None, junction_hard_limit=None, junction_soft_limit=None,
        basic_auth_mode=None, tfim_sso=None, remote_http_header=None, preserve_cookie=None, cookie_include_path=None,
        transparent_path_junction=None, mutual_auth=None, insert_session_cookies=None, request_encoding=None,
        enable_basic_auth=None, key_label=None, gso_resource_group=None, junction_cookie_javascript_block=None,
        client_ip_http=None, version_two_cookies=None, ltpa_keyfile=None, authz_rules=None, fsso_config_file=None,
        username=None, password=None, server_uuid=None, local_ip=None, ltpa_keyfile_password=None,
        delegation_support=None, scripting_support=None, insert_ltpa_cookies=None, check_mode=False, force=False,
        http2_junction=None, http2_proxy=None, sni_name=None, description=None,
        priority=None, server_cn=None, silent=None, case_insensitive_url=None, servers=None, warnings=[]):
    """
    Setting a standard or virtual junction - compares with existing junction and replaces if changes are detected
    """
    add_required = False
    logger = isamAppliance.logger
    # See if it's a virtual or standard junction
    isVirtualJunction = True
    if junction_point[:1] == '/':
        isVirtualJunction = False
        logger.debug("Junction: {0} is a standard junction".format(junction_point))
    if force is False:
        # Check if record exists
        logger.debug("Check if the junction exists.")
        if _check(isamAppliance, reverseproxy_id, junction_point):
            logger.debug("Junction exists. Compare junction details.")
            ret_obj = get(isamAppliance, reverseproxy_id=reverseproxy_id, junctionname=junction_point, warnings=warnings)
            exist_jct = ret_obj['data']
            jct_json = {
                'junction_point': junction_point,
                'junction_type': junction_type.lower(),
                'server_hostname': server_hostname,
                'server_port': server_port
            }
            logger.debug("See if the backend junction server matches any on the junction. Look for just one match.")
            srvs = ret_obj['data']['servers']
            srvs_len = len(srvs)

            if not junction_server_exists(isamAppliance, srvs=srvs,
                                          server_hostname=server_hostname,
                                          server_port=server_port,
                                          case_sensitive_url=case_sensitive_url,
                                          isVirtualJunction=isVirtualJunction,
                                          http_port= http_port,
                                          local_ip=local_ip,
                                          query_contents=query_contents,
                                          server_dn=server_dn,
                                          server_uuid=server_uuid,
                                          virtual_hostname=virtual_hostname,
                                          windows_style_url=windows_style_url,
                                          priority=priority,
                                          server_cn=server_cn,
                                          case_insensitive_url=case_insensitive_url):
                add_required = True
            elif not add_required:
                if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
                    # If no case_insensitive_url is passed, we take the old one and invert it.
                    # Who thinks it's a good idea to make changes in an API like this ?
                    if case_insensitive_url is not None:
                        jct_json["case_insensitive_url"] = case_insensitive_url
                    elif case_sensitive_url is not None:
                        if case_sensitive_url.lower() == 'no':
                            jct_json["case_insensitive_url"] = 'yes'
                        else:
                            jct_json["case_insensitive_url"] = 'no'  # default
                elif case_sensitive_url is not None:
                    jct_json['case_sensitive_url'] = case_sensitive_url

                if authz_rules is None:
                    jct_json['authz_rules'] = 'no'
                else:
                    jct_json['authz_rules'] = authz_rules
                if basic_auth_mode is None:
                    jct_json['basic_auth_mode'] = 'filter'
                else:
                    jct_json['basic_auth_mode'] = basic_auth_mode
                if client_ip_http is None or client_ip_http.lower() == 'no':
                    jct_json['client_ip_http'] = 'do not insert'
                elif client_ip_http.lower() == 'yes':
                    jct_json['client_ip_http'] = 'insert'
                else:
                    jct_json['client_ip_http'] = client_ip_http
                if not isVirtualJunction:
                  logger.debug("Only for standard junctions - {0}.".format(virtual_hostname))
                  if cookie_include_path is None:
                      jct_json['cookie_include_path'] = 'no'
                  else:
                      jct_json['cookie_include_path'] = cookie_include_path
                if isVirtualJunction and sms_environment:
                    jct_json['sms_environment'] = sms_environment
                if delegation_support is None:
                    jct_json['delegation_support'] = 'no'
                else:
                    jct_json['delegation_support'] = delegation_support
                if fsso_config_file is None or fsso_config_file == '':
                    jct_json['fsso_config_file'] = 'disabled'
                else:
                    jct_json['fsso_config_file'] = fsso_config_file
                if insert_session_cookies is None:
                    jct_json['insert_session_cookies'] = 'no'
                else:
                    jct_json['insert_session_cookies'] = insert_session_cookies
                if junction_hard_limit is None:
                    jct_json['junction_hard_limit'] = '0 - using global value'
                else:
                    jct_json['junction_hard_limit'] = str(junction_hard_limit)
                if junction_soft_limit is None:
                    jct_json['junction_soft_limit'] = '0 - using global value'
                else:
                    jct_json['junction_soft_limit'] = str(junction_soft_limit)

                if mutual_auth is None:
                    jct_json['mutual_auth'] = 'no'
                else:
                    jct_json['mutual_auth'] = mutual_auth
                if not isVirtualJunction:
                    if preserve_cookie is None:
                        jct_json['preserve_cookie'] = 'no'
                    else:
                        jct_json['preserve_cookie'] = preserve_cookie

                if remote_http_header is None or remote_http_header == []:
                    logger.debug("\nSetting remote_http_header to do not insert")
                    if not isVirtualJunction:
                        jct_json['remote_http_header'] = 'do not insert'
                else:
                   jct_json['remote_http_header'] = [_word.replace('_', '-') for _word in
                                                     list(remote_http_header)]
                # To allow for multiple header values to be sorted during compare convert retrieved data into array
                if request_encoding is None:
                    jct_json['request_encoding'] = 'utf8_uri' # utf8_bin, utf8_uri, lcp_bin, and lcp_uri
                else:
                    jct_json['request_encoding'] = request_encoding
                if scripting_support is None:
                    jct_json['scripting_support'] = 'no'
                else:
                    jct_json['scripting_support'] = scripting_support
                if stateful_junction is None:
                    jct_json['stateful_junction'] = 'no'
                else:
                    jct_json['stateful_junction'] = stateful_junction
                if tfim_sso is None:
                    jct_json['tfim_sso'] = 'no'
                else:
                    jct_json['tfim_sso'] = tfim_sso
                if transparent_path_junction is None:
                    jct_json['transparent_path_junction'] = 'no'
                else:
                    jct_json['transparent_path_junction'] = transparent_path_junction
                if isVirtualJunction:
                   logger.debug("Only for virtual junctions - virtual hostname {0}.".format(virtual_hostname))

                   if virtual_hostname:
                       jct_json['virtual_junction_hostname'] = virtual_hostname
                   else:
                       if jct_json['server_port'] in ['80', '443', 80, 443]:
                           jct_json['virtual_junction_hostname'] = jct_json['server_hostname']
                       else:
                           jct_json['virtual_junction_hostname'] = jct_json['server_hostname'] + ":" +  jct_json['server_port']
                if http2_junction is not None and http2_junction != "no":
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                        warnings.append(
                            "Appliance at version: {0}, http2_junction: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring http2_junction for this call.".format(
                                isamAppliance.facts["version"], http2_junction))
                        http2_junction = None
                    else:
                        jct_json['http2_junction'] = http2_junction
                        #if 'http2_junction' not in exist_jct:
                        #    exist_jct['http2_junction'] = jct_json['http2_junction']
                if http2_proxy is not None and http2_proxy != "no":
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                        warnings.append(
                            "Appliance at version: {0}, http2_proxy: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring http2_proxy for this call.".format(
                                isamAppliance.facts["version"], http2_proxy))
                        http2_proxy = None
                    else:
                        jct_json['http2_proxy'] = http2_proxy
                        #if 'http2_proxy' not in exist_jct:
                        #    exist_jct['http2_proxy'] = jct_json['http2_proxy']
                if sni_name is not None:
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                        warnings.append(
                            "Appliance at version: {0}, sni_name: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring sni_name for this call.".format(
                                isamAppliance.facts["version"], sni_name))
                        sni_name = None
                    else:
                        jct_json['sni_name'] = sni_name
                if description is not None:
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.7.0") < 0:
                        warnings.append(
                            "Appliance at version: {0}, description: {1} is not supported. Needs 9.0.7.0 or higher. Ignoring description for this call.".format(
                                isamAppliance.facts["version"], description))
                        description = None
                    else:
                        jct_json['description'] = description
                if isVirtualJunction and silent:
                    jct_json['silent'] = silent

            if junction_exists(isamAppliance, exist_jct, jct_json):
                add_required = False
            else:
                add_required = True
            if add_required and srvs_len > 1:
                warnings.append(
                    "Junction will be replaced. Existing multiple servers #{0} will be overwritten. Please re-add as needed.".format(
                        srvs_len))
        else:
            add_required = True

    if force or add_required:
        # Junction force add will replace the junction, no need for delete (force set to True as a result)
        return add(isamAppliance=isamAppliance, reverseproxy_id=reverseproxy_id, junction_point=junction_point,
                   server_hostname=server_hostname, server_port=server_port, junction_type=junction_type,
                   virtual_hostname=virtual_hostname, server_dn=server_dn, query_contents=query_contents,
                   stateful_junction=stateful_junction, case_sensitive_url=case_sensitive_url,
                   windows_style_url=windows_style_url, https_port=https_port, http_port=http_port,
                   proxy_hostname=proxy_hostname, proxy_port=proxy_port, sms_environment=sms_environment,
                   vhost_label=vhost_label, junction_hard_limit=junction_hard_limit,
                   junction_soft_limit=junction_soft_limit, basic_auth_mode=basic_auth_mode, tfim_sso=tfim_sso,
                   remote_http_header=remote_http_header, preserve_cookie=preserve_cookie,
                   cookie_include_path=cookie_include_path, transparent_path_junction=transparent_path_junction,
                   mutual_auth=mutual_auth, insert_session_cookies=insert_session_cookies,
                   request_encoding=request_encoding, enable_basic_auth=enable_basic_auth, key_label=key_label,
                   gso_resource_group=gso_resource_group,
                   junction_cookie_javascript_block=junction_cookie_javascript_block, client_ip_http=client_ip_http,
                   version_two_cookies=version_two_cookies, ltpa_keyfile=ltpa_keyfile, authz_rules=authz_rules,
                   fsso_config_file=fsso_config_file, username=username, password=password, server_uuid=server_uuid,
                   local_ip=local_ip, ltpa_keyfile_password=ltpa_keyfile_password,
                   delegation_support=delegation_support, scripting_support=scripting_support,
                   insert_ltpa_cookies=insert_ltpa_cookies, check_mode=check_mode, force=True,
                   http2_junction=http2_junction, http2_proxy=http2_proxy, sni_name=sni_name, description=description,
                   priority=priority, server_cn=server_cn, silent=silent,
                   case_insensitive_url=case_insensitive_url,
                   warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def compare(isamAppliance1, isamAppliance2, reverseproxy_id, reverseproxy_id2=None):
    """
    Compare list of junctions in a given reverse proxy between 2 appliances
    """
    if reverseproxy_id2 is None or reverseproxy_id2 == '':
        reverseproxy_id2 = reverseproxy_id
    ret_obj1 = get_all(isamAppliance1, reverseproxy_id)
    ret_obj2 = get_all(isamAppliance2, reverseproxy_id2)

    for jct in ret_obj1['data']:
        ret_obj = get(isamAppliance1, reverseproxy_id, jct['id'])
        del ret_obj['data']['active_worker_threads']
        for srv in ret_obj['data']['servers']:
            del srv['current_requests']
            del srv['operation_state']
            del srv['server_state']
            if ret_obj['data']['stateful_junction'] == 'no':
                del srv['server_uuid']
            del srv['total_requests']
        jct['details'] = ret_obj['data']

    for jct in ret_obj2['data']:
        ret_obj = get(isamAppliance2, reverseproxy_id2, jct['id'])
        del ret_obj['data']['active_worker_threads']
        for srv in ret_obj['data']['servers']:
            del srv['current_requests']
            del srv['operation_state']
            del srv['server_state']
            if ret_obj['data']['stateful_junction'] == 'no':
                del srv['server_uuid']
            del srv['total_requests']
        jct['details'] = ret_obj['data']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['active_worker_threads', 'servers/current_requests',
                                                                'servers/operation_state', 'servers/server_state',
                                                                'servers/server_uuid', 'servers/total_requests'])

def set_all(isamAppliance, reverseproxy_id: str, junctions: list=[], check_mode=False, force=False, warnings=[]):
    """
    Set junctions with all the servers
    The input is a list of junction objects, that can be passed to the `set` function
    The list of junctions is first compared to the output of `get_all`, so we only need to update junctions that are changed.

    :param isamAppliance:
    :param reverseproxy_id:
    :param junctions: List of junctions to set.  This is a list of dicts, with each dict representing a junction
    :param check_mode:
    :param force:
    :return:
    """
    logger = isamAppliance.logger

    currentJunctions = get_all(isamAppliance, reverseproxy_id=reverseproxy_id, detailed=True)

    __markChanged = False # use this bool to indicate if there's been a change or not.

    if currentJunctions['rc'] == 0:
        logger.debug(f"\nCurrent junctions:\n{currentJunctions}")
    else:
        # no junctions exists
        logger.debug("No junctions exist yet.  Create them all.")
        # Force create - There are no junctions yet
        # use expansion
        __markChanged = True
        for j in junctions:
            j.pop('isVirtualJunction', None)
            __firstserver = j.get('servers', [''])[0]
            for _field in list(server_fields.keys()):
                if __firstserver.get(_field, None) is not None and j.get(_field, None) is None:
                    # only use server_fields if they are not defined on junction level
                        logger.debug(f"{_field} from {__firstserver.get(_field)} copied to junction level")
                        j[_field] = __firstserver.get(_field, None)
            if len(j.get('servers', [''])) > 1:
                __servers = j.get('servers', [''])[1:]
            else:
                __servers = None
            j.pop('servers', None)
            j['force'] = True  # Force create
            set(isamAppliance, reverseproxy_id, **j)
            # Also add servers (if servers[] has more than 1 item)
            if __servers is not None:
                for s in __servers:
                    for _field, kval in server_fields.items():
                        if s.get(_field, None) is not None:
                            j[_field] = s.get(_field, None)
                    junctions_server.set(isamAppliance, reverseproxy_id, **j)
    # Compare the junctions and the currentJunctions.
    for j in junctions:
        logger.debug(f"Processing junction: {j['junction_point']}")

        _checkUpdate = False
        j['isVirtualJunction'] = True
        if j['junction_point'][:1] == '/':
            j['isVirtualJunction'] = False
        if j.get('junction_soft_limit', None) is None:
            j['junction_soft_limit'] = '0 - using global value'
        else:
           j['junction_soft_limit'] = str( j.get('junction_soft_limit', None))
        if j.get('junction_hard_limit', None) is None:
            j['junction_hard_limit'] = '0 - using global value'
        else:
           j['junction_hard_limit'] = str( j.get('junction_hard_limit', None))
        if j.get('client_ip_http', None) is None or j.get('client_ip_http', '').lower() == 'no':
            j['client_ip_http'] = 'do not insert'
        elif j.get('client_ip_http', '').lower() == 'yes':
            j['client_ip_http'] = 'insert'
        if j.get('junction_type', None) is not None:
            j['junction_type'] = j.get('junction_type', '').lower() # if junction_type is empty, rest api will fail anyway
        # update remote http header logic here
        if j.get('remote_http_header', None) is None:
            logger.debug("No remote http header")
        elif isinstance(j.get('remote_http_header', None), list):
            j['remote_http_header'] = [_word.replace('_', '-') for _word in
                                              j.get('remote_http_header', None)]
        else:
            j['remote_http_header'] = [j.get('remote_http_header', '')]

        # check that we have the required fields, if not, get them from the first server (if that exists)
        __firstserver = j.get('servers', [''])[0]
        for _field in list(server_fields.keys()):
            if __firstserver.get(_field, None) is not None and j.get(_field, None) is None:
                # only use server_fields if they are not defined on junction level
                logger.debug(f"{_field} from {__firstserver.get('server_hostname')} copied to junction level")
                j[_field] = __firstserver.get(_field, None)
        if len(j.get('servers', [''])) > 1:
            __servers = j.get('servers', [''])[1:]

        for c in currentJunctions['data']:
            servers = []
            if tools.version_compare(isamAppliance.facts["version"], "9.0.1.0") > 0:
                srv_separator = '#'
            else:
                srv_separator = '&'

            if c.get('junction_point', None) == j['junction_point']:
                if c.get('servers', None) is not None:
                    if type(c.get('servers', [])) is str:
                        srvs = c['servers'].split(srv_separator)
                        logger.debug("Servers in raw string: {0}".format(c['servers']))
                        logger.debug("Number of servers in junction: {0}".format(len(srvs)))
                        for srv in srvs:
                            logger.debug("Parsing Server: {0}".format(srv))
                            server = {}
                            for s in srv.split(';'):
                                if s != '':
                                    kv = s.split('!')
                                    server[kv[0]] = kv[1]
                            servers.append(server)
                        c['servers'] = servers
                else:
                    c['servers'] = []

                logger.debug(f"The junction at {j['junction_point']} already exists.")
                _checkUpdate = dict(c)
                break
            elif c.get('id', None) == j['junction_point']:
                logger.debug(f"The junction at {j['junction_point']} already exists (simple syntax)")
                warnings.append(f"Had to use simple get syntax unexpectedly for {j['junction_point']}")
                _checkUpdate = get(isamAppliance, reverseproxy_id, j['junction_point'], check_mode=False, force=False, warnings=warnings)
                _checkUpdate = _checkUpdate.get('data', _checkUpdate)
                if _checkUpdate.get('servers', None) is not None:
                    if type(_checkUpdate.get('servers', [])) is str:
                        srvs = _checkUpdate['servers'].split(srv_separator)
                        logger.debug("Servers in raw string: {0}".format(_checkUpdate['servers']))
                        logger.debug("Number of servers in junction: {0}".format(len(srvs)))
                        for srv in srvs:
                            logger.debug("Parsing Server: {0}".format(srv))
                            server = {}
                            for s in srv.split(';'):
                                if s != '':
                                    kv = s.split('!')
                                    server[kv[0]] = kv[1]
                            servers.append(server)
                        _checkUpdate['servers'] = servers
                else:
                    _checkUpdate['servers'] = []
                break

        if _checkUpdate:
            __firstserver = j.get('servers', [''])[0]
            for _field in list(server_fields.keys()):
                if __firstserver.get(_field, None) is not None and j.get(_field, None) is None:
                    # only use server_fields if they are not defined on junction level
                    logger.debug(f"{_field} from {__firstserver.get('server_hostname')} copied to junction level")
                    j[_field] = __firstserver.get(_field, None)
            if not junction_exists(isamAppliance, _checkUpdate, j):
                __markChanged = True
                # Run set()
                logger.debug("\n\nUpdate junction\n\n")
                warnings.append(f"Instance {reverseproxy_id}: Updating junction {j['junction_point']}")
                j['force'] = True  # force create
                j['warnings'] = warnings
                j.pop('isVirtualJunction', None)
                __result = set(isamAppliance, reverseproxy_id, **j)
                logger.debug(f"Adding servers")
                # Also add servers (if servers[] has more than 1 item)
                if len(j.get('servers', [''])) > 1:
                    j.pop('servers', None)
                    for s in __servers:
                        for _field, kval in server_fields.items():
                            if s.get(_field, None) is not None:
                                j[_field] = s.get(_field, None)
                        junctions_server.set(isamAppliance, reverseproxy_id, **j)
            else:
                logger.debug(f"\n\n{reverseproxy_id}: Junction {j.get('junction_point','')} does not need updating\n\n")
                warnings.append(f"Instance {reverseproxy_id}: Junction {j.get('junction_point','')} does not need updating")
        else:
            # Force create - this junction does not exist yet
            j.pop('isVirtualJunction', None)
            j['force'] = True # force create
            __markChanged = True
            j['warnings'] = warnings
            __firstserver = j.get('servers', [''])[0]
            for _field in list(server_fields.keys()):
                if __firstserver.get(_field, None) is not None and j.get(_field, None) is None:
                    # only use server_fields if they are not defined on junction level
                        logger.debug(f"{_field} from {__firstserver.get('server_hostname')} copied to junction level")
                        j[_field] = __firstserver.get(_field, None)
            logger.debug(f"Creating new junction with {j}")
            set(isamAppliance, reverseproxy_id, **j)
            logger.debug(f"Adding servers")
            # Also add servers (if servers[] has more than 1 item)
            if len(j.get('servers', [''])) > 1:
                __servers = j.get('servers', [''])[1:]
                j.pop('servers', None)
                for s in __servers:
                    for _field, kval in server_fields.items():
                        if s.get(_field, None) is not None:
                            j[_field] = s.get(_field, None)
                    junctions_server.set(isamAppliance, reverseproxy_id, **j)
    if __markChanged:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        return isamAppliance.create_return_object(warnings=warnings)


def junction_server_exists(isamAppliance, srvs, server_hostname: str, server_port, case_sensitive_url: str='yes',
                         isVirtualJunction=False, http_port=None, local_ip=None,
                         query_contents=None, server_dn=None,
                         server_uuid=None, virtual_hostname=None, windows_style_url=None, priority=None, server_cn=None, case_insensitive_url: str='no', **kwargs) -> bool:
  server_found = False
  for srv in srvs:
    if srv['server_hostname'] == server_hostname and str(srv['server_port']) == str(server_port):
        logger.debug("Matched a server - {0}.".format(srv))
        server_found = True
        server_json = {
            'server_hostname': server_hostname,
            'server_port': str(server_port)
        }

        if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
            # If no case_insensitive_url is passed, we take the old one and invert it.
            # Who thinks it's a good idea to make changes in an API like this ?
            if case_insensitive_url is not None:
                server_json["case_insensitive_url"] = case_insensitive_url
            elif case_sensitive_url is not None:
                if case_sensitive_url.lower() == 'no':
                    server_json["case_insensitive_url"] = 'yes'
                else:
                    server_json["case_insensitive_url"] = 'no'  # default
        elif case_sensitive_url is not None:
            server_json['case_sensitive_url'] = case_sensitive_url
        else:
            server_json['case_sensitive_url'] = 'yes'

        if http_port is None:
            server_json['http_port'] = str(server_port)
        else:
            server_json['http_port'] = str(http_port)
        if local_ip is None:
            server_json['local_ip'] = ''
        else:
            server_json['local_ip'] = local_ip
        if query_contents is None or query_contents == '':
            server_json['query_content_url'] = '/cgi-bin/query_contents'
        else:
            server_json['query_content_url'] = query_contents
        if server_dn is None:
            server_json['server_dn'] = ''
        else:
            server_json['server_dn'] = server_dn
        if server_uuid is not None:
            server_json['server_uuid'] = server_uuid
        else:
            # Server UUID gets generated if not specified
            srv.pop('server_uuid', None)
        if not isVirtualJunction:
            if virtual_hostname is not None:
                logger.debug("Only for standard junctions - {0}.".format(virtual_hostname))
                server_json['virtual_junction_hostname'] = virtual_hostname
            else:
                if server_json['server_port'] in ['80', 80]:
                    server_json['virtual_junction_hostname'] = server_json['server_hostname']
                else:
                    server_json['virtual_junction_hostname'] = server_json['server_hostname'] + ":" + server_json[
                        'server_port']
            if 'virtual_junction_hostname' not in srv:
                # this is not in the returned servers object for virtual host junctions, it's in the junction's object
                if virtual_hostname is not None:
                    srv['virtual_junction_hostname'] = virtual_hostname
                else:
                    if srv['server_port'] in ['80', '443', 80, 443]:
                        srv['virtual_junction_hostname'] = srv['server_hostname']
                    else:
                        srv['virtual_junction_hostname'] = 'fuckoff' # srv['server_hostname'] + ":" + srv['server_port']
        if windows_style_url is None:
            server_json['windows_style_url'] = 'no'
        else:
            server_json['windows_style_url'] = windows_style_url
        # v10.0.2
        if tools.version_compare(isamAppliance.facts["version"], "10.0.2.0") >= 0:
            if priority is None:
                server_json['priority'] = '9'
            else:
                server_json['priority'] = str(priority)
            if server_cn is None:
                server_json['server_cn'] = ''
            else:
                server_json['server_cn'] = server_cn

        srv = {k: v for k, v in srv.items() if k in server_json.keys()}

        current_servers = json.dumps(srv, skipkeys=True, sort_keys=True)
        new_servers = json.dumps(server_json, skipkeys=True, sort_keys=True)
        if current_servers != new_servers:
            logger.debug("\n\nServers are found to be different. See following JSON for difference.\n\n")
        else:
            logger.debug("\n\nServers are the same.  See comparison below.\n\n")
        logger.debug(f"\nNew Server JSON: {new_servers}")
        logger.debug(f"\nOld Server JSON: {current_servers}")
        break
  return server_found

def junction_exists(isamAppliance, exist_jct, new_j):
    # perform a comparison.  we receive the actual current junction as input here
    __srvs = exist_jct.get('servers', None)
    new_j.pop('isVirtualJunction', None)
    logger.debug(f"\n\nServers in junction {new_j['junction_point']}:\n{__srvs}")
    __result = True
    if __srvs is not None and not junction_server_exists(isamAppliance, __srvs, **new_j):
        __result = False
    if __result:
        # ok we still need to compare
        # exist_jct = dict(_checkUpdate)
        new_jct = dict(new_j)
        # remove the server fields - this has already been compared
        for _field, kval in server_fields.items():
            new_jct.pop(_field, None)
        # junction_type
        if exist_jct.get('junction_type', None) is not None:
            exist_jct['junction_type'] = exist_jct.get('junction_type', '').lower()
        # insert_ltpa_cookies
        if exist_jct.get('insert_ltpa_cookies', None) is None:
            exist_jct['insert_ltpa_cookies'] = 'no'
        # sms_environment
        if exist_jct.get('sms_environment', None) is None:
            exist_jct['sms_environment'] = ""
        # vhost_label
        if exist_jct.get('vhost_label', None) is None:
            exist_jct['vhost_label'] = ""
        # request_encoding utf8_bin, utf8_uri, lcp_bin, and lcp_uri.
        __re = exist_jct.get('request_encoding', None)
        if __re is not None:
            if __re == 'UTF-8, URI Encoded':
                exist_jct['request_encoding'] = 'utf8_uri'
            elif __re == 'UTF-8, Binary':
                exist_jct['request_encoding'] = 'utf8_bin'
            elif __re == 'Local Code Page, Binary':
                exist_jct['request_encoding'] = 'lcp_bin'
            elif __re == 'Local Code Page, URI Encoded':
                exist_jct['request_encoding'] = 'lcp_uri'

        # To allow for multiple header values to be sorted during compare convert retrieved data into array
        __rehh = exist_jct.get('remote_http_header', None)
        if __rehh is not None:
            if __rehh.startswith('insert - '):
                exist_jct['remote_http_header'] = [_word.replace('_', '-') for _word in (__rehh[9:]).split(' ')]
            # now see if it's actually 'all' - to do that, compare with string ["iv-creds", "iv-groups", "iv-user"]
            __nrehh = json.dumps(exist_jct.get('remote_http_header', None), skipkeys=True, sort_keys=True, cls=jsonSortedListEncoder)
            logger.debug(f"Sorted string content of remote_http_header {__nrehh}")
            if __nrehh == '["iv-creds", "iv-groups", "iv-user"]':
                exist_jct['remote_http_header'] = ['all']
            if __nrehh.replace('"', '') == "do not insert":
                exist_jct['remote_http_header'] = []

        # scripting support default
        __scripting_support = exist_jct.get('scripting_support', None)
        if __scripting_support is None:
            exist_jct['scripting_support'] = 'no'

        # scripting support default
        __transparent_path_junction = exist_jct.get('transparent_path_junction', None)
        if __transparent_path_junction is None:
            exist_jct['transparent_path_junction'] = 'no'

        # basic_auth_mode - filter (default), ignore, supply, gso.
        __bamode = exist_jct.get('basic_auth_mode', None)
        if __bamode is not None:
            # GSO
            if __bamode == "use GSO":
                exist_jct['basic_auth_mode'] = 'gso'

        # Remove servers field for comparing
        new_jct.pop("servers", None)
        # only compare values that are in the new request
        # This does not (always) compare values correctly where you just remove the key.  In that case, you'd have to change a different key as well (eg. description)
        exist_jct = {k: v for k, v in exist_jct.items() if k in new_jct.keys()}

        newJSON = json.dumps(new_jct, skipkeys=True, sort_keys=True, cls=jsonSortedListEncoder)
        logger.debug(f"\nSorted Desired  Junction {new_j['junction_point']}:\n\n {newJSON}\n")

        oldJSON = json.dumps(exist_jct, skipkeys=True, sort_keys=True, cls=jsonSortedListEncoder)
        logger.debug(f"\nSorted Current  Junction {exist_jct.get('junction_point', '')}:\n\n {oldJSON}\n")

        if newJSON != oldJSON:
            logger.debug("Junctions are found to be different. See JSON for difference.")
            __result = False
    return __result
