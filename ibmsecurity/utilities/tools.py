import random
import string
import logging
import pprint
import difflib
import hashlib
import ntpath

logger = logging.getLogger(__name__)


def json_sort(json_data):
    if isinstance(json_data, dict):
        return sorted((key, json_sort(value)) for key, value in json_data.items())

    if isinstance(json_data, list):
        return sorted(json_sort(x) for x in json_data)
    else:
        return json_data


def random_password(length=12, allow_special=True):
    myrg = random.SystemRandom()

    # If you want non-English characters, remove the [0:52]
    alphabet = string.letters[0:52] + string.digits
    if allow_special is True:
        alphabet = alphabet + "!@#$%^&*()"

    pw = str().join(myrg.choice(alphabet) for _ in xrange(length))

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
    with open(original_file, 'r') as f:
        original_file_contents = f.read()
    with open(new_file, 'r') as f:
        new_file_contents = f.read()
    hash_original_file = hashlib.sha224(original_file_contents).hexdigest()
    hash_new_file = hashlib.sha224(new_file_contents).hexdigest()
    if hash_original_file == hash_new_file:
        return True
    else:
        return False


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
    with open(filename, "rb") as f:
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
