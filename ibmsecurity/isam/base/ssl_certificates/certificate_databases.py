import logging
import zipfile
import shutil
import json
# from codecs import ignore_errors

from ibmsecurity.utilities.tools import get_random_temp_dir
from ibmsecurity.utilities.tools import json_equals

logger = logging.getLogger(__name__)
requires_model = "Appliance"

certificate_database_optional_args = (
    "token_label",
    "serial_number",
    "passcode",
    "hsm_type",
    "ip",
    "port",
    "kneti_hash",
    "esn",
    "use_rfs",
    "rfs",
    "rfs_port",
    "rfs_auth",
    "safenet_pw",
    "secondary_ip",
    "secondary_port",
    "secondary_kneti_hash",
    "secondary_esn",
    "update_zip"
)
certificate_database_new_10_05 = (
    "safenet_keystore_list",
    "safenet_primary_keystore",
    "safenet_user"
)
certificate_database_new_10_08 = (
    "serial_number"
)


def get_all(isamAppliance, check_mode=False, force=False):
    """
    Get list of all certificate databases
    """
    return isamAppliance.invoke_get("Retrieving all current certificate database names",
                                    "/isam/ssl_certificates")


def get(isamAppliance, cert_dbase_id, check_mode=False, force=False):
    """
    Retrieving the SSL certificate database details
    """

    retObj = isamAppliance.invoke_get("Retrieving the SSL certificate database details",
                                    f"/isam/ssl_certificates/{cert_dbase_id}/details",
                                    requires_model=requires_model,
                                    ignore_error=True)
    if retObj.get('rc', 0) == 404:
        return isamAppliance.create_return_object(rc=404, warnings=[f"{cert_dbase_id} does not exist"])
    else:
        return retObj


def create(isamAppliance, kdb_name, type='kdb',
           check_mode=False, force=False,
           **kwargs,
          ):
    """
    Create a certificate database
               token_label=None,
           serial_number=None,
           passcode=None,
           hsm_type=None,
           ip=None, port=None, kneti_hash=None, esn=None,
           secondary_ip=None, secondary_port=None, secondary_kneti_hash=None, secondary_esn=None,
           use_rfs=None,
           rfs=None, rfs_port=None, rfs_auth=None, safenet_user=None, safenet_pw=None,
           update_zip=None,
           safenet_keystore_list=None, safenet_primary_keystore=None,
    TODO: Update zip does not work atm.
    """
    warnings = []
    if force or not _check(isamAppliance, kdb_name):
        if check_mode:
            return isamAppliance.create_return_object(changed=True)
        else:
            json_data = {
                    "kdb_name": kdb_name,
                    "type": type,
                }
            for k, v in kwargs.items():
               if k in certificate_database_optional_args:
                    json_data[k] = v
               # new in 10.0.5
               if k in certificate_database_new_10_05:
                   if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.5.0") < 0:
                       warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.5.0 or higher. Ignoring {k} for this call.")
                   else:
                       json_data[k] = v
               # new in 10.0.8
               if k in certificate_database_new_10_08:
                   if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.8.0") < 0:
                       warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.8.0 or higher. Ignoring {k} for this call.")
                   else:
                       json_data[k] = v
               # Logic
               if type != 'p11' or json_data.get("hsm_type", None) not in ("safenet","safenet-ha"):
                   # warnings.append("Serial number, safenet_* are only valid for safenet hsm, removed from input")
                   json_data.pop("serial_number", None)
                   json_data.pop("safenet_user", None)
                   json_data.pop("safenet_pw", None)
                   json_data.pop("safenet_keystore_list", None)
                   json_data.pop("safenet_primary_keystore", None)
               if type != 'p11' or json_data.get("hsm_type", None) != "ncipher":
                   warnings.append("kneti_hash, port, secondary_*, rfs are only valid for ncipher hsm, removed from input")
                   json_data.pop("port", None)
                   json_data.pop("kneti_hash", None)
                   json_data.pop("secondary_ip", None)
                   json_data.pop("secondary_port", None)
                   json_data.pop("secondary_kneti_hash", None)
                   json_data.pop("secondary_esn", None)
                   json_data.pop("use_rfs", None)
                   json_data.pop("rfs", None)
                   json_data.pop("rfs_port", None)
                   json_data.pop("rfs_auth", None)

               retObj = isamAppliance.invoke_post( f"Creating certificate database {kdb_name}",
                  "/isam/ssl_certificates",
                  json_data,
                  warnings=warnings,
                  ignore_error=True
               )
               if retObj.get("rc", 0) == 400:
                   warnings.append(f"Invalid type (you need to install an extension to support network hsm {type})")
                   return isamAppliance.create_return_object(warnings=warnings)
               else:
                   return retObj

    return isamAppliance.create_return_object()


def delete(isamAppliance, cert_dbase_id, check_mode=False, force=False):
    """
    Delete a certificate database
    """
    if force is True or _check(isamAppliance, cert_dbase_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete(
                "Deleting a certificate database",
                f"/isam/ssl_certificates/{cert_dbase_id}")

    return isamAppliance.create_return_object()


def export_db(isamAppliance, cert_id, filename, check_mode=False, force=False):
    """
    Export a certificate database
    """
    import os.path

    if force is True or (_check(isamAppliance, cert_id) is True and os.path.exists(filename) is False):
        if check_mode is False:  # No point downloading a file if in check_mode
            return isamAppliance.invoke_get_file(
                "Export a certificate database",
                f"/isam/ssl_certificates/{cert_id}?export",
                filename)

    return isamAppliance.create_return_object()


def import_db(isamAppliance, kdb, stash, zip=None, check_mode=False, force=False):
    """
    Import certificate database
    """
    # Grab the filename to use as identifier (strip path and extension)
    import os.path

    tmpdir=None
    if zip != None:
        with zipfile.ZipFile(zip,"r") as zip_ref:
            tmpdir = get_random_temp_dir()
            zip_ref.extractall(tmpdir)
            kdb = tmpdir + '/' + kdb
            stash = tmpdir + '/' + stash

    kdb_id = os.path.basename(kdb)
    kdb_id = os.path.splitext(kdb_id)[0]

    try:
        if force is True or _check(isamAppliance, kdb_id) is False:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_post_files(
                    "Import certificate database",
                    "/isam/ssl_certificates",
                    [
                        {
                            'file_formfield': 'kdb',
                            'filename': kdb,
                            'mimetype': 'application/octet-stream'
                        },
                        {
                            'file_formfield': 'stash',
                            'filename': stash,
                            'mimetype': 'application/octet-stream'
                        }
                    ],
                    {})
    finally:
        if tmpdir != None:
            shutil.rmtree(tmpdir)
    return isamAppliance.create_return_object()


def rename(isamAppliance, cert_id, new_name, check_mode=False, force=False):
    """
    Rename a certificate database
    """
    if force is True or _check(isamAppliance, cert_id) is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put(
                "Renaming a certificate database",
                f"/isam/ssl_certificates/{cert_id}",
                {
                    "new_name": new_name
                })

    return isamAppliance.create_return_object()


def set(isamAppliance, cert_id, description=None, type="kdb", check_mode=False, force=False, **kwargs):
    """
    Set description for a certificate database (type="kdb)"
    Update network certificate database (type="p11")
    """
    warnings = []
    desc_match = True  # This will remain True even when cert db is not found!

    if type == "kdb":
        if not force:
            if description is None:
                desc_match = True
            else:
                ret_obj = get_all(isamAppliance)
                for certdb in ret_obj['data']:
                    if certdb['id'] == cert_id:
                        if certdb['description'] != description:
                            desc_match = False
                        break

        if force or not desc_match:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return isamAppliance.invoke_put(
                    "Set description for a certificate database",
                    f"/isam/ssl_certificates/{cert_id}",
                    {
                        "description": description
                    })
    else:
        # type = p11
        json_data = {}
        for k, v in kwargs.items():
            if k in certificate_database_optional_args:
                json_data[k] = v
            # new in 10.0.5
            if k in certificate_database_new_10_05:
                if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.5.0") < 0:
                    warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.5.0 or higher. Ignoring {k} for this call.")
                else:
                    json_data[k] = v
            # new in 10.0.8
            if k in certificate_database_new_10_08:
                if ibmsecurity.utilities.tools.version_compare(isamAppliance.facts['version'], "10.0.8.0") < 0:
                    warnings.append(f"Appliance at version: {isamAppliance.facts['version']}, {k}: {v} is not supported. Needs 10.0.8.0 or higher. Ignoring {k} for this call.")
                else:
                    json_data[k] = v
        ret_obj = get(isamAppliance, cert_id)
        # Idempotency
        if ret_obj.get("rc", 0) == 404:
            return isamAppliance.create_return_object(warnings=warnings)
        if not json_equals(ret_obj, json_data):
                return isamAppliance.invoke_put(
                    "Updating network certificate database",
                    f"/isam/ssl_certificates/{cert_id}",
                    json_data,
                    warnings=warnings
                )
    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, id):
    """
    Check if certificate database already exists
    """
    ret_obj = get_all(isamAppliance)

    for certdb in ret_obj['data']:
        if certdb['id'] == id:
            return True

    return False


def compare(isamAppliance1, isamAppliance2):
    """
    Compare certificate databases between two appliances
    """
    ret_obj1 = get_all(isamAppliance1)
    ret_obj2 = get_all(isamAppliance2)

    # Version is last modified time of file - not worth comparing
    for cert_db in ret_obj1['data']:
        del cert_db['version']
    for cert_db in ret_obj2['data']:
        del cert_db['version']

    import ibmsecurity.utilities.tools
    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=['version'])
