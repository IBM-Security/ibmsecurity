import logging

logger = logging.getLogger(__name__)

uri = "/mga/runtime_profile/cluster/v1"
requires_modules = ["mga", "federation"]
requires_version = "8.0.0.0"


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the status of the clustered runtime profiles
    """
    return isamAppliance.invoke_get("Retrieving the status of the clustered runtime profiles",
                                    "{0}".format(uri),
                                    requires_modules=requires_modules, requires_version=requires_version)


def execute(isamAppliance, operation, check_mode=False, force=False):
    """
    Stopping, starting, restarting, or reloading the clustered runtime profiles

    :param isamAppliance:
    :param operation:
    :return:
    """

    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_put("Stopping, starting, restarting, or reloading the clustered runtime profiles",
                                        "{0}".format(uri),
                                        {
                                            'operation': operation
                                        },
                                        requires_modules=requires_modules,
                                        requires_version=requires_version)
