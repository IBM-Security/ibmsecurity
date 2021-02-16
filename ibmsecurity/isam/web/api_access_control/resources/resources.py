import logging
import os

import ibmsecurity
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/wga/apiac/resource/instance"
requires_modules = ["wga"]
requires_version = "9.0.7"


def get_all(isamAppliance, instance_name, resource_server_name, check_mode=False, force=False):
    """
    Retrieve a list of all API Access Control Resources
    """
    return isamAppliance.invoke_get("Retrieve a list of all API Access Control Resources",
                                    "{0}/{1}/server{2}/resource".format(uri, instance_name, resource_server_name),
                                    requires_modules=requires_modules, requires_version=requires_version)


def get(isamAppliance, instance_name, resource_server_name, resource_name, method,
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


def add(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type="standard",
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


def update(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type="standard",
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


def set(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type="standard",
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
        return update(isamAppliance=isamAppliance, instance_name=instance_name,
                      resource_server_name=resource_server_name, method=method, path=path, policy=policy,
                      server_type=server_type, name=name, static_response_headers=static_response_headers,
                      rate_limiting_policy=rate_limiting_policy, url_aliases=url_aliases,
                      documentation=documentation, check_mode=check_mode, force=force)
    else:
        return add(isamAppliance=isamAppliance, instance_name=instance_name,
                   resource_server_name=resource_server_name, method=method, path=path, policy=policy,
                   server_type=server_type, name=name, static_response_headers=static_response_headers,
                   rate_limiting_policy=rate_limiting_policy, url_aliases=url_aliases,
                   documentation=documentation, check_mode=check_mode, force=force)


def delete(isamAppliance, instance_name, resource_server_name, method, path, server_type='standard',
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


def delete_select(isamAppliance, instance_name, resource_server_name, resources, command="DELETE",
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


def delete_all(isamAppliance, instance_name, resource_server_name, server_type='standard',
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


def export_all(isamAppliance, instance_name, resource_server_name, file_path, check_mode=False, force=False):
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


def export_file(isamAppliance, instance_name, resource_server_name, method, path, file_path,
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


def import_file(isamAppliance, instance_name, resource_server_name, filename,
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


def _check_instance_exist(isamAppliance, instance_name):
    ret_obj = ibmsecurity.isam.web.api_access_control.resources.instances.get_all(isamAppliance)

    for obj in ret_obj['data']:
        if obj['name'] == instance_name:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_server_exist(isamAppliance, instance_name, junction_point):
    ret_obj = ibmsecurity.isam.web.api_access_control.resources.servers.get_all(isamAppliance, instance_name)
    for obj in ret_obj['data']:
        if obj['name'] == junction_point:
            return True, ret_obj['warnings']

    return False, ret_obj['warnings']


def _check_resource_exist(isamAppliance, instance_name, resource_server_name, method, path):
    ret_obj = get_all(isamAppliance, instance_name, resource_server_name)
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
    ret_obj = get_all(isamAppliance, instance_name, resource_server_name)
    warnings = ret_obj['warnings']

    if ret_obj['data'] != []:
        return True, warnings
    else:
        return False, warnings


def _check_all_servers(isamAppliance, instance_name):
    ret_obj = ibmsecurity.isam.web.api_access_control.servers.get_all(isamAppliance, instance_name)
    warnings = ret_obj['warnings']

    if ret_obj['data'] != []:
        return True, warnings
    else:
        return False, warnings


def _check_list_resource(isamAppliance, instance_name, resource_server_name, resources):
    ret_obj = get_all(isamAppliance, instance_name, resource_server_name)
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
    ret_obj = ibmsecurity.isam.web.api_access_control.resources.servers.get_all(isamAppliance, instance_name)
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


def _check_resource_content(isamAppliance, instance_name, resource_server_name, method, path, policy, server_type, name,
                            static_response_headers, rate_limiting_policy, url_aliases, documentation):
    ret_obj = get(isamAppliance, instance_name, resource_server_name, path, method, server_type)
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

    app1_instances = ibmsecurity.isam.web.api_access_control.resources.instances.get_all(isamAppliance1)
    app2_instances = ibmsecurity.isam.web.api_access_control.resources.instances.get_all(isamAppliance2)

    instance_diff = tools.json_compare(app1_instances, app2_instances)

    for inst1 in app1_instances['data']:
        for inst2 in app2_instances['data']:
            if inst1['name'] == inst2['name']:
                servers1 = ibmsecurity.isam.web.api_access_control.resources.servers.get_all(isamAppliance1,
                                                                                             instance_name=inst1[
                                                                                                 'name'])
                servers2 = ibmsecurity.isam.web.api_access_control.resources.servers.get_all(isamAppliance2,
                                                                                             instance_name=inst2[
                                                                                                 'name'])
                servers_diff = tools.json_compare(servers1, servers2)

                if servers_diff['data']['matches'] is False:
                    if 'context_difference' in instance_diff['data']:
                        instance_diff['data']['context_difference'].append(
                            servers_diff['data']['context_difference'])
                    else:
                        instance_diff['data']['context_difference'] = (servers_diff['data']['context_difference'])

                    if 'difference' in instance_diff['data']:
                        instance_diff['data']['difference'] += servers_diff['data']['difference']
                    else:
                        instance_diff['data']['difference'] = servers_diff['data']['difference']

                    if 'html_difference' in instance_diff['data']:
                        instance_diff['data']['html_difference'] += servers_diff['data']['html_difference']
                    else:
                        instance_diff['data']['html_difference'] = servers_diff['data']['html_difference']

                    instance_diff['data']['matches'] = False
                    instance_diff['data']['deleted_keys'].append(servers_diff['data']['deleted_keys'])
                for srv1 in servers1['data']:
                    for srv2 in servers2['data']:
                        if srv1['name'] == srv2['name']:
                            resources1 = get_all(isamAppliance1, instance_name=inst1['name'],
                                                 resource_server_name=srv1['name'])
                            resources2 = get_all(isamAppliance2, instance_name=inst1['name'],
                                                 resource_server_name=srv1['name'])
                            resources_diff = tools.json_compare(resources1, resources2)
                            if resources_diff['data']['matches'] is False:
                                if 'context_difference' in instance_diff['data']:
                                    instance_diff['data']['context_difference'].append(
                                        resources_diff['data']['context_difference'])
                                else:
                                    instance_diff['data']['context_difference'] = (
                                    resources_diff['data']['context_difference'])

                                if 'difference' in instance_diff['data']:
                                    instance_diff['data']['difference'] += resources_diff['data']['difference']
                                else:
                                    instance_diff['data']['difference'] = resources_diff['data']['difference']

                                if 'html_difference' in instance_diff['data']:
                                    instance_diff['data']['html_difference'] += resources_diff['data'][
                                        'html_difference']
                                else:
                                    instance_diff['data']['html_difference'] = resources_diff['data'][
                                        'html_difference']

                                instance_diff['data']['matches'] = False
                                instance_diff['data']['deleted_keys'].append(resources_diff['data']['deleted_keys'])

    return instance_diff
