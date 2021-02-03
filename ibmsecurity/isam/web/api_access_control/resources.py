import logging
import os

from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/resource/instance"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get_all_instances(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of all Reverse Proxy Instances
    """
    return isamAppliance.invoke_get("Retrieve a list of all Reverse Proxy Instances",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_all_servers(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Retrieve a list of all API Access Control Resource Servers
    """
    return isamAppliance.invoke_get("Retrieve a list of all API Access Control Resource Servers",
                                    "{0}/{1}/server".format(uri, instance_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_all_resources(isamAppliance, instance_name, resource_server_name, check_mode=False, force=False):
    """
    Retrieve a list of all API Access Control Resources
    """
    return isamAppliance.invoke_get("Retrieve a list of all API Access Control Resources",
                                    "{0}/{1}/server{2}/resource".format(uri, instance_name, resource_server_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_a_server(isamAppliance, instance_name, resource_server_name, check_mode=False, force=False):
    """
    Retrieve a single API Access Control Resource Server
    """
    return isamAppliance.invoke_get("Retrieve a single API Access Control Resource Server",
                                    "{0}/{1}/server{2}".format(uri, instance_name, resource_server_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get_a_resource(isamAppliance, instance_name, resource_server_name, resource_name, method,
                   server_type="standard", check_mode=False, force=False):
    """
    Retrieve a single API Access Control Resource
    """

    if tools.version_compare(isamAppliance.facts["version"], "10.0.0") < 0:
        url = "{0}/{1}/server{2}/resource/{3}{4}?server_type={5}".format(uri, instance_name, resource_server_name,
                                                                         method, resource_name, server_type)
    else:
        url = "{0}/{1}/server{2}/resource/{3}{2}{4}?server_type={5}".format(uri, instance_name, resource_server_name,
                                                                            method, resource_name, server_type)

    return isamAppliance.invoke_get("Retrieve a single API Access Control Resource",
                                    url, requires_modules=requires_modules, requires_version=requires_version)


def get_an_instance(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Retrieve a single Reverse Proxy Instance
    """
    return isamAppliance.invoke_get("Retrieve a single Reverse Proxy Instance",
                                    "{0}/{1}".format(uri, instance_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def add_server(isamAppliance, instance_name, server_hostname, junction_point, junction_type, policy, authentication,
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
               boolean_rule_header=None, forms_based_sso=None, check_mode=False, force=False):
    """
    Creating a new API Access Control Resource Server
    """
    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is False:
        if instance_exist is False:
            warnings.append("{0} does not exist".format(instance_name))
            return isamAppliance.create_return_object(warnings=warnings)
        else:
            server_exist, warnings = _check_server_exist(isamAppliance, instance_name, junction_point)
            if server_exist is True:
                warnings.append("The specified resource server name already exist")
                return isamAppliance.create_return_object(warnings=warnings)

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

        if case_sensitive_url is not None:
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

        if boolean_rule_header is not None:
            json_data['boolean_rule_header']

        if forms_based_sso is not None:
            json_data['forms_based_sso']

        return isamAppliance.invoke_post(
            "Creating a new API Access Control Resource Server",
            "{0}/{1}/server".format(uri, instance_name),
            json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def add_resource(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type="standard",
                 name=None, static_response_headers=None, rate_limiting_policy=None, url_aliases=None,
                 documentation=None, check_mode=False, force=False):
    """
    Creating a new API Access Control Resource
    """
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

    resource_exist, warnings = _check_resource_exist(isamAppliance, instance_name, resource_server_name, method, path)

    if force is True or resource_exist is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            json_data = {
                'method': method,
                'policy': policy,
                'server_type': server_type
            }

            if tools.version_compare(isamAppliance.facts["version"], "10.0.0") < 0:
                json_data['path'] = path
            else:
                json_data['path'] = "{0}{1}".format(resource_server_name, path)

            if name is not None:
                json_data['name'] = name

            if static_response_headers is not None:
                json_data['static_response_headers'] = static_response_headers

            if rate_limiting_policy is not None:
                json_data['rate_limiting_policy'] = rate_limiting_policy

            if url_aliases is not None:
                json_data['url_aliases'] = url_aliases

            if documentation is not None:
                json_data['documentation'] = documentation

            return isamAppliance.invoke_post(
                "Creating a new API Access Control Resource",
                "{0}/{1}/server{2}/resource".format(uri, instance_name, resource_server_name),
                json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def update_server(isamAppliance, instance_name, junction_point, server_hostname, junction_type,
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
                  check_mode=False, force=False):
    """
    Updating an existing API Access Control Resource Server
    """
    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is False:
        if instance_exist is False:
            warnings.append("{0} does not exist".format(instance_name))
            return isamAppliance.create_return_object(warnings=warnings)
        else:
            server_exist, warnings = _check_server_exist(isamAppliance, instance_name, junction_point)
            if server_exist is False:
                warnings.append("The specified resource does not exist")
                return isamAppliance.create_return_object(warnings=warnings)

    update_required, warnings, json_data = _check_server_content(isamAppliance=isamAppliance,
                                                                 instance_name=instance_name,
                                                                 junction_point=junction_point,
                                                                 server_hostname=server_hostname,
                                                                 junction_type=junction_type, policy=policy,
                                                                 authentication=authentication, server_type=server_type,
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
                                                                 fsso_config_file=fsso_config_file, username=username,
                                                                 password=password,
                                                                 server_uuid=server_uuid, server_port=server_port,
                                                                 virtual_hostname=virtual_hostname, server_dn=server_dn,
                                                                 local_ip=local_ip, query_contents=query_contents,
                                                                 case_sensitive_url=case_sensitive_url,
                                                                 windows_style_url=windows_style_url,
                                                                 ltpa_keyfile_password=ltpa_keyfile_password,
                                                                 https_port=https_port,
                                                                 http_port=http_port, proxy_hostname=proxy_hostname,
                                                                 proxy_port=proxy_port, sms_environment=sms_environment,
                                                                 vhost_label=vhost_label, junction_force=junction_force,
                                                                 delegation_support=delegation_support,
                                                                 scripting_support=scripting_support)

    json_data['force'] = junction_force

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating an existing API Access Control Resource Server",
                "{0}/{1}/server{2}?server_type={3}".format(uri, instance_name, junction_point, server_type),
                json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set_server(isamAppliance, instance_name, junction_point, server_hostname, junction_type,
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
               boolean_rule_header=None, forms_based_sso=None, check_mode=False, force=False):
    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is False:
        if instance_exist is False:
            warnings.append("{0} does not exist".format(instance_name))
            return isamAppliance.create_return_object(warnings=warnings)

    server_exist, warnings = _check_server_exist(isamAppliance, instance_name, junction_point)

    if server_exist is True:
        return update_server(isamAppliance=isamAppliance, instance_name=instance_name, junction_point=junction_point,
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
                             scripting_support=scripting_support, check_mode=check_mode, force=force)
    else:
        return add_server(isamAppliance=isamAppliance, instance_name=instance_name, server_hostname=server_hostname,
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
                          scripting_support=scripting_support, boolean_rule_header=boolean_rule_header,
                          forms_based_sso=forms_based_sso, check_mode=check_mode, force=force)


def update_resource(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type="standard",
                    name=None, static_response_headers=None, rate_limiting_policy=None, url_aliases=None,
                    documentation=None, check_mode=False, force=False):
    """
    Updating an existing API Access Control Resource
    """
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
            else:
                resource_exist, warnings = _check_resource_exist(isamAppliance, instance_name, resource_server_name,
                                                                 method, path)
                if resource_exist is False:
                    warnings.append("The specified resource does not exist")
                    return isamAppliance.create_return_object(warnings=warnings)

    update_required, warnings, json_data = _check_resource_content(isamAppliance=isamAppliance,
                                                                   instance_name=instance_name,
                                                                   resource_server_name=resource_server_name,
                                                                   method=method, path=path, policy=policy,
                                                                   server_type=server_type, name=name,
                                                                   static_response_headers=static_response_headers,
                                                                   rate_limiting_policy=rate_limiting_policy,
                                                                   url_aliases=url_aliases, documentation=documentation)
    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if tools.version_compare(isamAppliance.facts["version"], "10.0.0") < 0:
                url = "{0}/{1}/server{2}/resource/{3}{4}?server_type={5}".format(uri, instance_name,
                                                                                 resource_server_name,
                                                                                 method, path, server_type)
            else:
                url = "{0}/{1}/server{2}/resource/{3}{2}{4}?server_type={5}".format(uri, instance_name,
                                                                                    resource_server_name,
                                                                                    method, path, server_type)

            return isamAppliance.invoke_put(
                "Updating an existing API Access Control Resource",
                url, json_data, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def set_resource(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type="standard",
                 name=None, static_response_headers=None, rate_limiting_policy=None, url_aliases=None,
                 documentation=None, check_mode=False, force=False):
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

    resource_exist, warnings = _check_resource_exist(isamAppliance, instance_name, resource_server_name,
                                                     method, path)
    if resource_exist is True:
        return update_resource(isamAppliance=isamAppliance, instance_name=instance_name,
                               resource_server_name=resource_server_name, method=method, path=path, policy=policy,
                               server_type=server_type, name=name, static_response_headers=static_response_headers,
                               rate_limiting_policy=rate_limiting_policy, url_aliases=url_aliases,
                               documentation=documentation, check_mode=check_mode, force=force)
    else:
        return add_resource(isamAppliance=isamAppliance, instance_name=instance_name,
                            resource_server_name=resource_server_name, method=method, path=path, policy=policy,
                            server_type=server_type, name=name, static_response_headers=static_response_headers,
                            rate_limiting_policy=rate_limiting_policy, url_aliases=url_aliases,
                            documentation=documentation, check_mode=check_mode, force=force)


def delete_a_resource(isamAppliance, instance_name, resource_server_name, method, path, server_type='standard',
                      check_mode=False, force=False):
    """
    Delete an existing API Access Control Resource
    """

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

    resource_exist, warnings = _check_resource_exist(isamAppliance, instance_name, resource_server_name, method, path)

    if force is True or resource_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if tools.version_compare(isamAppliance.facts["version"], "10.0.0") < 0:
                url = "{0}/{1}/server{2}/resource/{3}{4}?server_type={5}".format(uri, instance_name,
                                                                                 resource_server_name,
                                                                                 method, path, server_type)
            else:
                url = "{0}/{1}/server{2}/resource/{3}{2}{4}?server_type={5}".format(uri, instance_name,
                                                                                    resource_server_name,
                                                                                    method, path, server_type)
            return isamAppliance.invoke_delete(
                "Delete an existing API Access Control Resource",
                url,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_select_resources(isamAppliance, instance_name, resource_server_name, resources, command="DELETE",
                            server_type="standard", check_mode=False, force=False):
    """
    Delete a selection of API Access Control Resources
    """
    exist_all, warnings = _check_list_resource(isamAppliance, instance_name, resource_server_name, resources)

    if force is True or exist_all is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Delete a selection of API Access Control Resources",
                "{0}/{1}/server{2}/resource?server_type={3}".format(uri, instance_name, resource_server_name,
                                                                    server_type),
                {
                    'command': command,
                    'resources': resources
                },
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_all_resources(isamAppliance, instance_name, resource_server_name, server_type='standard',
                         check_mode=False, force=False):
    """
    Delete all existing API Access Control Resources
    """

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

    resource_exist, warnings = _check_all_resource(isamAppliance, instance_name, resource_server_name)

    if force is True or resource_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Delete all existing API Access Control Resources",
                "{0}/{1}/server{2}/resource?server_type={3}".format(uri, instance_name, resource_server_name,
                                                                    server_type),
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_a_server(isamAppliance, instance_name, resource_server_name, server_type='standard',
                    check_mode=False, force=False):
    """
    Delete an existing API Access Control Resource Server
    """

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
            url = "{0}/{1}/server{2}?server_type={3}".format(uri, instance_name, resource_server_name, server_type)
            return isamAppliance.invoke_delete(
                "Delete an existing API Access Control Resource Server",
                url,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_select_servers(isamAppliance, instance_name, resource_servers, command="DELETE",
                          check_mode=False, force=False):
    """
    Delete a selection of API Access Control Resource Servers
    """
    exist_all, warnings = _check_list_servers(isamAppliance, instance_name, resource_servers)

    if force is True or exist_all is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Delete a selection of API Access Control Resource Servers",
                "{0}/{1}/server".format(uri, instance_name),
                {
                    'command': command,
                    'resource_servers': resource_servers
                },
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def delete_all_servers(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Delete all existing API Access Control Resource Servers
    """

    instance_exist, warnings = _check_instance_exist(isamAppliance, instance_name)

    if force is False:
        if instance_exist is False:
            warnings.append("{0} does not exist".format(instance_name))
            return isamAppliance.create_return_object(warnings=warnings)

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


def export_all_servers(isamAppliance, instance_name, file_path, check_mode=False, force=False):
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


def export_all_resources(isamAppliance, instance_name, resource_server_name, file_path, check_mode=False, force=False):
    """
    Exporting all existing API Access Control Resources
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
            url = "{0}/{1}/server{2}/resource?export=true".format(uri, instance_name, resource_server_name)
            return isamAppliance.invoke_get_file(
                "Exporting all existing API Access Control Resources",
                url,
                file_path,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def export_a_server(isamAppliance, instance_name, resource_server_name, file_path, check_mode=False, force=False):
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


def export_a_resource(isamAppliance, instance_name, resource_server_name, method, path, file_path,
                      server_type="standard", check_mode=False, force=False):
    """
    Exporting an existing API Access Control Resource
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

    resource_exist, warnings = _check_resource_exist(isamAppliance, instance_name, resource_server_name, method, path)

    if force is True or resource_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if tools.version_compare(isamAppliance.facts["version"], "10.0.0") < 0:
                url = "{0}/{1}/server{2}/resource/{3}{4}?export=true&server_type={5}".format(uri, instance_name,
                                                                                             resource_server_name,
                                                                                             method, path, server_type)
            else:
                url = "{0}/{1}/server{2}/resource/{3}{2}{4}?export=true&server_type={5}".format(uri, instance_name,
                                                                                                resource_server_name,
                                                                                                method, path,
                                                                                                server_type)
            return isamAppliance.invoke_get_file(
                "Exporting an existing API Access Control Resource",
                url,
                file_path,
                requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def import_a_resource(isamAppliance, instance_name, resource_server_name, filename,
                      server_type="standard", check_mode=False, force=False):
    """
    Importing an API Access Control Resource(s)
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
        else:
            server_exist, warnings = _check_server_exist(isamAppliance, instance_name, resource_server_name)
            if server_exist is False:
                warnings.append("The specified resource server name does not exist")
                return isamAppliance.create_return_object(warnings=warnings)

    if force is True or server_exist is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            url = "{0}/{1}/server{2}/resource?server_type={3}".format(uri, instance_name,
                                                                      resource_server_name, server_type)

            return isamAppliance.invoke_post_files(
                "Importing an API Access Control Resource(s)", url,
                [
                    {
                        'file_formfield': 'config_file',
                        'filename': filename,
                        'mimetype': 'application/octet-stream'
                    }
                ],
                {}, requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)


def import_a_server(isamAppliance, instance_name, filename, check_mode=False, force=False):
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


def _check_instance_exist(isamAppliance, instance_name):
    ret_obj = get_all_instances(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == instance_name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_server_exist(isamAppliance, instance_name, junction_point):
    ret_obj = get_all_servers(isamAppliance, instance_name)
    for obj in ret_obj['data']:
        if obj['name'] == junction_point:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_resource_exist(isamAppliance, instance_name, resource_server_name, method, path):
    ret_obj = get_all_resources(isamAppliance, instance_name, resource_server_name)
    warnings = ret_obj['warnings']
    if tools.version_compare(isamAppliance.facts["version"], "10.0.0") < 0:
        path_name = path
    else:
        path_name = "{0}{1}".format(resource_server_name, path)
    for obj in ret_obj['data']:
        if obj['method'] == method and obj['path'] == path_name:
            return True, warnings

    return False, warnings


def _check_all_resource(isamAppliance, instance_name, resource_server_name):
    ret_obj = get_all_resources(isamAppliance, instance_name, resource_server_name)
    warnings = ret_obj['warnings']

    if ret_obj['data'] != []:
        return True, warnings
    else:
        return False, warnings


def _check_all_servers(isamAppliance, instance_name):
    ret_obj = get_all_servers(isamAppliance, instance_name)
    warnings = ret_obj['warnings']

    if ret_obj['data'] != []:
        return True, warnings
    else:
        return False, warnings


def _check_list_resource(isamAppliance, instance_name, resource_server_name, resources):
    ret_obj = get_all_resources(isamAppliance, instance_name, resource_server_name)
    warnings = ret_obj['warnings']
    non_exist = False

    for resource in resources:
        found = False
        for obj in ret_obj['data']:
            if obj['id'] == resource:
                found = True
        if found is False:
            non_exist = True
            warnings.append("Did not find resource {0}".format(resource))

    if non_exist is False:
        return True, ret_obj['warnings']
    else:
        return False, warnings


def _check_list_servers(isamAppliance, instance_name, resource_servers):
    ret_obj = get_all_servers(isamAppliance, instance_name)
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
                          authentication,
                          server_type, static_response_headers, jwt, junction_hard_limit, junction_soft_limit,
                          basic_auth_mode, tfim_sso, remote_http_header, stateful_junction, http2_junction, http2_proxy,
                          sni_name, preserve_cookie, cookie_include_path, transparent_path_junction, mutual_auth,
                          insert_ltpa_cookies, insert_session_cookies, request_encoding, enable_basic_auth, key_label,
                          gso_resource_group, junction_cookie_javascript_block, client_ip_http, version_two_cookies,
                          ltpa_keyfile,
                          authz_rules, fsso_config_file, username, password, server_uuid, server_port, virtual_hostname,
                          server_dn,
                          local_ip, query_contents, case_sensitive_url, windows_style_url, ltpa_keyfile_password,
                          https_port,
                          http_port, proxy_hostname, proxy_port, sms_environment, vhost_label, junction_force,
                          delegation_support,
                          scripting_support):
    ret_obj = get_a_server(isamAppliance, instance_name, junction_point)
    current_data = {
        'server_hostname': ret_obj['data']['server_hostname'],
        'junction_point': ret_obj['data']['junction_point'],
        'junction_type': ret_obj['data']['junction_type'].lower(),
        'policy': ret_obj['data']['policy'],
        'authentication': ret_obj['data']['authentication']
    }

    json_data = {
        'server_hostname': server_hostname,
        'junction_point': junction_point,
        'junction_type': junction_type.lower(),
        'policy': policy,
        'authentication': authentication
    }

    if static_response_headers is not None:
        json_data['static_response_headers'] = static_response_headers
        if 'static_response_headers' in ret_obj['data']:
            current_data['static_response_headers'] = ret_obj['data']['static_response_headers']

    if jwt is not None:
        json_data['jwt'] = jwt
        if 'jwt' in ret_obj['data']:
            current_data['jwt'] = ret_obj['data']['jwt']

    if junction_hard_limit is not None:
        json_data['junction_hard_limit'] = junction_hard_limit
        if 'junction_hard_limit' in ret_obj['data']:
            current_data['junction_hard_limit'] = ret_obj['data']['junction_hard_limit']

    if junction_soft_limit is not None:
        json_data['junction_soft_limit'] = junction_soft_limit
        if 'junction_soft_limit' in ret_obj['data']:
            current_data['junction_soft_limit'] = ret_obj['data']['junction_soft_limit']

    if basic_auth_mode is not None:
        json_data['basic_auth_mode'] = basic_auth_mode
        if 'basic_auth_mode' in ret_obj['data']:
            current_data['basic_auth_mode'] = ret_obj['data']['basic_auth_mode']

    if tfim_sso is not None:
        json_data['tfim_sso'] = tfim_sso
        if 'tfim_sso' in ret_obj['data']:
            current_data['tfim_sso'] = ret_obj['data']['tfim_sso']

    print(ret_obj['data']['remote_http_header'])
    if remote_http_header is not None:
        json_data['remote_http_header'] = remote_http_header
        if 'remote_http_header' in ret_obj['data']:
            http_headers = ret_obj['data']['remote_http_header'].split(' ')
            if 'insert' in http_headers:
                http_headers.remove('insert')
            if '-' in http_headers:
                http_headers.remove('-')
            current_data['remote_http_header'] = http_headers

    print(sorted(json_data['remote_http_header']))
    print(sorted(current_data['remote_http_header']))
    if sorted(json_data['remote_http_header']) != sorted(current_data['remote_http_header']):
        print("not same")
    else:
        print("same")

    if stateful_junction is not None:
        json_data['stateful_junction'] = stateful_junction
        if 'stateful_junction' in ret_obj['data']:
            current_data['stateful_junction'] = ret_obj['data']['stateful_junction']

    if http2_junction is not None:
        json_data['http2_junction'] = http2_junction
        if 'http2_junction' in ret_obj['data']:
            current_data['http2_junction'] = ret_obj['data']['http2_junction']

    if http2_proxy is not None:
        json_data['http2_proxy'] = http2_proxy
        if 'http2_proxy' in ret_obj['data']:
            current_data['http2_proxy'] = ret_obj['data']['http2_proxy']

    if sni_name is not None:
        json_data['sni_name'] = sni_name
        if 'sni_name' in ret_obj['data']:
            current_data['sni_name'] = ret_obj['data']['sni_name']

    if preserve_cookie is not None:
        json_data['preserve_cookie'] = preserve_cookie
        if 'preserve_cookie' in ret_obj['data']:
            current_data['preserve_cookie'] = ret_obj['data']['preserve_cookie']

    if cookie_include_path is not None:
        json_data['cookie_include_path'] = cookie_include_path
        if 'cookie_include_path' in ret_obj['data']:
            current_data['cookie_include_path'] = ret_obj['data']['cookie_include_path']

    if transparent_path_junction is not None:
        json_data['transparent_path_junction'] = transparent_path_junction
        if 'transparent_path_junction' in ret_obj['data']:
            current_data['transparent_path_junction'] = ret_obj['data']['transparent_path_junction']

    if mutual_auth is not None:
        json_data['mutual_auth'] = mutual_auth
        if 'mutual_auth' in ret_obj['data']:
            current_data['mutual_auth'] = ret_obj['data']['mutual_auth']

    if insert_ltpa_cookies is not None:
        json_data['insert_ltpa_cookies'] = insert_ltpa_cookies
        if 'insert_ltpa_cookies' in ret_obj['data']:
            current_data['insert_ltpa_cookies'] = ret_obj['data']['insert_ltpa_cookies']

    if insert_session_cookies is not None:
        json_data['insert_session_cookies'] = insert_session_cookies
        if 'insert_session_cookies' in ret_obj['data']:
            current_data['insert_session_cookies'] = ret_obj['data']['insert_session_cookies']

    if request_encoding is not None:
        json_data['request_encoding'] = request_encoding
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
        if 'enable_basic_auth' in ret_obj['data']:
            current_data['enable_basic_auth'] = ret_obj['data']['enable_basic_auth']

    if key_label is not None:
        json_data['key_label'] = key_label
        if 'key_label' in ret_obj['data']:
            current_data['key_label'] = ret_obj['data']['key_label']

    if gso_resource_group is not None:
        json_data['gso_resource_group'] = gso_resource_group
        if 'gso_resource_group' in ret_obj['data']:
            current_data['gso_resource_group'] = ret_obj['data']['gso_resource_group']

    if junction_cookie_javascript_block is not None:
        json_data['junction_cookie_javascript_block'] = junction_cookie_javascript_block
        if 'junction_cookie_javascript_block' in ret_obj['data']:
            current_data['junction_cookie_javascript_block'] = ret_obj['data']['junction_cookie_javascript_block']

    if client_ip_http is not None:
        json_data['client_ip_http'] = client_ip_http
        if 'client_ip_http' in ret_obj['data']:
            if ret_obj['data']['client_ip_http'] == 'do not insert':
                current_data['client_ip_http'] = 'no'
            else:
                current_data['client_ip_http'] = ret_obj['data']['client_ip_http']

    if version_two_cookies is not None:
        json_data['client_ip_http'] = client_ip_http
        if 'version_two_cookies' in ret_obj['data']:
            current_data['version_two_cookies'] = ret_obj['data']['version_two_cookies']

    if ltpa_keyfile is not None:
        json_data[ltpa_keyfile] = ltpa_keyfile
        if 'ltpa_keyfile' in ret_obj['data']:
            current_data['ltpa_keyfile'] = ret_obj['data']['ltpa_keyfile']

    if authz_rules is not None:
        json_data['authz_rules'] = authz_rules
        if 'authz_rules' in ret_obj['data']:
            current_data['authz_rules'] = ret_obj['data']['authz_rules']

    if fsso_config_file is not None:
        json_data['fsso_config_file'] = fsso_config_file
        if 'fsso_config_file' in ret_obj['data']:
            current_data['fsso_config_file'] = ret_obj['data']['fsso_config_file']

    if username is not None:
        json_data['username'] = username
        if 'username' in ret_obj['data']:
            current_data['username'] = ret_obj['data']['username']

    if password is not None:
        json_data['password'] = password
        if 'password' in ret_obj['data']:
            current_data['password'] = ret_obj['data']['password']

    if server_uuid is not None:
        json_data['server_uuid'] = server_uuid
        if 'server_uuid' in ret_obj['data']:
            current_data['server_uuid'] = ret_obj['data']['server_uuid']

    if server_port is not None:
        json_data['server_port'] = server_port
        if 'server_port' in ret_obj['data']:
            current_data['server_port'] = ret_obj['data']['server_port']

    if virtual_hostname is not None:
        json_data['virtual_hostname'] = virtual_hostname
        if 'virtual_hostname' in ret_obj['data']:
            current_data['virtual_hostname'] = ret_obj['data']['virtual_hostname']

    if server_dn is not None:
        json_data['server_dn'] = server_dn
        if 'server_dn' in ret_obj['data']:
            current_data['server_dn'] = ret_obj['data']['server_dn']

    if local_ip is not None:
        json_data['local_ip'] = local_ip
        if 'local_ip' in ret_obj['data']:
            current_data['local_ip'] = ret_obj['data']['local_ip']

    if query_contents is not None:
        json_data['query_contents'] = query_contents
        if 'query_contents' in ret_obj['data']:
            current_data['query_contents'] = ret_obj['data']['query_contents']

    if case_sensitive_url is not None:
        json_data['case_sensitive_url'] = case_sensitive_url
        if 'case_sensitive_url' in ret_obj['data']:
            current_data['case_sensitive_url'] = ret_obj['data']['case_sensitive_url']

    if windows_style_url is not None:
        json_data['windows_style_url'] = windows_style_url
        if 'windows_style_url' in ret_obj['data']:
            current_data['windows_style_url'] = ret_obj['data']['windows_style_url']

    if ltpa_keyfile_password is not None:
        json_data['ltpa_keyfile_password'] = ltpa_keyfile_password
        if 'ltpa_keyfile_password' in ret_obj['data']:
            current_data['ltpa_keyfile_password'] = ret_obj['data']['ltpa_keyfile_password']

    if https_port is not None:
        json_data['https_port'] = https_port
        if 'https_port' in ret_obj['data']:
            current_data['https_port'] = ret_obj['data']['https_port']

    if http_port is not None:
        json_data['http_port'] = http_port
        if 'http_port' in ret_obj['data']:
            current_data['http_port'] = ret_obj['data']['http_port']

    if proxy_hostname is not None:
        json_data['proxy_hostname'] = proxy_hostname
        if 'proxy_hostname' in ret_obj['data']:
            current_data['proxy_hostname'] = ret_obj['data']['proxy_hostname']

    if proxy_port is not None:
        json_data['proxy_port'] = proxy_port
        if 'proxy_port' in ret_obj['data']:
            current_data['proxy_port'] = ret_obj['data']['proxy_port']

    if sms_environment is not None:
        json_data['sms_environment'] = sms_environment
        if 'sms_environment' in ret_obj['data']:
            current_data['sms_environment'] = ret_obj['data']['sms_environment']

    if vhost_label is not None:
        json_data['vhost_label'] = vhost_label
        if 'vhost_label' in ret_obj['data']:
            current_data['vhost_label'] = ret_obj['data']['vhost_label']

    if delegation_support is not None:
        json_data['delegation_support'] = delegation_support
        if 'delegation_support' in ret_obj['data']:
            current_data['delegation_support'] = ret_obj['data']['delegation_support']

    if scripting_support is not None:
        json_data['scripting_support'] = scripting_support
        if 'scripting_support' in ret_obj['data']:
            current_data['scripting_support'] = ret_obj['data']['scripting_support']

    sorted_obj1 = tools.json_sort(json_data)
    logger.debug("Sorted sorted_obj1: {0}".format(sorted_obj1))
    sorted_obj2 = tools.json_sort(current_data)
    logger.debug("Sorted sorted_obj2: {0}".format(sorted_obj2))

    if sorted_obj1 != sorted_obj2:
        logger.info("Changes detected, update needed.")
        return True, ret_obj['warnings'], json_data

    return False, ret_obj['warnings'], json_data


def _check_resource_content(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type, name,
                            static_response_headers, rate_limiting_policy, url_aliases, documentation):
    ret_obj = get_a_resource(isamAppliance, instance_name, resource_server_name, path, method, server_type)
    current_data = {
        'policy': ret_obj['data']['policy']
    }

    json_data = {
        'policy': policy,
    }

    if name is not None:
        json_data['name'] = name
        if 'name' in ret_obj['data']:
            current_data['name'] = ret_obj['data']['name']

    if static_response_headers is not None:
        json_data['static_response_headers'] = name
        if 'static_response_headers' in ret_obj['data']:
            current_data['static_response_headers'] = ret_obj['data']['static_response_headers']

    if rate_limiting_policy is not None:
        json_data['rate_limiting_policy'] = name
        if 'rate_limiting_policy' in ret_obj['data']:
            current_data['rate_limiting_policy'] = ret_obj['data']['rate_limiting_policy']

    if url_aliases is not None:
        json_data['url_aliases'] = name
        if 'url_aliases' in ret_obj['data']:
            current_data['url_aliases'] = ret_obj['data']['url_aliases']

    if documentation is not None:
        json_data['documentation'] = name
        if 'documentation' in ret_obj['data']:
            current_data['documentation'] = ret_obj['data']['documentation']

    sorted_obj1 = tools.json_sort(json_data)
    logger.debug("Sorted sorted_obj1: {0}".format(sorted_obj1))
    sorted_obj2 = tools.json_sort(current_data)
    logger.debug("Sorted sorted_obj2: {0}".format(sorted_obj2))

    if sorted_obj1 != sorted_obj2:
        logger.info("Changes detected, update needed.")
        return True, ret_obj['warnings'], json_data

    return False, ret_obj['warnings'], json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare resources between two appliances
    """
    ret_obj1 = get_all_instances(isamAppliance1)
    ret_obj2 = get_all_instances(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2)
