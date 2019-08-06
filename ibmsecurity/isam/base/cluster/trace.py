import logging

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the tracing levels
    """
    return isamAppliance.invoke_get("Retrieve the tracing levels",
                                    "/isam/cluster/tracing/v1")


def _check(isamAppliance, dsc):
    ret_obj = get(isamAppliance)

    if isinstance(dsc, basestring):
        import ast
        dsc = ast.literal_eval(dsc)

    return ret_obj['data']['dsc'] == dsc


def set(isamAppliance, dsc, check_mode=False, force=False):
    """
    Updating the tracing levels
    """
    if force is True or _check(isamAppliance, dsc) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Updating the tracing levels",
                "/isam/cluster/tracing/v1",
                {
                    'dsc': dsc
                })

    return isamAppliance.create_return_object()
