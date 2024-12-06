import logging

from ibmsecurity.utilities import tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/iam/access/v8/audit/components"
requires_modules = ["mga", "federation"]
requires_version = None


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve audit configuration
    """
    return isamAppliance.invoke_get("Retrieve all audit component configuration", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def search(isamAppliance, component_name: str, check_mode=False, force=False):
    """
    Get the id for the component by (group) name
    """
    ret_obj = None

    ret_obj = get_all(isamAppliance)
    if ret_obj.get("data", None):
        for obj in ret_obj.get("data"):
            if obj['group'] == component_name:
                logger.info(f"Found name {component_name} id: {obj['id']}")
                return obj['id']
        return None
    else:
        return None


def get(isamAppliance, group_name: str = None, component_id: str = None, type_id: str = None, check_mode=False, force=False):
    """
    Retrieve specific audit configuration component group by component_id, by type or by group name
    """
    requires_version = None
    warnings = []
    if component_id is None and type_id is None and group_name is None:
        warnings = ['No group_name, component_id nor type_id passed']
        return isamAppliance.create_return_object(warnings)
    elif group_name:
        # translate name to component_id
        component_id = search(isamAppliance, component_name=group_name)
        if component_id:
            uri_part = component_id
        else:
            warnings = [f"Cannot find group by name of: {group_name}"]
            return isamAppliance.create_return_object(warnings)
    elif component_id:
        # Ignore type_id in this case
        uri_part = component_id
    else:
        # valid values are runtime or management
        if type_id in ['runtime', 'management']:
            requires_version = "10.0.7.0"
            uri_part = type_id
        else:
            warnings = [f"Invalid type_id passed to function: {type_id}"]
            return isamAppliance.create_return_object(warnings)
    return isamAppliance.invoke_get("Retrieve audit configuration component ", f"{uri}/{uri_part}", requires_modules=requires_modules,
                                    requires_version=requires_version, warnings=warnings)


def set(isamAppliance, component_id: str, enabled=True, check_mode=False, force=False):
    """
    Update Audit Configuration Component by id
    This simply enables or disables the group.
    TODO: Add set by type and set_all
    """
    if isinstance(enabled, str):
        if enabled.upper() in ['TRUE', 'YES']:
            enabled = True
        else:
            enabled = False
    update_required = _check(isamAppliance, component_id, enabled)
    if enabled:
        json_data = {
            'enabled': True
        }
    else:
        json_data = {
            'enabled': False
        }
    if force or update_required:
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Update Audit Configuration Component",
                f"{uri}/{component_id}",
                json_data,
                requires_modules=requires_modules,
                requires_version=requires_version)


def _check(isamAppliance, component_id: str, enabled: bool):
    """
    Check and return True if update needed
    """
    update_required = False

    ret_obj = get(isamAppliance, component_id=component_id)
    cmp_cfg = ret_obj.get("data", None)
    logger.debug(f"\n\n{cmp_cfg}\n\n")
    if cmp_cfg is not None and str(cmp_cfg.get('enabled', "frottekop")) != str(enabled):
        update_required = True
        logger.debug(f"\n\nAudit Configuration Component requires an update {cmp_cfg.get('enabled')} <> {enabled}")
    else:
        logger.warning("Audit Configuration Component does not need an update or does not exist.")

    return update_required


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Audit Configuration Components between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    for obj in ret_obj1['data']:
        del obj['id']
    for obj in ret_obj2['data']:
        del obj['id']

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['id'])
