import logging
import os

import ibmsecurity
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/resource/instance"
requires_modules = ["wga"]
requires_version = "9.0.7"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get_all(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Retrieve a list of all API Access Control Resource Servers
    """
    return isamAppliance.invoke_get("Retrieve a list of all API Access Control Resource Servers",
                                    "{0}/{1}/server".format(uri, instance_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, instance_name, resource_server_name, check_mode=False, force=False):
    """
    Retrieve a single API Access Control Resource Server
    """
    return isamAppliance.invoke_get("Retrieve a single API Access Control Resource Server",
                                    "{0}/{1}/server{2}".format(uri, instance_name, resource_server_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add(isamAppliance, instance_name, server_hostname, junction_point, junction_type, policy, authentication,
        static_response_headers=None, jwt=None, junction_hard_limit=None, junction_soft_limit=None,
        basic_auth_mode=None, tfim_sso=None, remote_http_header=None, stateful_junction=None,
        http2_junction=None, http2_proxy=None, sni_name=None, preserve_cookie=None, cookie_include_path=None,
        transparent_path_junction=None, mutual_auth=None, insert_ltpa_cookies=None,
        insert_session_cookies=None, request_encoding=None, enable_basic_auth=None, key_label=None,
        gso_resource_group=None, junction_cookie_javascript_block=None, client_ip_http=None,
        version_two_cookies=None, ltpa_keyfile=None, authz_rules=None, fsso_config_file=None, username=None,
        password=None, server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None, local_ip=None,
        query_contents=None, case_sensitive_url=None, windows_style_url=None, ltpa_keyfile_password=None,
        https_port=None, http_port=None, proxy_hostname=None, proxy_port=None, sms_environment=None,
        vhost_label=None, junction_force=None, delegation_support=None, scripting_support=None,
        case_insensitive_url=None,
        check_mode=False, force=False):
    """
    Creating a new API Access Control Resource Server
    """
    server_exist, warnings = _check_server_exist(isamAppliance, instance_name, junction_point)

    if force is True or server_exist is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                'instance_name': instance_name,
                'server_hostname': server_hostname,
                'junction_point': junction_point,
                'junction_type': junction_type,
                'policy': policy,
                'authentication': authentication
            }
            if static_response_headers is not None:
                json_data['static_response_headers'] = static_response_headers

            if jwt is not None:
                json_data['jwt'] = jwt

            if junction_hard_limit is not None:
                json_data['junction_hard_limit'] = junction_hard_limit

            if junction_soft_limit is not None:
                json_data['junction_soft_limit'] = junction_soft_limit

            if basic_auth_mode is not None:
                json_data['basic_auth_mode'] = basic_auth_mode

            if tfim_sso is not None:
                json_data['tfim_sso'] = tfim_sso

            if remote_http_header is not None:
                json_data['remote_http_header'] = remote_http_header

            if stateful_junction is not None:
                json_data['stateful_junction'] = stateful_junction

            if http2_junction is not None:
                json_data['http2_junction']

            if http2_proxy is not None:
                json_data['http2_proxy'] = http2_proxy

            if sni_name is not None:
                json_data['sni_name'] = sni_name

            if preserve_cookie is not None:
                json_data['preserve_cookie'] = preserve_cookie

            if cookie_include_path is not None:
                json_data['cookie_include_path'] = cookie_include_path

            if transparent_path_junction is not None:
                json_data['transparent_path_junction'] = transparent_path_junction

            if mutual_auth is not None:
                json_data['mutual_auth'] = mutual_auth

            if insert_ltpa_cookies is not None:
                json_data['insert_ltpa_cookies'] = insert_ltpa_cookies

            if insert_session_cookies is not None:
                json_data['insert_session_cookies'] = insert_session_cookies

            if request_encoding is not None:
                json_data['request_encoding'] = request_encoding

            if enable_basic_auth is not None:
                json_data['enable_basic_auth'] = enable_basic_auth

            if key_label is not None:
                json_data['key_label'] = key_label

            if gso_resource_group is not None:
                json_data['gso_resource_group'] = gso_resource_group

            if junction_cookie_javascript_block is not None:
                json_data['junction_cookie_javascript_block'] = junction_cookie_javascript_block

            if client_ip_http is not None:
                json_data['client_ip_http'] = client_ip_http

            if version_two_cookies is not None:
                json_data['version_two_cookies'] = version_two_cookies

            if ltpa_keyfile is not None:
                json_data[ltpa_keyfile] = ltpa_keyfile

            if authz_rules is not None:
                json_data['authz_rules'] = authz_rules

            if fsso_config_file is not None:
                json_data['fsso_config_file'] = fsso_config_file

            if username is not None:
                json_data['username'] = username

            if password is not None:
                json_data['password'] = password

            if server_uuid is not None:
                json_data['server_uuid'] = server_uuid

            if server_port is not None:
                json_data['server_port'] = server_port

            if virtual_hostname is not None:
                json_data['virtual_hostname'] = virtual_hostname

            if server_dn is not None:
                json_data['server_dn'] = server_dn

            if local_ip is not None:
                json_data['local_ip'] = local_ip

            if query_contents is not None:
                json_data['query_contents'] = query_contents

            if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
                # If no case_insensitive_url is passed, we take the old one and invert it.
                # Who thinks it's a good idea to make changes in an API like this ?
                if case_insensitive_url is not None:
                    json_data["case_insensitive_url"] = case_insensitive_url
                elif case_sensitive_url is not None:
                    if case_sensitive_url.lower() == 'yes':
                        jct_srv_json["case_insensitive_url"] = 'no'
                    else:
                        jct_srv_json["case_insensitive_url"] = 'yes'
            elif case_sensitive_url is not None:
                json_data['case_sensitive_url'] = case_sensitive_url

            if windows_style_url is not None:
                json_data['windows_style_url'] = windows_style_url

            if ltpa_keyfile_password is not None:
                json_data['ltpa_keyfile_password'] = ltpa_keyfile_password

            if https_port is not None:
                json_data['https_port'] = https_port

            if http_port is not None:
                json_data['http_port'] = http_port

            if proxy_hostname is not None:
                json_data['proxy_hostname'] = proxy_hostname

            if proxy_port is not None:
                json_data['proxy_port'] = proxy_port

            if sms_environment is not None:
                json_data['sms_environment'] = sms_environment

            if vhost_label is not None:
                json_data['vhost_label'] = vhost_label

            if junction_force is not None:
                json_data['force'] = junction_force

            if delegation_support is not None:
                json_data['delegation_support'] = delegation_support

            if scripting_support is not None:
                json_data['scripting_support'] = scripting_support

            return isamAppliance.invoke_post(
                "Creating a new API Access Control Resource Server",
                "{0}/{1}/server".format(uri, instance_name),
                json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def update(isamAppliance, instance_name, junction_point, server_hostname, junction_type,
           policy, authentication, server_type="standard", static_response_headers=None, jwt=None,
           junction_hard_limit=None, junction_soft_limit=None, basic_auth_mode=None, tfim_sso=None,
           remote_http_header=None, stateful_junction=None, http2_junction=None, http2_proxy=None,
           sni_name=None, preserve_cookie=None, cookie_include_path=None, transparent_path_junction=None,
           mutual_auth=None, insert_ltpa_cookies=None, insert_session_cookies=None, request_encoding=None,
           enable_basic_auth=None, key_label=None, gso_resource_group=None,
           junction_cookie_javascript_block=None, client_ip_http=None, version_two_cookies=None,
           ltpa_keyfile=None, authz_rules=None, fsso_config_file=None, username=None, password=None,
           server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None, local_ip=None,
           query_contents=None, case_sensitive_url=None, windows_style_url=None, ltpa_keyfile_password=None,
           https_port=None, http_port=None, proxy_hostname=None, proxy_port=None, sms_environment=None,
           vhost_label=None, junction_force=True, delegation_support=None, scripting_support=None,
           case_insensitive_url=None,
           check_mode=False, force=False):
    """
    Updating an existing API Access Control Resource Server
    """

    server_exist, warnings = _check_server_exist(isamAppliance, instance_name, junction_point)
    if server_exist is True:
        update_required, warnings = _check_server_content(isamAppliance=isamAppliance,
                                                          instance_name=instance_name,
                                                          junction_point=junction_point,
                                                          server_hostname=server_hostname,
                                                          junction_type=junction_type, policy=policy,
                                                          authentication=authentication,
                                                          static_response_headers=static_response_headers,
                                                          jwt=jwt,
                                                          junction_hard_limit=junction_hard_limit,
                                                          junction_soft_limit=junction_soft_limit,
                                                          basic_auth_mode=basic_auth_mode,
                                                          tfim_sso=tfim_sso,
                                                          remote_http_header=remote_http_header,
                                                          stateful_junction=stateful_junction,
                                                          http2_junction=http2_junction,
                                                          http2_proxy=http2_proxy, sni_name=sni_name,
                                                          preserve_cookie=preserve_cookie,
                                                          cookie_include_path=cookie_include_path,
                                                          transparent_path_junction=transparent_path_junction,
                                                          mutual_auth=mutual_auth,
                                                          insert_ltpa_cookies=insert_ltpa_cookies,
                                                          insert_session_cookies=insert_session_cookies,
                                                          request_encoding=request_encoding,
                                                          enable_basic_auth=enable_basic_auth,
                                                          key_label=key_label,
                                                          gso_resource_group=gso_resource_group,
                                                          junction_cookie_javascript_block=junction_cookie_javascript_block,
                                                          client_ip_http=client_ip_http,
                                                          version_two_cookies=version_two_cookies,
                                                          ltpa_keyfile=ltpa_keyfile, authz_rules=authz_rules,
                                                          fsso_config_file=fsso_config_file,
                                                          username=username,
                                                          password=password,
                                                          server_uuid=server_uuid, server_port=server_port,
                                                          virtual_hostname=virtual_hostname,
                                                          server_dn=server_dn,
                                                          local_ip=local_ip, query_contents=query_contents,
                                                          case_sensitive_url=case_sensitive_url,
                                                          case_insensitive_url=case_insensitive_url,
                                                          windows_style_url=windows_style_url,
                                                          ltpa_keyfile_password=ltpa_keyfile_password,
                                                          https_port=https_port,
                                                          http_port=http_port, proxy_hostname=proxy_hostname,
                                                          proxy_port=proxy_port,
                                                          sms_environment=sms_environment,
                                                          vhost_label=vhost_label,
                                                          delegation_support=delegation_support,
                                                          scripting_support=scripting_support)

    else:
        return isamAppliance.create_return_object(warnings=warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                'instance_name': instance_name,
                'server_hostname': server_hostname,
                'junction_point': junction_point,
                'junction_type': junction_type,
                'policy': policy,
                'authentication': authentication
            }
            if static_response_headers is not None:
                json_data['static_response_headers'] = static_response_headers

            if jwt is not None:
                json_data['jwt'] = jwt

            if junction_hard_limit is not None:
                json_data['junction_hard_limit'] = junction_hard_limit

            if junction_soft_limit is not None:
                json_data['junction_soft_limit'] = junction_soft_limit

            if basic_auth_mode is not None:
                json_data['basic_auth_mode'] = basic_auth_mode

            if tfim_sso is not None:
                json_data['tfim_sso'] = tfim_sso

            if remote_http_header is not None:
                json_data['remote_http_header'] = remote_http_header

            if stateful_junction is not None:
                json_data['stateful_junction'] = stateful_junction

            if http2_junction is not None:
                json_data['http2_junction']

            if http2_proxy is not None:
                json_data['http2_proxy'] = http2_proxy

            if sni_name is not None:
                json_data['sni_name'] = sni_name

            if preserve_cookie is not None:
                json_data['preserve_cookie'] = preserve_cookie

            if cookie_include_path is not None:
                json_data['cookie_include_path'] = cookie_include_path

            if transparent_path_junction is not None:
                json_data['transparent_path_junction'] = transparent_path_junction

            if mutual_auth is not None:
                json_data['mutual_auth'] = mutual_auth

            if insert_ltpa_cookies is not None:
                json_data['insert_ltpa_cookies'] = insert_ltpa_cookies

            if insert_session_cookies is not None:
                json_data['insert_session_cookies'] = insert_session_cookies

            if request_encoding is not None:
                json_data['request_encoding'] = request_encoding

            if enable_basic_auth is not None:
                json_data['enable_basic_auth'] = enable_basic_auth

            if key_label is not None:
                json_data['key_label'] = key_label

            if gso_resource_group is not None:
                json_data['gso_resource_group'] = gso_resource_group

            if junction_cookie_javascript_block is not None:
                json_data['junction_cookie_javascript_block'] = junction_cookie_javascript_block

            if client_ip_http is not None:
                json_data['client_ip_http'] = client_ip_http

            if version_two_cookies is not None:
                json_data['version_two_cookies'] = version_two_cookies

            if ltpa_keyfile is not None:
                json_data[ltpa_keyfile] = ltpa_keyfile

            if authz_rules is not None:
                json_data['authz_rules'] = authz_rules

            if fsso_config_file is not None:
                json_data['fsso_config_file'] = fsso_config_file

            if username is not None:
                json_data['username'] = username

            if password is not None:
                json_data['password'] = password

            if server_uuid is not None:
                json_data['server_uuid'] = server_uuid

            if server_port is not None:
                json_data['server_port'] = server_port

            if virtual_hostname is not None:
                json_data['virtual_hostname'] = virtual_hostname

            if server_dn is not None:
                json_data['server_dn'] = server_dn

            if local_ip is not None:
                json_data['local_ip'] = local_ip

            if query_contents is not None:
                json_data['query_contents'] = query_contents

            if tools.version_compare(isamAppliance.facts["version"], "10.0.6.0") >= 0:
                # If no case_insensitive_url is passed, we take the old one and invert it.
                # Who thinks it's a good idea to make changes in an API like this ?
                if case_insensitive_url is not None:
                    json_data["case_insensitive_url"] = case_insensitive_url
                elif case_sensitive_url is not None:
                    if case_sensitive_url.lower() == 'yes':
                        json_data["case_insensitive_url"] = 'no'
                    else:
                        json_data["case_insensitive_url"] = 'yes'
            elif case_sensitive_url is not None:
                json_data['case_sensitive_url'] = case_sensitive_url

            if windows_style_url is not None:
                json_data['windows_style_url'] = windows_style_url

            if ltpa_keyfile_password is not None:
                json_data['ltpa_keyfile_password'] = ltpa_keyfile_password

            if https_port is not None:
                json_data['https_port'] = https_port

            if http_port is not None:
                json_data['http_port'] = http_port

            if proxy_hostname is not None:
                json_data['proxy_hostname'] = proxy_hostname

            if proxy_port is not None:
                json_data['proxy_port'] = proxy_port

            if sms_environment is not None:
                json_data['sms_environment'] = sms_environment

            if vhost_label is not None:
                json_data['vhost_label'] = vhost_label

            if junction_force is not None:
                json_data['force'] = junction_force

            if delegation_support is not None:
                json_data['delegation_support'] = delegation_support

            if scripting_support is not None:
                json_data['scripting_support'] = scripting_support

            return isamAppliance.invoke_put(
                "Updating an existing API Access Control Resource Server",
                "{0}/{1}/server{2}?{3}".format(uri, instance_name, junction_point, server_type),
                json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set(isamAppliance, instance_name, junction_point, server_hostname, junction_type,
        policy, authentication, server_type="standard", static_response_headers=None, jwt=None,
        junction_hard_limit=None, junction_soft_limit=None, basic_auth_mode=None, tfim_sso=None,
        remote_http_header=None, stateful_junction=None, http2_junction=None, http2_proxy=None,
        sni_name=None, preserve_cookie=None, cookie_include_path=None, transparent_path_junction=None,
        mutual_auth=None, insert_ltpa_cookies=None, insert_session_cookies=None, request_encoding=None,
        enable_basic_auth=None, key_label=None, gso_resource_group=None,
        junction_cookie_javascript_block=None, client_ip_http=None, version_two_cookies=None,
        ltpa_keyfile=None, authz_rules=None, fsso_config_file=None, username=None, password=None,
        server_uuid=None, server_port=None, virtual_hostname=None, server_dn=None, local_ip=None,
        query_contents=None, case_sensitive_url=None, windows_style_url=None, ltpa_keyfile_password=None,
        https_port=None, http_port=None, proxy_hostname=None, proxy_port=None, sms_environment=None,
        vhost_label=None, junction_force=True, delegation_support=None, scripting_support=None,
        case_insensitive_url=None,
        check_mode=False, force=False):
    server_exist, warnings = _check_server_exist(isamAppliance, instance_name, junction_point)

    if server_exist is True:
        return update(isamAppliance=isamAppliance, instance_name=instance_name, junction_point=junction_point,
                      server_hostname=server_hostname, junction_type=junction_type, policy=policy,
                      authentication=authentication, server_type=server_type,
                      static_response_headers=static_response_headers, jwt=jwt,
                      junction_hard_limit=junction_hard_limit,
                      junction_soft_limit=junction_soft_limit, basic_auth_mode=basic_auth_mode,
                      tfim_sso=tfim_sso, remote_http_header=remote_http_header,
                      stateful_junction=stateful_junction, http2_junction=http2_junction,
                      http2_proxy=http2_proxy, sni_name=sni_name, preserve_cookie=preserve_cookie,
                      cookie_include_path=cookie_include_path,
                      transparent_path_junction=transparent_path_junction, mutual_auth=mutual_auth,
                      insert_ltpa_cookies=insert_ltpa_cookies, insert_session_cookies=insert_session_cookies,
                      request_encoding=request_encoding, enable_basic_auth=enable_basic_auth,
                      key_label=key_label, gso_resource_group=gso_resource_group,
                      junction_cookie_javascript_block=junction_cookie_javascript_block,
                      client_ip_http=client_ip_http, version_two_cookies=version_two_cookies,
                      ltpa_keyfile=ltpa_keyfile, authz_rules=authz_rules, fsso_config_file=fsso_config_file,
                      username=username, password=password, server_uuid=server_uuid, server_port=server_port,
                      virtual_hostname=virtual_hostname, server_dn=server_dn, local_ip=local_ip,
                      query_contents=query_contents, case_sensitive_url=case_sensitive_url,
                      windows_style_url=windows_style_url, ltpa_keyfile_password=ltpa_keyfile_password,
                      https_port=https_port, http_port=http_port, proxy_hostname=proxy_hostname,
                      proxy_port=proxy_port, sms_environment=sms_environment, vhost_label=vhost_label,
                      junction_force=junction_force, delegation_support=delegation_support,
                      scripting_support=scripting_support,
                      case_insensitive_url=case_insensitive_url,
                      check_mode=check_mode, force=force)
    else:
        return add(isamAppliance=isamAppliance, instance_name=instance_name, server_hostname=server_hostname,
                   junction_point=junction_point, junction_type=junction_type, policy=policy,
                   authentication=authentication, static_response_headers=static_response_headers, jwt=jwt,
                   junction_hard_limit=junction_hard_limit, junction_soft_limit=junction_soft_limit,
                   basic_auth_mode=basic_auth_mode, tfim_sso=tfim_sso, remote_http_header=remote_http_header,
                   stateful_junction=stateful_junction, http2_junction=http2_junction, http2_proxy=http2_proxy,
                   sni_name=sni_name, preserve_cookie=preserve_cookie, cookie_include_path=cookie_include_path,
                   transparent_path_junction=transparent_path_junction, mutual_auth=mutual_auth,
                   insert_ltpa_cookies=insert_ltpa_cookies, insert_session_cookies=insert_session_cookies,
                   request_encoding=request_encoding, enable_basic_auth=enable_basic_auth, key_label=key_label,
                   gso_resource_group=gso_resource_group,
                   junction_cookie_javascript_block=junction_cookie_javascript_block,
                   client_ip_http=client_ip_http, version_two_cookies=version_two_cookies,
                   ltpa_keyfile=ltpa_keyfile, authz_rules=authz_rules, fsso_config_file=fsso_config_file,
                   username=username, password=password, server_uuid=server_uuid, server_port=server_port,
                   virtual_hostname=virtual_hostname, server_dn=server_dn, local_ip=local_ip,
                   query_contents=query_contents, case_sensitive_url=case_sensitive_url,
                   windows_style_url=windows_style_url, ltpa_keyfile_password=ltpa_keyfile_password,
                   https_port=https_port, http_port=http_port, proxy_hostname=proxy_hostname,
                   proxy_port=proxy_port, sms_environment=sms_environment, vhost_label=vhost_label,
                   junction_force=junction_force, delegation_support=delegation_support,
                   scripting_support=scripting_support,
                   case_insensitive_url=case_insensitive_url,
                   check_mode=check_mode, force=force)


def delete(isamAppliance, instance_name, resource_server_name, server_type='standard',
           check_mode=False, force=False):
    """
    Delete an existing API Access Control Resource Server
    """

    server_exist, warnings = _check_server_exist(isamAppliance, instance_name, resource_server_name)

    if force is True or server_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            url = "{0}/{1}/server{2}?server_type={3}".format(uri, instance_name, resource_server_name, server_type)
            return isamAppliance.invoke_delete(
                "Delete an existing API Access Control Resource Server",
                url,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_selection(isamAppliance, instance_name, resource_servers, command="DELETE",
                     check_mode=False, force=False):
    """
    Delete a selection of API Access Control Resource Servers
    """

    ret_obj = get_all(isamAppliance, instance_name)
    warnings = ret_obj['warnings']
    found_any = False
    new_list_servers = []

    for server in resource_servers:
        found = False
        for obj in ret_obj['data']:
            if obj['name'] == server:
                found = True
                found_any = True
        if found is False:
            warnings.append("Did not find resource server {0} to delete".format(server))
        else:
            new_list_servers.append(server)

    if force is True or found_any is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Delete a selection of API Access Control Resource Servers",
                "{0}/{1}/server".format(uri, instance_name),
                {
                    'command': command,
                    'resource_servers': new_list_servers
                },
                requires_modules=requires_modules,
                requires_version=requires_version, warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_all(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Delete all existing API Access Control Resource Servers
    """

    all_exist, warnings = _check_all_servers(isamAppliance, instance_name)

    if force is True or all_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            url = "{0}/{1}/server".format(uri, instance_name)
            return isamAppliance.invoke_delete(
                "Delete all existing API Access Control Resource Servers",
                url,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def export_all(isamAppliance, instance_name, file_path, check_mode=False, force=False):
    """
    Exporting all existing API Access Control Resource Servers
    """

    if os.path.exists(file_path) is True:
        warn_str = "File {0} already exists".format(file_path)
        warnings = [warn_str]
        return isamAppliance.create_return_object(warnings=warnings)

    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is True or instance_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            url = "{0}/{1}/server?export=true".format(uri, instance_name)
            return isamAppliance.invoke_get_file(
                "Exporting all existing API Access Control Resource Servers",
                url,
                file_path,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def export_file(isamAppliance, instance_name, resource_server_name, file_path, check_mode=False, force=False):
    """
    Exporting an existing API Access Control Resource Server
    """
    if os.path.exists(file_path) is True:
        warn_str = "File {0} already exists".format(file_path)
        warnings = [warn_str]
        return isamAppliance.create_return_object(warnings=warnings)

    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)
    if force is False:
        if instance_exist is False:
            warnings.append("{0} does not exist".format(instance_name))
            return isamAppliance.create_return_object(warnings=warnings)
        else:
            server_exist, warnings = _check_server_exist(isamAppliance, instance_name, resource_server_name)
            if server_exist is False:
                warnings.append("The specified resource server name does not exist")
                return isamAppliance.create_return_object(warnings=warnings)

    if force is True or server_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            url = "{0}/{1}/server{2}?export=true".format(uri, instance_name, resource_server_name)
            return isamAppliance.invoke_get_file(
                "Exporting an existing API Access Control Resource Server",
                url,
                file_path,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def import_file(isamAppliance, instance_name, filename, check_mode=False, force=False):
    """
    Importing an API Access Control Resource Server(s)
    """
    if os.path.exists(filename) is False:
        warn_str = "File {0} does not exists".format(filename)
        warnings = [warn_str]
        return isamAppliance.create_return_object(warnings=warnings)

    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)
    if force is False:
        if instance_exist is False:
            warnings.append("{0} does not exist".format(instance_name))
            return isamAppliance.create_return_object(warnings=warnings)

    if force is True or instance_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            url = "{0}/{1}/server".format(uri, instance_name)

            return isamAppliance.invoke_post_files(
                "Importing an API Access Control Resource Server(s)", url,
                [
                    {
                        'file_formfield': 'config_file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {}, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def _check_server_exist(isamAppliance, instance_name, junction_point):
    ret_obj = get_all(isamAppliance, instance_name)
    for obj in ret_obj['data']:
        if obj['name'] == junction_point:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_all_servers(isamAppliance, instance_name):
    ret_obj = get_all(isamAppliance, instance_name)
    warnings = ret_obj['warnings']

    if ret_obj['data'] != []:
        return True, warnings
    else:
        return False, warnings


def _check_list_servers(isamAppliance, instance_name, resource_servers):
    ret_obj = get_all(isamAppliance, instance_name)
    warnings = ret_obj['warnings']
    non_exist = False

    for server in resource_servers:
        found = False
        for obj in ret_obj['data']:
            if obj['name'] == server:
                found = True
        if found is False:
            non_exist = True
            warnings.append("Did not find resource server {0}".format(server))

    if non_exist is False:
        return True, ret_obj['warnings']
    else:
        return False, warnings


def _check_server_content(isamAppliance, instance_name, junction_point, server_hostname, junction_type, policy,
                          authentication, static_response_headers, jwt, junction_hard_limit, junction_soft_limit,
                          basic_auth_mode, tfim_sso, remote_http_header, stateful_junction, http2_junction, http2_proxy,
                          sni_name, preserve_cookie, cookie_include_path, transparent_path_junction, mutual_auth,
                          insert_ltpa_cookies, insert_session_cookies, request_encoding, enable_basic_auth, key_label,
                          gso_resource_group, junction_cookie_javascript_block, client_ip_http, version_two_cookies,
                          ltpa_keyfile, authz_rules, fsso_config_file, username, password, server_uuid, server_port,
                          virtual_hostname, server_dn, local_ip, query_contents, case_sensitive_url,
                          windows_style_url, ltpa_keyfile_password, https_port, http_port, proxy_hostname, proxy_port,
                          sms_environment, vhost_label, delegation_support, scripting_support, case_insensitive_url):
    ret_obj = get(isamAppliance, instance_name, junction_point)
    current_data = ret_obj['data']
    add_required = False
    json_data = {
        'server_hostname': server_hostname,
        'junction_point': junction_point,
        'junction_type': junction_type.lower(),
        'policy': policy,
        'authentication': authentication
    }

    server_str = current_data['servers']
    server_list = server_str.split("#")

    for server in server_list:
        if server[-1] == ";":
            str_length = len(server)
            server_str = server[:str_length - 1]
        else:
            server_str = server
        server_values = server_str.split(";")
        srv = {}
        for values in server_values:
            jnames = values.split("!")
            value_pair = {
                jnames[0]: jnames[1]
            }
            srv.update(value_pair)
        server_found = False
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
                    if case_sensitive_url.lower() == 'yes':
                        server_json["case_insensitive_url"] = 'no'
                    else:
                        server_json["case_insensitive_url"] = 'yes'
                else:
                    server_json["case_insensitive_url"] = 'yes'
            elif case_sensitive_url is not None:
                server_json['case_sensitive_url'] = case_sensitive_url
            else:
                server_json['case_sensitive_url'] = 'no'

            if http_port is None:
                server_json['http_port'] = str(server_port)
            else:
                server_json['http_port'] = str(http_port)

            if https_port is not None:
                server_json['https_port'] = str(https_port)

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
        if static_response_headers is not None:
            json_data['static_response_headers'] = static_response_headers
        else:
            json_data['static_response_headers'] = {}

        if jwt is not None:
            json_data['jwt'] = jwt
        else:
            json_data['jwt'] = {}

        if junction_hard_limit is not None:
            json_data['junction_hard_limit'] = junction_hard_limit
        else:
            json_data['junction_hard_limit'] = '0 - using global value'

        if junction_soft_limit is not None:
            json_data['junction_soft_limit'] = junction_soft_limit
        else:
            json_data['junction_soft_limit'] = '0 - using global value',

        if basic_auth_mode is not None:
            json_data['basic_auth_mode'] = basic_auth_mode
        else:
            json_data['basic_auth_mode'] = 'filter'

        if tfim_sso is not None:
            json_data['tfim_sso'] = tfim_sso
        else:
            json_data['tfim_sso'] = 'no'

        if remote_http_header is None:
            json_data['remote_http_header'] = 'do not insert'
        elif isinstance(remote_http_header, basestring) and remote_http_header.lower() == 'all':
            json_data['remote_http_header'] = ['iv_creds', 'iv_groups', 'iv_user']
        else:
            json_data['remote_http_header'] = remote_http_header

        if 'remote_http_header' in ret_obj['data']:
            http_headers = ret_obj['data']['remote_http_header'].split(' ')
            if 'insert' in http_headers:
                http_headers.remove('insert')
            if '-' in http_headers:
                http_headers.remove('-')
            current_data['remote_http_header'] = http_headers

        if stateful_junction is not None:
            json_data['stateful_junction'] = stateful_junction
        else:
            json_data['stateful_junction'] = 'no'

        if http2_junction is not None:
            json_data['http2_junction'] = http2_junction

        if http2_proxy is not None:
            json_data['http2_proxy'] = http2_proxy

        if sni_name is not None:
            json_data['sni_name'] = sni_name

        if preserve_cookie is not None:
            json_data['preserve_cookie'] = preserve_cookie
        else:
            json_data['preserve_cookie'] = 'no'

        if cookie_include_path is not None:
            json_data['cookie_include_path'] = cookie_include_path
        else:
            json_data['cookie_include_path'] = 'no'

        if transparent_path_junction is not None:
            json_data['transparent_path_junction'] = transparent_path_junction
        else:
            json_data['transparent_path_junction'] = 'no'

        if mutual_auth is not None:
            json_data['mutual_auth'] = mutual_auth
        else:
            json_data['mutual_auth'] = mutual_auth

        if insert_ltpa_cookies is not None:
            json_data['insert_ltpa_cookies'] = insert_ltpa_cookies

        if insert_session_cookies is not None:
            json_data['insert_session_cookies'] = insert_session_cookies
        else:
            json_data['insert_session_cookies'] = 'no'

        if request_encoding is not None:
            json_data['request_encoding'] = request_encoding
        else:
            json_data['request_encoding'] = 'utf8_uri'

        if 'request_encoding' in ret_obj['data']:
            if ret_obj['data']['request_encoding'] == "UTF-8, URI Encoded":
                current_data['request_encoding'] = 'utf8_uri'
            elif ret_obj['data']['request_encoding'] == "UTF-8, Binary":
                current_data['request_encoding'] = 'utf8_bin'
            elif ret_obj['data']['request_encoding'] == "Local Code Page, Binary":
                current_data['request_encoding'] = 'lcp_bin'
            elif ret_obj['data']['request_encoding'] == "Local Code Page, URI Encoded":
                current_data['request_encoding'] = 'lcp_uri'

        if enable_basic_auth is not None:
            json_data['enable_basic_auth'] = enable_basic_auth

        if key_label is not None:
            json_data['key_label'] = key_label

        if gso_resource_group is not None:
            json_data['gso_resource_group'] = gso_resource_group

        if junction_cookie_javascript_block is not None:
            json_data['junction_cookie_javascript_block'] = junction_cookie_javascript_block

        if client_ip_http is not None:
            json_data['client_ip_http'] = client_ip_http
            if 'client_ip_http' in ret_obj['data']:
                if ret_obj['data']['client_ip_http'] == 'do not insert':
                    current_data['client_ip_http'] = 'no'
                else:
                    current_data['client_ip_http'] = ret_obj['data']['client_ip_http']

        if client_ip_http is None or client_ip_http.lower() == 'no':
            json_data['client_ip_http'] = 'do not insert'
        elif client_ip_http.lower() == 'yes':
            json_data['client_ip_http'] = 'insert'
        else:
            json_data['client_ip_http'] = client_ip_http

        if version_two_cookies is not None:
            json_data['client_ip_http'] = client_ip_http

        if ltpa_keyfile is not None:
            json_data[ltpa_keyfile] = ltpa_keyfile

        if authz_rules is not None:
            json_data['authz_rules'] = authz_rules
        else:
            json_data['authz_rules'] = 'no'

        if fsso_config_file is not None:
            json_data['fsso_config_file'] = fsso_config_file
        else:
            json_data['fsso_config_file'] = 'disabled'

        if username is not None:
            json_data['username'] = username

        if password is not None:
            json_data['password'] = password

        if ltpa_keyfile_password is not None:
            json_data['ltpa_keyfile_password'] = ltpa_keyfile_password

        if proxy_hostname is not None:
            json_data['proxy_hostname'] = proxy_hostname

        if proxy_port is not None:
            json_data['proxy_port'] = proxy_port

        if sms_environment is not None:
            json_data['sms_environment'] = sms_environment

        if vhost_label is not None:
            json_data['vhost_label'] = vhost_label

        if delegation_support is not None:
            json_data['delegation_support'] = delegation_support
        else:
            json_data['delegation_support'] = 'no'

        if scripting_support is not None:
            json_data['scripting_support'] = scripting_support
        else:
            json_data['scripting_support'] = 'no'

        del current_data['boolean_rule_header']
        del current_data['forms_based_sso']
        del current_data['http_header_ident']
        del current_data['session_cookie_backend_portal']
        del current_data['servers']
        sorted_obj1 = tools.json_sort(json_data)
        logger.debug("Sorted sorted_obj1: {0}".format(sorted_obj1))
        sorted_obj2 = tools.json_sort(current_data)
        logger.debug("Sorted sorted_obj2: {0}".format(sorted_obj2))

        if sorted_obj1 != sorted_obj2:
            logger.info("Changes detected, update needed.")
            add_required = True

    return add_required, ret_obj['warnings']


def _check_instance_exist(isamAppliance, instance_name):
    ret_obj = ibmsecurity.isam.web.api_access_control.resources.instances.get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == instance_name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def compare(isamAppliance1, isamAppliance2):
    """
    Compare resources between two appliances
    """

    app1_instances = ibmsecurity.isam.web.api_access_control.resources.instances.get_all(isamAppliance1)
    app2_instances = ibmsecurity.isam.web.api_access_control.resources.instances.get_all(isamAppliance2)

    obj1 = []
    obj2 = []

    for inst1 in app1_instances['data']:
        servers = get_all(isamAppliance1, instance_name=inst1['name'])
        for srv in servers['data']:
            if "servers" in srv:
                srvlist = srv['servers'].split(";")
                new_str = None
                for value in srvlist:
                    if value.find("server_uuid") == -1 and \
                            value.find("current_requests") == -1 and \
                            value.find("total_requests") == -1:
                        if new_str is None:
                            new_str = value
                        else:
                            new_str = new_str + ";" + value
                srv['servers'] = new_str
            obj1.append(srv)

    for inst2 in app2_instances['data']:
        servers = get_all(isamAppliance2, instance_name=inst2['name'])
        for srv in servers['data']:
            if "servers" in srv:
                srvlist = srv['servers'].split(";")
                new_str = None
                for value in srvlist:
                    if value.find("server_uuid") == -1 and \
                            value.find("current_requests") == -1 and \
                            value.find("total_requests") == -1:
                        if new_str is None:
                            new_str = value
                        else:
                            new_str = new_str + ";" + value
                srv['servers'] = new_str
            obj2.append(srv)

    app1_instances['data'].extend(obj1)
    app2_instances['data'].extend(obj2)

    return tools.json_compare(app1_instances, app2_instances,
                              deleted_keys=['server_uuid', 'current_requests', 'total_requests'])


def compare_one_instance(isamAppliance1, isamAppliance2, instance1_name, instance2_name=None):
    """
    Compare resources between two appliances
    """
    if instance2_name is None or instance2_name == '':
        instance2_name = instance1_name

    obj1 = []
    obj2 = []
    servers1 = get_all(isamAppliance1, instance_name=instance1_name)
    for srv in servers1['data']:
        if "servers" in srv:
            srvlist = srv['servers'].split(";")
            new_str = None
            for value in srvlist:
                if value.find("server_uuid") == -1 and \
                        value.find("current_requests") == -1 and \
                        value.find("total_requests") == -1:
                    if new_str is None:
                        new_str = value
                    else:
                        new_str = new_str + ";" + value
            srv['servers'] = new_str
        obj1.append(srv)

    servers2 = get_all(isamAppliance2, instance_name=instance2_name)
    for srv in servers2['data']:
        if "servers" in srv:
            srvlist = srv['servers'].split(";")
            new_str = None
            for value in srvlist:
                if value.find("server_uuid") == -1 and \
                        value.find("current_requests") == -1 and \
                        value.find("total_requests") == -1:
                    if new_str is None:
                        new_str = value
                    else:
                        new_str = new_str + ";" + value
            srv['servers'] = new_str
        obj2.append(srv)

    servers1['data'] = obj1
    servers2['data'] = obj2

    return tools.json_compare(servers1, servers2, deleted_keys=['server_uuid', 'current_requests', 'total_requests'])
