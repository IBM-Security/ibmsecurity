import logging

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current log file language
    """

    return isamAppliance.invoke_get("Retrieve the current log file language",
                                    "/isam/applang/v1"
                                    )


def update(isamAppliance, language, check_mode=False, force=False):
    """
    Change the log file language
    """

    current_obj = get(isamAppliance)
    current_lang = current_obj['data']['id']

    if force is True or current_lang != language:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)

        else:
            return isamAppliance.invoke_post(
                "Change the log file language",
                "/isam/applang/v1",
                {'id': language}
            )

    return isamAppliance.create_return_object()
