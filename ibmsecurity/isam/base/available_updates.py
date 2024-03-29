import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve available updates
    """
    return isamAppliance.invoke_get("Retrieving available updates",
                                    "/updates/available.json")


def discover(isamAppliance, check_mode=False, force=False):
    """
    Discover available updates
    """
    return isamAppliance.invoke_get("Discover available updates",
                                    "/updates/available/discover")


def upload(isamAppliance, file, check_mode=False, force=False):
    """
    Upload Available Update
    """
    if force is True or _check_file(isamAppliance, file) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post_files(
                "Upload Available Update",
                "/core/updates/available",
                [{
                    'file_formfield': 'uploadedfile',
                    'filename': file,
                    'mimetype': 'application/octet-stream'
                }],
                {}, json_response=False)

    return isamAppliance.create_return_object()


def _check_file(isamAppliance, file):
    """
    Parse the file name to see if it is already uploaded - use version and release date from pkg file name
    Also check to see if the firmware level is already uploaded
    Note: Lot depends on the name of the file.

    :param isamAppliance:
    :param file:
    :return:
    """
    import os.path

    # If there is an exception then simply return False
    # Sample filename - isam_9.0.2.0_20161102-2353.pkg
    logger.debug("Checking provided file is ready to upload: {0}".format(file))
    try:
        # Extract file name from path
        f = os.path.basename(file)
        fn = os.path.splitext(f)
        logger.debug("File name without path: {0}".format(fn[0]))

        # Split of file by '-' hyphen and '_' under score
        import re
        fp = re.split('-|_', fn[0])
        firm_file_version = fp[1]
        firm_file_product = fp[0]
        firm_file_date = fp[2]
        logger.debug("PKG file details: {0}: version: {1} date: {2}".format(firm_file_product, firm_file_version, firm_file_date))

        # Check if firmware level already contains the update to be uploaded or greater, check Active partition
        # firmware "name" of format - isam_9.0.2.0_20161102-2353
        import ibmsecurity.isam.base.firmware
        ret_obj = ibmsecurity.isam.base.firmware.get(isamAppliance)
        for firm in ret_obj['data']:
            # Split of file by '-' hyphen and '_' under score
            fp = re.split('-|_', firm['name'])
            firm_appl_version = fp[1]
            firm_appl_product = fp[0]
            firm_appl_date = fp[2]
            logger.debug("Partition details ({0}): {1}: version: {2} date: {3}".format(firm['partition'], firm_appl_product, firm_appl_version, firm_appl_date))
            if firm['active'] is True:
                from ibmsecurity.utilities import tools
                if tools.version_compare(firm_appl_version, firm_file_version) >= 0:
                    logger.info(
                        "Active partition has version {0} which is greater or equals than install package at version {1}.".format(
                            firm_appl_version, firm_file_version))
                    return True
                else:
                    logger.info(
                        "Active partition has version {0} which is smaller than install package at version {1}.".format(
                            firm_appl_version, firm_file_version))

        # Check if update uploaded - will not show up if installed though
        ret_obj = get(isamAppliance)
        for upd in ret_obj['data']:
            rd = upd['release_date']
            rd = rd.replace('-', '')  # turn release date into 20161102 format from 2016-11-02
            if upd['version'] == fp[1] and rd == fp[2]:  # Version of format 9.0.2.0
                return True
    except Exception as e:
        logger.debug("Exception occured: {0}".format(e))
        pass

    return False


def install(isamAppliance, type, version, release_date, name, check_mode=False, force=False):
    """
    Install Available Update
    """
    if force is True or _check(isamAppliance, type, version, release_date, name) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            ret_obj = isamAppliance.invoke_post("Install Available Update",
                                                "/updates/available/install",
                                                {"updates": [
                                                    {
                                                        "type": type,
                                                        "version": version,
                                                        "release_date": release_date,
                                                        "name": name
                                                    }
                                                ]
                                                })
            isamAppliance.facts['version'] = version
            return ret_obj

    return isamAppliance.create_return_object()

def _check(isamAppliance, type, version, release_date, name):
    ret_obj = get(isamAppliance)
    warnings = []
    for upd in ret_obj['data']:
        # If there is an installation in progress then abort
        # API changed in v10.0.5.0 , state, schedule_date,
        #   iso_scheduled_date and expired_install are no longer available.
        if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts["version"], "10.0.5.0") >= 0:
            if 'state' in upd and upd['state'] == 'Installing':
                logger.debug("Detecting a state of installing...")
                return False
        else:
            warnings.append("Appliance at version: {0}, state can no longer be checked in 10.0.5.0 or higher. Ignoring for this call.".format(
                    isamAppliance.facts["version"]))

        logger.info(upd)

        if upd['type'] == type and upd['version'] == version and \
                upd['release_date'] == release_date and upd['name'] == name:
            logger.debug("Requested firmware ready for install...")
            return True

    logger.debug("Requested firmware not available for install...")

    return False
