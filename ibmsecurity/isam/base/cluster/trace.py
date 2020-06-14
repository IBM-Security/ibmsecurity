import logging

logger = logging.getLogger(__name__)
requires_model="Appliance"

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the tracing levels
    """
    return isamAppliance.invoke_get("Retrieve the tracing levels",
                                    "/isam/cluster/tracing/v1", requires_model=requires_model)


def _check(isamAppliance, dsc):

    check_value,warnings = True,""
    ret_obj = get(isamAppliance)
    warnings = ret_obj['warnings']

    if isinstance(dsc, basestring):
        import ast
        dsc = ast.literal_eval(dsc)

    if 'dsc' in ret_obj['data']:
        check_value = (ret_obj['data']['dsc']==dsc)
        return check_value,warnings
    else:
        check_value=True
        return check_value,warnings


def set(isamAppliance, dsc, check_mode=False, force=False):
    """
    Updating the tracing levels
    """

    check_value,warnings = _check(isamAppliance, dsc)
    if force is True or check_value is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put(
                "Updating the tracing levels",
                "/isam/cluster/tracing/v1",
                {
                    'dsc': dsc
                }, requires_model=requires_model)

    return isamAppliance.create_return_object(warnings=warnings)
