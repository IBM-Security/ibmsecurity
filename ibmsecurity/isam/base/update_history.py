def get_all(isamAppliance, check_mode=False, force=False):
    """
    Retrieve a list of all update history records
    """
    return isamAppliance.invoke_get("Retrieve a list of all update history records",
                                    "/updates/history/records.json")


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve all update history records
    """
    return isamAppliance.invoke_get("Retrieve all update history records",
                                    "/updates/history/")
