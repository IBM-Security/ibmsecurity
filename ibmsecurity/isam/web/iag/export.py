import logging
import os
from io import open
import ibmsecurity.isam.web.reverse_proxy.instance as rp

logger = logging.getLogger(__name__)

# URI for this module
uri = "/wga/iag/export"
requires_modules = ["wga"]
requires_version = "10.0.4"

def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the wga features for iag
    """
    return isamAppliance.invoke_get("Retrieving the IAG features", f"{uri}/features",
                                    requires_version=requires_version, requires_modules=requires_modules)

def get(isamAppliance, instance, check_mode=False, force=False):
    """
    Retrieving the wga junctions for a specific instance for iag
    """
    if rp._check(isamAppliance, instance):
        return isamAppliance.invoke_get(f"Retrieving the IAG junction for {instance}", f"{uri}/{instance}/junctions",
                                        requires_version=requires_version, requires_modules=requires_modules)
    else:
        logger.debug(f"Instance: {instance} does not exist")
        return isamAppliance.create_return_object(warnings=f"Instance: {instance} does not exist", rc=1)


def download(isamAppliance, instance, junctions, features, filename="iag.zip", check_mode=False, force=False):
    """
    Downloads the configuration for the instance and junction and features
    It will delete the file if it exists already only if force=True.
    """
    if force or rp._check(isamAppliance, instance):
        if force and os.path.exists(filename):
          os.remove(filename)
          logger.debug(f"Removed {filename}")

        if not check_mode:
          json_data = {
               "junctions": junctions,
               "features": features
               }
          zip_data = isamAppliance.invoke_post(f"Exporting junctions and features for IAG for {instance}", f"{uri}/{instance}/download", data=json_data,
                                               requires_version = requires_version, requires_modules = requires_modules)
          with open(filename, 'wb') as f:
             f.write(zip_data['data'])
        else:
          return isamAppliance.create_return_object(warnings=f"Skipped export, we are in check_mode {check_mode}",
                                                      rc=0)
    else:
        logger.debug(f"Instance: {instance} does not exist, cannot export")
        return isamAppliance.create_return_object(warnings=f"Instance: {instance} does not exist, cannot export", rc=1)

def validate(isamAppliance, instance, junctions, features, check_mode=False, force=False):
    """
    Returns an overview of the junctions and features with warnings.
    """
    if rp._check(isamAppliance, instance):
        json_data = {
            "junctions": junctions,
            "features": features
        }

        return isamAppliance.invoke_post(f"Exporting junctions and features for IAG for {instance}", f"{uri}/{instance}/validate", data=json_data,
                                         requires_version=requires_version, requires_modules=requires_modules)

    else:
        logger.debug(f"Instance: {instance} does not exist, cannot export")
        return isamAppliance.create_return_object(warnings=f"Instance: {instance} does not exist, cannot export", rc=1)
