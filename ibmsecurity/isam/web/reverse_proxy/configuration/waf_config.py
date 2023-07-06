import logging
import ibmsecurity.utilities.tools
import os.path

logger = logging.getLogger(__name__)

requires_modules = ["wga"]
requires_version = "10.0.5.0"


def get(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Retrieving the WAF configuration file (modsecurity.conf)
    """
    return isamAppliance.invoke_get("Retrieving the WAF configuration file",
     "/isam/advanced_configuration/{0}?component=waf".format(instance_name))


def export_file(isamAppliance, instance_name, filename, check_mode=False, force=False):
    """
    Exporting the WAF configuration file (modsecurity.conf)
    """
    if force is True or os.path.exists(filename) is False:
        if check_mode is False:
            return isamAppliance.invoke_get_file(
            "Exporting the WAF configuration file",
            "/isam/advanced_configuration/{0}?export&component=waf".format(instance_name),
            filename)

    return isamAppliance.create_return_object()


def revert(isamAppliance, instance_name, check_mode=False, force=False):
    """
    Reverting a previously updated WAF configuration file
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Reverting a previously updated WAF configuration file",
            "/isam/advanced_configuration/{0}&component=waf".format(instance_name),
            {
                'operation': 'revert'
            })


def update(isamAppliance, instance_name, file_contents, check_mode=False, force=False):
    """
    Updating the WAF configuration file
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put(
            "Updating the WAF configuration file",
            "/isam/advanced_configuration/{0}?component=waf".format(instance_name),
            {
                'file_contents': file_contents
            })


def compare(isamAppliance1, isamAppliance2, resource_id):
    """
    Compare stanzas within resource between two appliances
    """
    ret_obj1 = get(isamAppliance1, resource_id)
    ret_obj2 = get(isamAppliance2, resource_id)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1=ret_obj1, ret_obj2=ret_obj2, deleted_keys=[])
