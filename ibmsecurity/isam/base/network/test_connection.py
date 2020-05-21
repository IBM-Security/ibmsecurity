import logging

logger = logging.getLogger(__name__)

# URI for this module
uri = "/core/net/connect"
requires_modules = None
requires_version = "9.0.3.0"
requires_model = "Appliance"


def connect(isamAppliance, server, port, ssl=True, timeout=60, key=None, showcerts=None, status=None, reconnect=None,
            pause=None, debug=None, msg=None, nbio_test=None, state=None, nbio=None, crlf=None, quiet=None,
            ssl2=None, ssl3=None, tls1_2=None, tls1_1=None, tls1=None, dtls1=None, no_ssl2=None, no_ssl3=None,
            no_tls1_2=None, no_tls1_1=None, no_tls1=None, tlsextdebug=None, check_mode=False, force=False):
    """
    Run Connect Test
    """
    # Create JSON with required fields
    json_data = {
        'server': server,
        'port': port
    }

    # Populate JSON with optional values that are specified
    default_data = {
        'ssl': ssl,
        'timeout': timeout,
        'key': key,
        'showcerts': showcerts,
        'status': status,
        'reconnect': reconnect,
        'pause': pause,
        'debug': debug,
        'msg': msg,
        'nbio_test': nbio_test,
        'state': state,
        'nbio': nbio,
        'crlf': crlf,
        'quiet': quiet,
        'ssl2': ssl2,
        'ssl3': ssl3,
        'tls1_2': tls1_2,
        'tls1_1': tls1_1,
        'tls1': tls1,
        'dtls1': dtls1,
        'no_ssl2': no_ssl2,
        'no_ssl3': no_ssl3,
        'no_tls1_2': no_tls1_2,
        'no_tls1_1': no_tls1_1,
        'no_tls1': no_tls1,
        'tlsextdebug': tlsextdebug
    }

    for k, value in default_data.items():
        if value is not None:
            json_data[k] = value

    ret_obj = isamAppliance.invoke_post("Run Connect Test", uri, json_data, requires_modules=requires_modules,
                                        requires_version=requires_version, requires_model=requires_model,
                                        ignore_error=True)
    # HTTP POST calls get flagged as changes - but test connection changes nothing so override
    if ret_obj['changed'] is True:
        ret_obj['changed'] = False

    return ret_obj
