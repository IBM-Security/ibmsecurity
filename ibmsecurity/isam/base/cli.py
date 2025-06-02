import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/cli"
requires_modules = None
requires_version = "9.0.3.0"


def execute(isamAppliance, command, input=None, check_mode=False, force=False, ignore_error=False):
    """
    Run CLI Command
    """
    post_data = {
        'command': command
    }
    if input is not None:
        post_data['input'] = input

    warnings = ["Idempotency checks are not coded for CLI calls.",
                "All CLI calls will be marked as changed whether a change happens or not."]
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True, warnings=warnings)
    else:
        return isamAppliance.invoke_post("Run CLI Command", uri, post_data, ignore_error=ignore_error,
                                         requires_modules=requires_modules, requires_version=requires_version,
                                         warnings=warnings)
