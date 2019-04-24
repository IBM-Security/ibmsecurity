import logging
from ibmsecurity.isam.web.reverse_proxy.configuration import entry

logger = logging.getLogger(__name__)
requires_modules = ["wga"]
requires_version = "9.0.3.0"


def config(isamAppliance, instance_id, lmi, runtime, reuse_acls=None, reuse_certs=None, channel=None,
           check_mode=False, force=False):
    """
    MMFA configuration for a reverse proxy instance
    """
    if force is True or _check_config(isamAppliance, instance_id) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                "lmi": lmi,
                "runtime": runtime
            }
            # Add optional values to the JSON
            if reuse_acls is not None and reuse_acls != '':
                json_data['reuse_acls'] = reuse_acls
            if reuse_certs is not None and reuse_certs != '':
                json_data['reuse_certs'] = reuse_certs
            if channel is not None and channel != '':
                json_data['channel'] = channel
            return isamAppliance.invoke_post(
                "MMFA configuration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/mmfa_config".format(instance_id), json_data,
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def unconfig(isamAppliance, instance_id, check_mode=False, force=False):
    """
    MMFA unconfiguration for a reverse proxy instance
    """
    if force is True or _check_config(isamAppliance, instance_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "MMFA unconfiguration for a reverse proxy instance",
                "/wga/reverseproxy/{0}/mmfa_config".format(instance_id),
                requires_modules=requires_modules, requires_version=requires_version)

    return isamAppliance.create_return_object()


def _check_config(isamAppliance, instance_id):
    """
    Check webseal config stanza / entry for autoconfig flag to determine if config already done

    :param isamAppliance:
    :param instance_id:
    :return:
    """
    try:
        ret_obj = entry.get(isamAppliance, instance_id, "mmfa-config-info", "autoconfig")
        if ret_obj['data']['autoconfig'] == ["mmfa"]:
            logger.info(
                "WebSEAL entry mmfa-config-info:autoconfig has value {}. 'mmfa' means config already done.".format(
                    ret_obj['data']))
            return True
    except:
        pass

    return False
