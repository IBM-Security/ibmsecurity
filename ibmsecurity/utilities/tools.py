import random
import string
import logging
import pprint
import difflib
import hashlib
import ntpath
import re
from io import open
import zipfile

logger = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = (str, bytes)


def json_sort(json_data):
    if isinstance(json_data, dict):
        return sorted((key, json_sort(value)) for key, value in json_data.items())

    if isinstance(json_data, list):
        return sorted(json_sort(x) for x in json_data)
    else:
        return json_data


def json_replace_value(json_data, from_value, to_value):
    '''
    Replaces all found from_values with to_value in a json - from_value can be a JSON itself

    :param json_data:
    :param from_value:
    :param to_value:
    :return:
    '''
    if json_data == from_value:
        return to_value
    elif isinstance(json_data, dict):
        new_dict = {}
        for key, value in json_data.items():
            if type(value) == type(from_value) and value == from_value:
                value = to_value
            elif isinstance(value, dict):
                value = json_replace_value(value, from_value, to_value)
            elif isinstance(value, list):
                value = json_replace_value(value, from_value, to_value)
            new_dict[key] = value
        return new_dict
    elif isinstance(json_data, list):
        new_list = []
        for elem in json_data:
            if type(elem) == type(from_value) and elem == from_value:
                elem = to_value
            elif isinstance(elem, dict):
                elem = json_replace_value(elem, from_value, to_value)
            elif isinstance(elem, list):
                elem = json_replace_value(elem, from_value, to_value)
            new_list.append(elem)
        return new_list
    else:
        return json_data


def json_remove_value(json_data, value):
    '''
    Removes all found values (along with key if part of a dict)

    :param json_data:
    :param from_value:
    :param to_value:
    :return:
    '''
    if isinstance(json_data, dict):
        new_dict = {}
        for k, v in json_data.items():
            if isinstance(v, dict) or isinstance(v, list):
                v = json_remove_value(v, value)
                new_dict[k] = v
            elif type(v) == type(value) and v == value:
                pass
            else:
                new_dict[k] = v
        return new_dict
    elif isinstance(json_data, list):
        new_list = []
        for elem in json_data:
            if isinstance(elem, dict) or isinstance(elem, list):
                elem = json_remove_value(elem, value)
                new_list.append(elem)
            elif type(elem) == type(value) and elem == value:
                pass
            else:
                new_list.append(elem)
        return new_list
    else:
        if type(json_data) == type(value) and json_data == value:
            return None
        else:
            return json_data


def random_password(length=12, allow_special=True):
    myrg = random.SystemRandom()

    # If you want non-English characters, remove the [0:52]
    alphabet = string.ascii_letters[0:52] + string.digits
    if allow_special is True:
        alphabet = alphabet + "!@#$%^&*()"

    pw = str().join(myrg.choice(alphabet) for _ in range(length))

    return pw


def json_compare(ret_obj1, ret_obj2, deleted_keys=[]):
    ret_obj = {'rc': 0, 'data': {'matches': False, 'difference': '', 'deleted_keys': deleted_keys},
               'changed': False, 'warnings': []}

    # Pick the highest RC to return (should not matter either way)
    if ret_obj1['rc'] > ret_obj2['rc']:
        ret_obj['rc'] = ret_obj1['rc']
    else:
        ret_obj['rc'] = ret_obj2['rc']

    if 'warnings' in ret_obj1 and ret_obj1['warnings']:
        ret_obj['warnings'].append(ret_obj1['warnings'])
    if 'warnings' in ret_obj2 and ret_obj2['warnings']:
        ret_obj['warnings'].append(ret_obj2['warnings'])

    sorted_json1 = json_sort(ret_obj1['data'])
    sorted_json2 = json_sort(ret_obj2['data'])

    if sorted_json1 == sorted_json2:
        ret_obj['data']['matches'] = True
    else:
        psj1 = pprint.pformat(sorted_json1)
        logger.debug('Sorted JSON1 to Compare: \n' + psj1)
        psj2 = pprint.pformat(sorted_json2)
        logger.debug('Sorted JSON2 to Compare: \n' + psj2)
        diff = difflib.ndiff(psj1.split('\n'), psj2.split('\n'))
        ret_obj['data']['difference'] = '\n'.join(diff)

    return ret_obj


def create_query_string(**kwargs):
    # Create a query string - using variable key value pairs
    query_str = ''
    for key in kwargs:
        if kwargs[key] is not None:
            if query_str == '':
                query_str = '?'
            else:
                query_str += '&'
            query_str += "{0}={1}".format(key, kwargs[key])

    logger.debug("Query Parameter to be used: {0}".format(query_str))

    return query_str


def files_same(original_file, new_file):
    """
    Compare two files
        -works with text, image, and zip files
    Returns Boolean
    """
    with open(original_file, 'rb') as f:
        original_file_contents = f.read()
    with open(new_file, 'rb') as f:
        new_file_contents = f.read()
    hash_original_file = hashlib.sha224(original_file_contents).hexdigest()
    hash_new_file = hashlib.sha224(new_file_contents).hexdigest()
    if hash_original_file == hash_new_file:
        return True
    else:
        return False

def files_same_zip_content(original_file, new_file):
    identical = True
    logger.debug("Comparing original_file[{}] vs new_file[{}]".format(original_file, new_file))
    z1 = zipfile.ZipFile(original_file)
    z2 = zipfile.ZipFile(new_file)
    
    if len(z1.infolist()) != len(z2.infolist()):
        logger.debug("number of archive elements differ: {} in {} vs {} from server".format(len(z1.infolist()), z1.filename, len(z2.infolist())))
        identical = False
        # Can stop comparison of zip files for perfomance
        return identical
    for zipentry in z1.infolist():
        if zipentry.filename not in z2.namelist():
            logger.debug("no file named {} found in {}".format(zipentry.filename, z2.filename))
            identical = False
        else:
            with z1.open(zipentry.filename) as f:
                original_file_contents = f.read()
            with z2.open(zipentry.filename) as f:
                new_file_contents = f.read()
            hash_original_file = hashlib.sha224(original_file_contents).hexdigest()
            hash_new_file = hashlib.sha224(new_file_contents).hexdigest()
            if hash_original_file != hash_new_file:
                identical = False
                logger.debug("content for zip file {} differs.".format(zipentry.filename))

    if identical:
        logger.info("content for zip files {} and {} are the same.".format(original_file,new_file))
    else:
        logger.info("content for zip files {} and {} are different.".format(original_file,new_file))

    return identical

def get_random_temp_dir():
    """
    Create a temporary directory
    """
    import os
    import tempfile
    tmpdir = tempfile.gettempdir()
    random_str = random_password(10, allow_special=False)
    tmpdir += '/%s' % random_str
    os.mkdir(tmpdir)
    return tmpdir


def strings(filename, min=4):
    """
    Emulate UNIX "strings" command on a file
    """
    with open(filename, 'r', errors='ignore') as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def version_compare(version1, version2):
    """
    Compare two ISAM version strings. Please note that the versions should be all numeric separated by dots.

    Returns following values:
         0 - if version strings are equivalent
        >0 - if version1 is greater than version2
        <0 - if version1 is less than version2

    Test cases to run for verifying this code:
        assert version_compare("1", "1") == 0
        assert version_compare("2.1", "2.2") < 0
        assert version_compare("3.0.4.10", "3.0.4.2") > 0
        assert version_compare("4.08", "4.08.01") < 0
        assert version_compare("3.2.1.9.8144", "3.2") > 0
        assert version_compare("3.2", "3.2.1.9.8144") < 0
        assert version_compare("1.2", "2.1") < 0
        assert version_compare("2.1", "1.2") > 0
        assert version_compare("5.6.7", "5.6.7") == 0
        assert version_compare("1.01.1", "1.1.1") == 0
        assert version_compare("1.1.1", "1.01.1") == 0
        assert version_compare("1", "1.0") == 0
        assert version_compare("1.0", "1") == 0
        assert version_compare("1.0", "1.0.1") < 0
        assert version_compare("1.0.1", "1.0") > 0
        assert version_compare("1.0.2.0", "1.0.2") == 0
        assert version_compare("10.0", "9.0.3") > 0

    :param version1:
    :param version2:
    :return:
    """

    def normalize(v):
        v = re.sub(r'_b\d+$', '', v)
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    if normalize(version1) == normalize(version2):
        return 0
    elif normalize(version1) > normalize(version2):
        return 1
    elif normalize(version1) < normalize(version2):
        return -1
