import logging

logger = logging.getLogger(__name__)


def get(isvgAppliance, check_mode=False, force=False):
    """
    Retrieve available updates
    """
    return isvgAppliance.invoke_get("Retrieving available updates",
                                    "/updates/available.json")


def discover(isvgAppliance, check_mode=False, force=False):
    """
    Discover available updates
    """
    return isvgAppliance.invoke_get("Discover available updates",
                                    "/updates/available/discover")


def upload(isvgAppliance, file, check_mode=False, force=False):
    """
    Upload Available Update
    """
    if force is True or _check_file(isvgAppliance, file) is False:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            return isvgAppliance.invoke_post_files(
                "Upload Available Update",
                "/updates/available",
                [{
                    'file_formfield': 'uploadedfile',
                    'filename': file,
                    'mimetype': 'application/octet-stream'
                }],
                {}, json_response=False)

    return isvgAppliance.create_return_object()


def _check_file(isvgAppliance, file):
    """
    Parse the file name to see if it is already uploaded - use version and release date from pkg file name
    Also check to see if the firmware level is already uploaded
    Note: Lot depends on the name of the file.

    :param isvgAppliance:
    :param file:
    :return:
    """
    import os.path

    # If there is an exception then simply return False
    # Sample filename - 8.0.1.9-ISS-ISVG_20181207-0045.pkg
    logger.debug("Checking provided file is ready to upload: {0}".format(file))
    try:
        # Extract file name from path
        f = os.path.basename(file)
        fn = os.path.splitext(f)
        logger.debug("File name without path: {0}".format(fn[0]))

        # Split of file by '-' hyphen and '_' under score
        import re
        fp = re.split('-|_', fn[0])
        firm_file_version = fp[0]
        firm_file_product = fp[2]
        firm_file_date = fp[3]
        logger.debug("PKG file details: {0}: version: {1} date: {2}".format(firm_file_product, firm_file_version, firm_file_date))

        # Check if firmware level already contains the update to be uploaded or greater, check Active partition
        # firmware "name" of format - 8.0.1.9-ISS-ISVG_20181207-0045
        import ibmsecurity.isvg.firmware
        ret_obj = ibmsecurity.isvg.firmware.get(isvgAppliance)
        for firm in ret_obj['data']:
            # Split of file by '-' hyphen and '_' under score
            fp = re.split('-|_', firm['name'])
            firm_appl_version = fp[0]
            firm_appl_product = fp[2]
            firm_appl_date = fp[3]
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
        ret_obj = get(isvgAppliance)
        for upd in ret_obj['data']:
            rd = upd['release_date']
            rd = rd.replace('-', '')  # turn release date into 20161102 format from 2016-11-02
            if upd['version'] == fp[0] and rd == fp[3]:  # Version of format 8.0.1.9
                return True
    except Exception as e:
        logger.debug("Exception occured: {0}".format(e))
        pass

    return False


def install(isvgAppliance, type, version, release_date, name, check_mode=False, force=False):
    """
    Install Available Update
    """
    if force is True or _check(isvgAppliance, type, version, release_date, name) is True:
        if check_mode is True:
            return isvgAppliance.create_return_object(changed=True)
        else:
            # obtain appliance lastboot time
            import ibmsecurity.isvg.firmware
            import time
            ret_obj_appliance = ibmsecurity.isvg.firmware.get(isvgAppliance)
            for firm in ret_obj_appliance['data']:
                if firm['active'] is True:
                    before_install_last_boot = firm['last_boot']
                    logger.info(
                        "Active partition last boot time {0} before firmware installation.".format(before_install_last_boot))

            # proceed with firmware installation
            ret_obj = isvgAppliance.invoke_post("Install Available Update",
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
            isvgAppliance.facts['version'] = version

            # isvg appliance has so much work to do after installing the firmware, it can take up
            # to several minutes before it reboots by itself.
            # Loop until appliance returns an error, or reboot is detected, before returning control.
            try:
                while True:
                    ret_obj_appliance = ibmsecurity.isvg.firmware.get(isvgAppliance)
                    for firm in ret_obj_appliance['data']:
                        if firm['active'] is True:
                            last_boot = firm['last_boot']
                            logger.info(
                                "Active partition last boot time {0} after firmware installation.".format(last_boot))
                            if last_boot > before_install_last_boot:
                                raise Exception ("Break out of loop")
                    time.sleep(30)
            except Exception as e:
                logger.debug("Exception occured: {0}. Assuming appliance has now initiated reboot process".format(e))
                pass

            return ret_obj

    return isvgAppliance.create_return_object()


def _check(isvgAppliance, type, version, release_date, name):
    ret_obj = get(isvgAppliance)
    for upd in ret_obj['data']:
        # If there is an installation in progress then abort
        if upd['state'] == 'Installing':
            logger.debug("Detecting a state of installing...")
            return False
        if upd['type'] == type and upd['version'] == version and upd['release_date'] == release_date and upd[
            'name'] == name:
            logger.debug("Requested firmware ready for install...")
            return True

    logger.debug("Requested firmware not available for install...")

    return False
