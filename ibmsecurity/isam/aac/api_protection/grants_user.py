import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, userid, check_mode=False, force=False):
    """
    Get grants by userid
    """
    return isamAppliance.invoke_get("Get grants by userid",
                                    "/iam/access/v8/grants/userIds/{0}".format(userid))


def delete(isamAppliance, userid, check_mode=False, force=False):
    """
    Delete grants by userid
    """
    if force is True or _check(isamAppliance, userid) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Delete grants by userid",
                                               "/iam/access/v8/grants/userIds/{0}".format(userid))

    return isamAppliance.create_return_object()


def _check(isamAppliance, userid):
    try:
        ret_obj = get(isamAppliance, userid)
        if len(ret_obj['data']) > 0:
            return True
    except:
        pass

    return False
