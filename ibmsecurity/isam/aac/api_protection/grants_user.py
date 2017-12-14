import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, userid, check_mode=False, force=False):
    """
    Get grants by userid
    """
    return isamAppliance.invoke_get("Get grants by userid",
                                    "/iam/access/v8/grants/userIds/{0}".format(userid))


def get_recent(isamAppliance, userid, timestamp, token_type='refresh_token', check_mode=False, force=False):
    """
    Get grants by userid and tokens more recent than given timestamp, also pass back any other tokens found

    token_type will check refresh tokens and can be changed or ignored by passing None

    other tokens could include recent access tokens (not refresh tokens)
    """
    ret_obj = get(isamAppliance=isamAppliance, userid=userid)

    recent_tokens = []
    other_tokens = []
    for attrbs in ret_obj['data']:
        for tok in attrbs['tokens']:
            if tok['dateCreated'] > timestamp and (tok['subType'] == token_type or token_type is None):
                recent_tokens.append(tok)
            else:
                other_tokens.append(tok)

    new_ret_obj = isamAppliance.create_return_object()
    new_ret_obj['data']['recent'] = recent_tokens
    new_ret_obj['data']['other'] = other_tokens

    return new_ret_obj


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
