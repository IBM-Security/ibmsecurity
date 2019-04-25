import logging
import ibmsecurity.utilities.tools
import os.path
from ibmsecurity.isam.web.reverse_proxy.management_root import directory
from ibmsecurity.isam.web.reverse_proxy.management_root import file

logger = logging.getLogger(__name__)


def export_zip(isamAppliance, instance_id, filename, check_mode=False, force=False):
    """
    Exporting the contents of the administration pages root as a .zip file

    :param isamAppliance:
    :param instance_id:
    :param filename:
    :param check_mode:
    :param force:
    :return:
    """
    if force is True or os.path.exists(filename) is False:
        if check_mode is False:
            return isamAppliance.invoke_get_file(
                "Exporting the contents of the administration pages root as a .zip file",
                "/wga/reverseproxy/{0}/management_root?index=&name=&enc_name=&type=&browser=".format(instance_id),
                filename)

    return isamAppliance.create_return_object()


def import_zip(isamAppliance, instance_id, filename, check_mode=False, force=False):
    """
    Importing the contents of a .zip file to the administration pages root
    """
    if check_mode is True:
        return isamAppliance.create_return_object(changed=True)
    else:
        return isamAppliance.invoke_post_files(
            "Importing the contents of a .zip file to the administration pages root",
            "/wga/reverseproxy/{0}/management_root".format(instance_id),
            [
                {
                    'file_formfield': 'file',
                    'filename': filename,
                    'mimetype': 'application/octet-stream'
                }
            ],
            {
                'type': 'file',
                'force': force
            })


def check(isamAppliance, instance_id, id, name, type, check_mode=False, force=False):
    ret_obj = None

    if (type.lower() == 'directory'):
        ret_obj = directory._check(isamAppliance, instance_id, id, name)
    elif (type.lower() == 'file'):
        ret_obj = file._check(isamAppliance, instance_id, id, name)
    else:
        type = 'unknown'

    data = {
        'id': ret_obj,
        'top': id,
        'name': name,
        'type': type
    }

    return isamAppliance.create_return_object(data=data)
