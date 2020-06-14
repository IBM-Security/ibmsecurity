import logging
from ibmsecurity.utilities import tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/reverseproxy"
requires_modules = ["wga"]
requires_version = None


def get_all(isamAppliance, reverseproxy_id, check_mode=False, force=False):
    """
    Retrieving a list of standard and virtual junctions

    :param isamAppliance:
    :param reverseproxy_id:
    :param check_mode:
    :param force:
    :return:
    """
    return isamAppliance.invoke_get("Retrieving a list of standard and virtual junctions",
                                    "{0}/{1}/junctions".format(uri, reverseproxy_id),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get(isamAppliance, reverseproxy_id, junctionname, check_mode=False, force=False):
    """
    Retrieving the parameters for a single standard or virtual junction

    :param isamAppliance:
    :param reverseproxy_id:
    :param junctionname:
    :param check_mode:
    :param force:
    :return:
    """
    ret_obj = isamAppliance.invoke_get("Retrieving the parameters for a single standard or virtual junction",
                                       "{0}/{1}/junctions?junctions_id={2}".format(uri, reverseproxy_id,
                                                                                   junctionname),
                                       requires_modules=requires_modules,
                                       requires_version=requires_version)
    # servers are provided as a single string, here we parse it out into a list + dict
    servers = []
    if tools.version_compare(isamAppliance.facts["version"], "9.0.1.0") > 0:
        srv_separator = '#'
    else:
        srv_separator = '&'
    logger.debug("Server Separator being used: {0}".format(srv_separator))
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


def _check(isamAppliance, reverseproxy_id, junctionname):
    ret_obj = get_all(isamAppliance, reverseproxy_id)

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
        http2_junction=None, http2_proxy=None, sni_name=None, description=None, warnings=[]):
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
    :return:
    """
    if force is True or _check(isamAppliance, reverseproxy_id, junction_point) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            # Create a simple json with just the main junction attributes
            jct_json = {
                "junction_point": junction_point,
                "junction_type": junction_type,
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
            if preserve_cookie is not None:
                jct_json["preserve_cookie"] = preserve_cookie
            if cookie_include_path is not None:
                jct_json["cookie_include_path"] = cookie_include_path
            if transparent_path_junction is not None:
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
            if case_sensitive_url is not None:
                jct_json["case_sensitive_url"] = case_sensitive_url
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
            if sms_environment is not None:
                jct_json["sms_environment"] = sms_environment
            if vhost_label is not None:
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
        http2_junction=None, http2_proxy=None, sni_name=None, description=None):
    """
    Setting a standard or virtual junction - compares with existing junction and replaces if changes are detected
    TODO: Compare all the parameters in the function - LTPA, BA are some that are not being compared
    """
    warnings = []
    add_required = False
    if force is False:
        # Check if record exists
        logger.debug("Check if the junction exists.")
        if _check(isamAppliance, reverseproxy_id, junction_point) is True:
            logger.debug("Junction exists. Compare junction details.")
            ret_obj = get(isamAppliance, reverseproxy_id=reverseproxy_id, junctionname=junction_point)
            server_found = False
            logger.debug("See if the backend junction server matches any on the junction. Look for just one match.")
            srvs = ret_obj['data']['servers']
            srvs_len = len(srvs)
            for srv in srvs:
                if srv['server_hostname'] == server_hostname and str(srv['server_port']) == str(server_port):
                    logger.debug("Matched a server - {0}.".format(srv))
                    server_found = True
                    server_json = {
                        'server_hostname': server_hostname,
                        'server_port': str(server_port)
                    }
                    if case_sensitive_url is None:
                        server_json['case_sensitive_url'] = 'no'
                    else:
                        server_json['case_sensitive_url'] = case_sensitive_url
                    if http_port is None:
                        server_json['http_port'] = str(server_port)
                    else:
                        server_json['http_port'] = str(http_port)
                    if local_ip is None:
                        server_json['local_ip'] = ''
                    else:
                        server_json['local_ip'] = local_ip
                    if query_contents is None:
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
                        if 'server_uuid' in srv:
                            del srv['server_uuid']
                    if virtual_hostname is None:
                        if 'virtual_junction_hostname' in srv:
                            del srv['virtual_junction_hostname']
                    else:
                        server_json['virtual_junction_hostname'] = virtual_hostname
                    if windows_style_url is None:
                        server_json['windows_style_url'] = 'no'
                    else:
                        server_json['windows_style_url'] = windows_style_url

                    # Delete dynamic data shown when we get junctions details
                    if 'current_requests' in srv:
                        del srv['current_requests']
                    if 'total_requests' in srv:
                        del srv['total_requests']
                    if 'operation_state' in srv:
                        del srv['operation_state']
                    if 'server_state' in srv:
                        del srv['server_state']
                    # Not sure what this attribute is supposed to contain?
                    if 'query_contents' in srv:
                        del srv['query_contents']
                    if tools.json_sort(server_json) != tools.json_sort(srv):
                        logger.debug("Servers are found to be different. See following JSON for difference.")
                        logger.debug("New Server JSON: {0}".format(tools.json_sort(server_json)))
                        logger.debug("Old Server JSON: {0}".format(tools.json_sort(srv)))
                        add_required = True
                    break
            if server_found is False:
                add_required = True
            elif add_required is False:
                exist_jct = ret_obj['data']
                jct_json = {
                    'junction_point': junction_point,
                    'junction_type': junction_type.upper()
                }
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
                if cookie_include_path is None:
                    jct_json['cookie_include_path'] = 'no'
                else:
                    jct_json['cookie_include_path'] = cookie_include_path
                if delegation_support is None:
                    jct_json['delegation_support'] = 'no'
                else:
                    jct_json['delegation_support'] = delegation_support
                if fsso_config_file is None:
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
                # We could have a comma delimited set of values - so split them into array
                if junction_cookie_javascript_block is not None and junction_cookie_javascript_block != '':
                    jct_json['junction_cookie_javascript_block'] = junction_cookie_javascript_block.split(',')
                    # Here the list is delimited by space
                    if 'junction_cookie_javascript_block' in exist_jct and exist_jct[
                        'junction_cookie_javascript_block'] is not None:
                        exist_jct['junction_cookie_javascript_block'] = exist_jct[
                            'junction_cookie_javascript_block'].split(' ')
                if mutual_auth is None:
                    jct_json['mutual_auth'] = 'no'
                else:
                    jct_json['mutual_auth'] = mutual_auth
                if preserve_cookie is None:
                    jct_json['preserve_cookie'] = 'no'
                else:
                    jct_json['preserve_cookie'] = preserve_cookie
                if remote_http_header is None or remote_http_header == []:
                    jct_json['remote_http_header'] = 'do not insert'
                elif isinstance(remote_http_header, basestring) and remote_http_header.lower() == 'all':
                    jct_json['remote_http_header'] = ['iv_creds', 'iv_groups', 'iv_user']
                else:
                    jct_json['remote_http_header'] = remote_http_header
                # To allow for multiple header values to be sorted during compare convert retrieved data into array
                if exist_jct['remote_http_header'].startswith('insert - '):
                    exist_jct['remote_http_header'] = (exist_jct['remote_http_header'][9:]).split(' ')
                if request_encoding is None:
                    jct_json['request_encoding'] = 'UTF-8, URI Encoded'
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
                if http2_junction is not None:
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                        warnings.append(
                            "Appliance at version: {0}, http2_junction: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring http2_junction for this call.".format(
                                isamAppliance.facts["version"], http2_junction))
                        http2_junction = None
                    else:
                        jct_json['http2_junction'] = http2_junction
                if http2_proxy is not None:
                    if tools.version_compare(isamAppliance.facts["version"], "9.0.4.0") < 0:
                        warnings.append(
                            "Appliance at version: {0}, http2_proxy: {1} is not supported. Needs 9.0.4.0 or higher. Ignoring http2_proxy for this call.".format(
                                isamAppliance.facts["version"], http2_proxy))
                        http2_proxy = None
                    else:
                        jct_json['http2_proxy'] = http2_proxy
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

                # TODO: Not sure of how to match following attributes! Need to revisit.
                # TODO: Not all function parameters are being checked - need to add!
                del exist_jct['boolean_rule_header']
                del exist_jct['forms_based_sso']
                del exist_jct['http_header_ident']
                del exist_jct['session_cookie_backend_portal']
                # We are already comparing server details - so remove this from this compare
                del exist_jct['servers']
                # Delete dynamic data shown when we get junctions details
                del exist_jct['active_worker_threads']
                if tools.json_sort(jct_json) != tools.json_sort(exist_jct):
                    logger.debug("Junctions are found to be different. See following JSON for difference.")
                    logger.debug("New Junction JSON: {0}".format(tools.json_sort(jct_json)))
                    logger.debug("Old Junction JSON: {0}".format(tools.json_sort(exist_jct)))
                    add_required = True
            if add_required is True and srvs_len > 1:
                warnings.append(
                    "Junction will replaced. Existing multiple servers #{0} will be overwritten. Please re-add as needed.".format(
                        srvs_len))
        else:
            add_required = True

    if force is True or add_required is True:
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
                   http2_junction=http2_junction, http2_proxy=http2_proxy, sni_name=sni_name, description=description, warnings=warnings)

    return isamAppliance.create_return_object()


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
