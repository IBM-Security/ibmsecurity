import logging
import ibmsecurity.utilities.tools

try:
    basestring
except NameError:
    basestring = (str, bytes)

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/xforce_updates_cfg"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Get Scheduled Security Updates
    """
    return isamAppliance.invoke_get("Get Scheduled Security Updates", uri, requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, enableAutoCheck=True, scheduleSettings=None, dailyFrequencySettings=None, schedule_type=None,
        check_mode=False, force=False):
    """
    Set Scheduled Security Update Settings
    Note: Sample values to be set:
        schedule_type: "day_or_week"
        scheduleSettings: {"day":"Sunday","time":"03:00"}
        dailyFrequencySettings: None
        OR
        schedule_type: "interval"
        dailyFrequencySettings: {"interval":60}
        scheduleSettings: None
        OR
        schedule_type: None
        dailyFrequencySettings: None
        scheduleSettings: None
    """
    update_required, json_data = _check(isamAppliance, enableAutoCheck=enableAutoCheck,
                                        scheduleSettings=scheduleSettings,
                                        dailyFrequencySettings=dailyFrequencySettings,
                                        schedule_type=schedule_type)

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Set Scheduled Security Update Settings", uri, json_data,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check(isamAppliance, enableAutoCheck, scheduleSettings, dailyFrequencySettings, schedule_type):
    update_required = False
    json_data = {
        "config": {
            "enableAutoCheck": enableAutoCheck,
            "dailyFrequencySettings": None,
            "scheduleSettings": None
        }
    }
    ret_obj = get(isamAppliance)

    if schedule_type == 'day_or_week':
        json_data['config']['scheduleSettings'] = scheduleSettings
    elif schedule_type == 'interval':
        if 'interval' in dailyFrequencySettings and isinstance(dailyFrequencySettings['interval'], basestring):
            dailyFrequencySettings['interval'] = int(dailyFrequencySettings['interval'])
            logger.debug("fixing interval")
        json_data['config']['dailyFrequencySettings'] = dailyFrequencySettings

    sorted_json_data = ibmsecurity.utilities.tools.json_sort(json_data)
    logger.debug(f"Sorted input: {sorted_json_data}")
    sorted_ret_obj = ibmsecurity.utilities.tools.json_sort(ret_obj['data'])
    logger.debug(f"Sorted existing data: {sorted_ret_obj}")
    if sorted_ret_obj != sorted_json_data:
        logger.info("Changes detected, update needed.")
        json_data["schedule_type"] = schedule_type
        update_required = True

    return update_required, json_data


def compare(isamAppliance1, isamAppliance2):
    """
    Compare Scheduled Security Update Settings between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
