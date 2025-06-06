import logging
import json
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the complete list of SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the complete list of SCIM configuration settings",
                                    "/mga/scim/configuration", requires_modules=requires_modules,
                                    requires_version=requires_version)


def get_user_profile(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current user profile SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current user profile SCIM configuration settings",
                                    "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get_ent_profile(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current enterprise user profile SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current enterprise user profile SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def get_isam_user(isamAppliance, check_mode=False, force=False):
    """
    Retrieve configuration of SCIM ISAM user settings
    """
    return isamAppliance.invoke_get("Retrieve configuration of SCIM ISAM user settings",
                                    "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)

def get_ext_auth_service_config(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current external authentication service SCIM configuration
    """
    return isamAppliance.invoke_get("Retrieving the current external authentication service SCIM configuration ",
                                    "{0}/urn:ietf:params:scim:schemas:extension:isam:1.0:MMFA:EAS".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def get_general_config(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current general SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current general SCIM configuration settings",
                                    "{0}/general".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def get_group_config(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current group SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current group SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:core:2.0:Group".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def get_ldap_objs(isamAppliance, ldap_connection, check_mode=False, force=False):
    """
    Retrieving the current list of ldap object classes from the configured ldap
    """
    return isamAppliance.invoke_get("Retrieving the current list of ldap object classes from the configured ldap",
                                    "{0}/urn:ietf:params:scim:schemas:core:2.0:User/ldap_objectclasses?ldap_connection={1}".format(
                                        uri, ldap_connection),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def get_ldap_attrs(isamAppliance, ldap_connection, ldap_objectclasses='', check_mode=False, force=False):
    """
    Retrieving the current list of user associated ldap attributes from the configured
    """
    return isamAppliance.invoke_get(
        "Retrieving the current list of user associated ldap attributes from the configured ",
        "{0}/urn:ietf:params:scim:schemas:core:2.0:User/ldap_attributes?ldap_connection={1}&ldap_objectclasses={1}".format(
            uri, ldap_connection, ldap_objectclasses),
        requires_modules=requires_modules,
        requires_version=requires_version
        )

def update_user_profile(isamAppliance, ldap_connection, user_suffix, search_suffix, check_mode=False, force=False):
    """
    Updating the user profile SCIM configuration settings
    """
    ret_obj = get_user_profile(isamAppliance)
    ret_obj = ret_obj['data']['urn:ietf:params:scim:schemas:core:2.0:User']
    del ret_obj['ldap_connection']
    del ret_obj['user_suffix']
    del ret_obj['search_suffix']

    ret_obj['ldap_connection'] = ldap_connection
    ret_obj['user_suffix'] = user_suffix
    ret_obj['search_suffix'] = search_suffix
    return isamAppliance.invoke_put(
        "Updating the user profile SCIM configuration settings",
        "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User",
        ret_obj, requires_modules=requires_modules,
        requires_version=requires_version)


def update_isam_user(isamAppliance, ldap_connection=None, isam_domain=None, update_native_users=None, connection_type=None, attrs_dir=None, enforce_password_policy=None, check_mode=False, force=False):
    """
    Updating the ISAM user SCIM configuration settings
    """
    ret_obj = get_isam_user(isamAppliance)
    ret_obj = ret_obj['data']['urn:ietf:params:scim:schemas:extension:isam:1.0:User']

    new_obj = {}

    update_required = False

    if ldap_connection is None:
        if 'ldap_connection' in ret_obj:
            new_obj['ldap_connection'] = ret_obj['ldap_connection']
    else:
        new_obj['ldap_connection'] = ldap_connection
        if 'ldap_connection' in ret_obj:
            if ret_obj['ldap_connection'] != ldap_connection:
                update_required = True
        else:
            update_required = True

    if isam_domain is None:
        if 'isam_domain' in ret_obj:
            new_obj['isam_domain'] = ret_obj['isam_domain']
    else:
        new_obj['isam_domain'] = isam_domain
        if 'isam_domain' in ret_obj:
            if ret_obj['isam_domain'] != isam_domain:
                update_required = True
        else:
            update_required = True

    if update_native_users is None:
        if 'update_native_users' in ret_obj:
            new_obj['update_native_users'] = ret_obj['update_native_users']
    else:
        new_obj['update_native_users'] = update_native_users
        if 'update_native_users' in ret_obj:
            if ret_obj['update_native_users'] != update_native_users:
                update_required = True
        else:
            update_required = True

    if connection_type is None:
        if 'connection_type' in ret_obj:
            new_obj['connection_type'] = ret_obj['connection_type']
    else:
        new_obj['connection_type'] = connection_type
        if 'connection_type' in ret_obj:
            if ret_obj['connection_type'] != connection_type:
                update_required = True
        else:
            update_required = True

    if attrs_dir is None:
        if 'attrs_dir' in ret_obj:
            new_obj['attrs_dir'] = ret_obj['attrs_dir']
    else:
        new_obj['attrs_dir'] = attrs_dir
        if 'attrs_dir' in ret_obj:
            if ret_obj['attrs_dir'] != attrs_dir:
                update_required = True
        else:
            update_required = True

    if enforce_password_policy is None:
        if 'enforce_password_policy' in ret_obj:
            new_obj['enforce_password_policy'] = ret_obj['enforce_password_policy']
    else:
        new_obj['enforce_password_policy'] = enforce_password_policy
        if 'enforce_password_policy' in ret_obj:
            if ret_obj['enforce_password_policy'] != enforce_password_policy:
                update_required = True
        else:
            update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating the ISAM user SCIM configuration settings",
                "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User",
                new_obj, requires_modules=requires_modules,
                requires_version=requires_version)

    return isamAppliance.create_return_object(changed=False)




def update_ent_profile(isamAppliance, mappings, check_mode=False, force=False):
    """
    Updating the enterprise user profile SCIM configuration settings

    """
    return isamAppliance.invoke_put("Updating the enterprise user profile SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User".format(uri),
                                    mappings,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )


def update_ext_auth_service_config(isamAppliance, schemas, check_mode=False, force=False):
    """
    Updating the external authentication service SCIM configuration settings
    """
    current_objs = get_ext_auth_service_config(isamAppliance)
    current_configs = current_objs['data']['urn:ietf:params:scim:schemas:extension:isam:1.0:MMFA:EAS']
    ws_connections = ibmsecurity.isam.aac.server_connections.ws.get_all(isamAppliance)
    ws_connections = ws_connections['data']
    update_required = False

    for obj in schemas:
        found = False
        for config in current_configs:
            if obj['connection'] == config['connection']:
                found = True
                new_schemas = obj['schemas']
                old_schemas = config['schemas']
                sorted_new = json_sort(new_schemas)
                sorted_old = json_sort(old_schemas)
                if sorted_new != sorted_old:
                    update_required = True

        if found is False:
            exist = False
            for ws in ws_connections:
                if obj['connection'] == ws['uuid']:
                    update_required = True
                    exist = True
            if exist is False:
                warnings = "Did not find connection {0} in the configured server list.".format(obj['connection'])
                return isamAppliance.create_return_object(changed=False, warnings=warnings)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating the external authentication service SCIM configuration settings",
                                            "{0}/urn:ietf:params:scim:schemas:extension:isam:1.0:MMFA:EAS".format(uri),
                                            schemas,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version
                                            )

    return isamAppliance.create_return_object(changed=False)


def set_all(isamAppliance, settings, check_mode=False, force=False):
    """
    Update entire SCIM settings
    """
    if settings is None or settings == '':
        return isamAppliance.create_return_object(
            warnings=["Need to pass content for scim configuration"])
    else:
        # Feature: Converting python string to dict (if required)
        # Attention: JSON strings must use " quotes according to RFC 8259
        # Example: '{"a":1, "b": 2, "c": 3}'
        if isinstance(settings, str):
            settings = json.loads(settings)
        if force or not _check(isamAppliance, settings):
            if check_mode:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Update SCIM settings",
                    "/mga/scim/configuration",
                    settings)

    return isamAppliance.create_return_object()

def _check(isamAppliance, settings):
    """
    Check if scim configuration is identical with server
    """
    ret_obj = get_all(isamAppliance)
    logger.debug("Comparing server scim configuration with desired configuration.")
    # Converting python ret_obj['data'] and settings from type dict to valid JSON (RFC 8259)
    # e.g. converts python boolean 'True' -> to JSON literal lowercase value 'true'
    cur_json_string = json.dumps(ret_obj['data'])
    cur_sorted_json = json_sort(cur_json_string)
    logger.debug("Server JSON : {0}".format(cur_sorted_json))
    given_json_string = json.dumps(settings)
    given_sorted_json = json_sort(given_json_string)
    logger.debug("Desired JSON: {0}".format(given_sorted_json))
    if cur_sorted_json != given_sorted_json:
        return False
        logger.debug("Changes detected!")
    else:
        logger.debug("Server configuration is identical with desired configuration. No change necessary.")
        return True


def update_group_config(isamAppliance, ldap_object_classes, group_dn, check_mode=False, force=False):
    """
    Updating the group SCIM configuration settings
    """
    obj = get_group_config(isamAppliance)
    obj = obj['data']['urn:ietf:params:scim:schemas:core:2.0:Group']

    current_dn = obj['group_dn']
    current_classes = obj['ldap_object_classes']

    if current_dn == group_dn:
        sorted_new = json_sort(ldap_object_classes)
        sorted_old = json_sort(current_classes)
        if sorted_new == sorted_old:
            update_required = False
        else:
            update_required = True
    else:
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            data = {}
            data['group_dn'] = group_dn
            data['ldap_object_classes'] = ldap_object_classes
            return isamAppliance.invoke_put("Updating the group SCIM configuration settings",
                                            "{0}/urn:ietf:params:scim:schemas:core:2.0:Group".format(uri),
                                            data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version
                                            )

    return isamAppliance.create_return_object(changed=False)


def update_mode(isamAppliance, schema_name, scim_attribute, mode, scim_subattribute=None, check_mode=False,
                force=False):
    """
    Updating the mode of a SCIM attribute
    """

    ret_obj = get_general_config(isamAppliance)

    mode = mode.lower()

    objs = ret_obj['data']['attribute_modes']

    update_required = True

    if scim_subattribute is None:
        obj1 = {'mode': mode, 'attribute': scim_attribute}
    else:
        obj1 = {'mode': mode, 'attribute': scim_attribute, 'subattribute': scim_subattribute}

    obj1 = json_sort(obj1)

    for obj in objs:
        schema = obj['schema']
        if schema == schema_name:
            modes = obj['modes']
            for anitem in modes:
                obj2 = json_sort(anitem)
                if obj1 == obj2:
                    update_required = False

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:

            if scim_subattribute is None:
                return isamAppliance.invoke_put("Updating the mode of a SCIM attribute",
                                                "{0}/general/attribute_modes/{1}/{2}".format(uri, schema_name,
                                                                                             scim_attribute),
                                                {'mode': mode},
                                                requires_modules=requires_modules,
                                                requires_version=requires_version
                                                )
            else:
                return isamAppliance.invoke_put("Updating the mode of a SCIM attribute",
                                                "{0}/general/attribute_modes/{1}/{2}/{3}".format(uri, schema_name,
                                                                                                 scim_attribute,
                                                                                                 scim_subattribute),
                                                {'mode': mode},
                                                requires_modules=requires_modules,
                                                requires_version=requires_version
                                                )

    return isamAppliance.create_return_object(changed=False)


def reset_mode(isamAppliance, schema_name, scim_attribute, scim_subattribute=None, check_mode=False, force=False):
    """
    Resetting a SCIM attribute mode to default
    """
    ret_obj = get_general_config(isamAppliance)

    objs = ret_obj['data']['attribute_modes']

    update_required = False

    for obj in objs:
        schema = obj['schema']
        if schema == schema_name:
            modes = obj['modes']
            for anitem in modes:
                if anitem['attribute'] == scim_attribute:
                    if scim_subattribute is not None:
                        if 'subattribute' in anitem:
                            if anitem['subattribute'] == scim_subattribute:
                                update_required = True
                    elif ('subattribute' in anitem) is False:
                        update_required = True


    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            if scim_subattribute is None:
                return isamAppliance.invoke_delete("Resetting a SCIM attribute mode to default",
                                               "{0}/general/attribute_modes/{1}/{2}".format(uri, schema_name,
                                                                                            scim_attribute),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version
                                               )
            else:
                return isamAppliance.invoke_delete("Resetting a SCIM attribute mode to default",
                                               "{0}/general/attribute_modes/{1}/{2}/{3}".format(uri, schema_name,
                                                                                                scim_attribute,
                                                                                                scim_subattribute),
                                               requires_modules=requires_modules,
                                               requires_version=requires_version
                                               )

    return isamAppliance.create_return_object(changed=False)
