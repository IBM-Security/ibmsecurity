import logging
import ibmsecurity.utilities.tools
from ibmsecurity.isam.web.reverse_proxy import junctions

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "10.0.2.0"


def config(isamAppliance, instance_id, junction="/ivg", mmfa=True, check_mode=False):
    """
    IVG configuration for a reverse proxy instance

    :param isamAppliance:
    :param instance_id:
    :param junction:
    :param mmfa:
    :param check_mode:
    :return:
    """
    warnings = []
    json_data = {
        "junction": junction,
        "mmfa": mmfa
    }
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        return isamAppliance.invoke_post(
            "IVG configuration for a reverse proxy instance",
            "/wga/reverseproxy/{0}/verify_gateway_config".format(instance_id), json_data, warnings=warnings,
            requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object(warnings=warnings)
