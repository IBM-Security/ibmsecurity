import json
import requests
import traceback
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from .ibmappliance import IBMAppliance
from .ibmappliance import IBMError
from .ibmappliance import IBMFatal
from ibmsecurity.utilities import tools
from io import open
from os import environ

try:
    basestring
except NameError:
    basestring = (str, bytes)


class ISAMAppliance(IBMAppliance):
    def __init__(self, hostname, user, lmi_port=443, cert=None, verify=None, debug=True):
        self.logger = logging.getLogger(__name__)
        self.debug = debug
        if self.debug: self.logger.debug('Creating an ISAMAppliance')
        if isinstance(lmi_port, str):
            self.lmi_port = int(lmi_port)
        else:
            self.lmi_port = lmi_port
        self.hostname = hostname
        self.session = requests.session()

        # If we did not get a value for verify, try the environment variable
        if verify is None:
            verify = str(environ.get("IBMSECLIB_VERIFY_CONNECTION", False)).lower() in ["true", "yes"]

        self.cert = cert

        self.disable_urllib_warnings = False
        if self.cert is None:
            self.logger.debug('Cert object is None, using BA Auth with userid/password.')
            self.session.auth = (user.username, user.password)
        else:
            self.logger.debug('Using cert based auth, since cert object is not None.')
            self.session.cert = self.cert

        self._set_ssl_verification(requests_verify_param=verify)

        IBMAppliance.__init__(self, hostname, user)

    def _set_ssl_verification(self, requests_verify_param):
        self.verify = requests_verify_param
        self.session.verify = self.verify
        if self.verify is None or self.verify is False:
            self.disable_urllib_warnings = True
            self.logger.warning("""
Certificate verification has been disabled. Python is NOT verifying the SSL
certificate of the host appliance and InsecureRequestWarning messages are
being suppressed for the following host:
  https://{0}:{1}

To use certificate verification:
  1. When the certificate is trusted by your Python environment:
        Instantiate all instances of ISAMAppliance with verify=True or set
        the environment variable IBMSECLIB_VERIFY_CONNECTION=True.
  2. When the certificate is not already trusted in your Python environment:
        Instantiate all instances of ISAMAppliance with the verify parameter
        set to the fully qualified path to a CA bundle.

See the following URL for more details:
  https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
""".format(self.hostname, self.lmi_port))

    def _url(self, uri):
        # Build up the URL
        url = "https://" + self.hostname + ":" + str(self.lmi_port) + uri
        if self.debug: self.logger.debug("Issuing request to: " + url)

        return url

    def _log_desc(self, description):
        if description != "":
            self.logger.info('*** ' + description + ' ***')

    def _suppress_ssl_warning(self):
        # If we have trust setup correctly, we do not want to suppress these warnings.
        if not self.disable_urllib_warnings:
            return

        # Disable https warning because of non-standard certs on appliance
        try:
            if self.debug: self.logger.debug("Suppressing SSL Warnings.")
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        except AttributeError:
            self.logger.warning("load requests.packages.urllib3.disable_warnings() failed")

    def _process_response(self, return_obj, http_response, ignore_error):

        # return_obj['rsp'] = http_response # Do not add this - breaks the ISAM Collection's connection
        return_obj['rc'] = http_response.status_code

        # Examine the response.
        if (http_response.status_code == 403):
            self.logger.error("  Request failed: ")
            self.logger.error("     status code: {0}".format(http_response.status_code))
            if http_response.text != "":
                self.logger.error("     text: " + http_response.text)
            # Unconditionally raise exception to abort execution
            raise IBMFatal("HTTP Return code: {0}".format(http_response.status_code), http_response.text)
        elif (
                http_response.status_code != 200 and http_response.status_code != 204 and http_response.status_code != 201):
            self.logger.error("  Request failed: ")
            self.logger.error("     status code: {0}".format(http_response.status_code))
            if http_response.text != "":
                self.logger.error("     text: " + http_response.text)
            if not ignore_error:
                raise IBMError("HTTP Return code: {0}".format(http_response.status_code), http_response.text)
            return_obj['changed'] = False  # force changed to be False as there is an error
        else:
            return_obj['rc'] = 0

        # Handle if there was json on input but response was not in json format
        try:
            json_data = json.loads(http_response.text)
            return_obj['data'] = json_data
        except ValueError:
            return_obj['data'] = http_response.content
            return

        if self.debug: self.logger.debug("Status Code: {0}".format(http_response.status_code))
        if http_response.text != "":
            if self.debug: self.logger.debug("Text: " + http_response.content.decode("utf-8"))

        for key in http_response.headers:
            if key == 'g-type':
                if http_response.headers[key] == 'application/octet-stream; charset=UTF-8':
                    json_data = {}
                    return_obj.data = http_response.content
                    return

        if http_response.text == "":
            json_data = {}
        else:
            json_data = json.loads(http_response.text)

        return_obj['data'] = json_data
        try:
            json_data = json.loads(http_response.content.decode("utf-8"))
            return_obj['data'] = json_data
        except UnicodeDecodeError:
            return_obj['data'] = http_response.content
        except ValueError:
            if isinstance(http_response.content, bytes):
                return_obj['data'] = http_response.content.decode("utf-8")
            else:
                return_obj['data'] = http_response.content

    def _process_connection_error(self, ignore_error, return_obj, error_message=""):
        if not ignore_error:
            self.logger.critical(f"Failed to connect to server: {error_message}")
            raise IBMError("HTTP Return code: 502", f"Failed to connect to server : {error_message}")
        else:
            self.logger.debug(f"Failed to connect to server: {error_message}")
            return_obj['rc'] = 502

    def _process_warnings(self, uri, requires_modules, requires_version, requires_model, warnings=[]):
        # flag to indicate if processing needs to return and not continue
        return_call = False
        if self.debug: self.logger.debug("Checking for minimum version: {0}.".format(requires_version))

        self.logger.debug("Checking for deployment model {0}.".format(requires_model))
        if requires_model is not None and 'model' in self.facts and self.facts['model'] is not None:
            if self.facts['model'] != requires_model:
                return_call = True
                warnings.append(
                    "API invoked requires model: {0}, appliance is of deployment model: {1}.".format(
                        requires_model, self.facts['model']))

        self.logger.debug("Checking for minimum version: {0}.".format(requires_version))

        if requires_version is not None and 'version' in self.facts and self.facts['version'] is not None:
            if tools.version_compare(self.facts['version'], requires_version) < 0:
                return_call = True
                warnings.append(
                    "API invoked requires minimum version: {0}, appliance is of lower version: {1}.".format(
                        requires_version, self.facts['version']))
        # Detecting modules from uri if none is provided
        if requires_modules is None and not requires_modules:
            if uri.startswith("/wga"):
                requires_modules = ['wga']
                if self.debug: self.logger.debug("Detected module: {0} from uri: {1}.".format(requires_modules, uri))
            elif uri.startswith("/mga"):
                requires_modules = ['mga']
                if self.debug: self.logger.debug("Detected module: {0} from uri: {1}.".format(requires_modules, uri))

        if self.debug: self.logger.debug("Checking for one of required modules: {0}.".format(requires_modules))
        if requires_modules is not None and requires_modules:
            if 'activations' in self.facts and self.facts['activations']:
                # Find intersection of the two lists
                iactive = [ia for ia in self.facts['activations'] if ia in requires_modules]
                if not iactive:
                    return_call = True
                    warnings.append(
                        "API invoked requires one of modules: {0}, appliance has these modules active: {1}.".format(
                            requires_modules, self.facts['activations']))
                else:
                    self.logger.info("Modules satisfying requirement: {0}".format(iactive))
            else:
                return_call = True
                warnings.append("API invoked requires module: {0}, appliance has no modules active.".format(
                    requires_modules))

        if self.debug: self.logger.debug("Warnings: {0}".format(warnings))
        return warnings, return_call

    def invoke_post_files(self, description, uri, fileinfo, data, ignore_error=False, requires_modules=None,
                          requires_version=None, warnings=[], json_response=True, data_as_files=False,
                          requires_model=None):
        """
        Send multipart/form-data upload file request to the appliance.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version,
                                                       warnings=warnings, requires_model=requires_model)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # Build up the URL and header information.
        if json_response:
            headers = {
                'Accept': 'application/json,text/html,application/xhtml+xml,application/xml'
            }
        else:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml'
            }
        if self.debug: self.logger.debug("Headers are: {0}".format(headers))

        if data_as_files is False:
            files = list()
            for file2post in fileinfo:
                files.append((file2post['file_formfield'],
                              (tools.path_leaf(file2post['filename']), open(file2post['filename'], 'rb'),
                               file2post['mimetype'])))
        else:
            files = data

        self._suppress_ssl_warning()

        try:
            if data_as_files is False:
                r = self.session.post(url=self._url(uri=uri), data=data, files=files, headers=headers)
            else:
                r = self.session.post(url=self._url(uri=uri), files=files, headers=headers)
            return_obj['changed'] = True  # POST of file would be a change
            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError as e:
            if not ignore_error:
                self.logger.critical(f"Failed to connect to server: {str(e)}")
                raise IBMError("HTTP Return code: 502", f"Failed to connect to server: {str(e)}")
            else:
                if self.debug: self.logger.debug(f"Failed to connect to server : {str(e)}")
                return_obj.rc = 502

        return return_obj

    def invoke_put_files(self, description, uri, fileinfo, data, ignore_error=False, requires_modules=None,
                         requires_version=None, warnings=[], requires_model=None):
        """
        Send multipart/form-data upload file request to the appliance.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version, requires_model=requires_model,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # Build up the URL and header information.
        headers = {
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml'
        }
        if self.debug: self.logger.debug("Headers are: {0}".format(headers))

        files = list()

        for file2post in fileinfo:
            files.append((file2post['file_formfield'],
                          (file2post['filename'], open(file2post['filename'], 'rb'), file2post['mimetype'])))

        self._suppress_ssl_warning()

        try:
            r = self.session.put(url=self._url(uri=uri), data=data, files=files, headers=headers)
            return_obj['changed'] = True  # POST of file would be a change
            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError as e:
            if not ignore_error:
                self.logger.critical(f"Failed to connect to server. {str(e)}")
                raise IBMError("HTTP Return code: 502", f"Failed to connect to server : {str(e)}")
            else:
                if self.debug: self.logger.debug(f"Failed to connect to server: {str(e)}")
                return_obj.rc = 502

        return return_obj

    def invoke_get_file(self, description, uri, filename, no_headers=False, ignore_error=False, requires_modules=None,
                        requires_version=None, warnings=[], requires_model=None):
        """
        Invoke a GET request and download the response data to a file
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version, requires_model=requires_model,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # In some cases passing a header causes response to come back as JSON
        if no_headers is True:
            headers = {}
        else:
            headers = {
                'Accept': 'application/json,application/octet-stream'
            }
            if self.debug: self.logger.debug("Headers are: {0}".format(headers))

        self._suppress_ssl_warning()

        try:
            r = self.session.get(url=self._url(uri=uri), stream=True, headers=headers)

            if (r.status_code != 200 and r.status_code != 204 and r.status_code != 201):
                self.logger.error("  Request failed: ")
                self.logger.error("     status code: {0}".format(r.status_code))
                if r.text != "":
                    self.logger.error("     text: " + r.text)
                if not ignore_error:
                    raise IBMError("HTTP Return code: {0}".format(r.status_code), r.text)
                else:
                    return_obj['rc'] = r.status_code
                    return_obj['data'] = {'msg': 'Unable to extract contents to file!'}
            else:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                return_obj['rc'] = 0
                return_obj['data'] = {'msg': 'Contents extracted to file: ' + filename}

        except requests.exceptions.ConnectionError as e:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj, error_message=str(e))

        except IOError:
            if not ignore_error:
                self.logger.critical("Failed to write to file: " + filename)
                raise IBMError("HTTP Return code: 999", "Failed to write to file: " + filename)
            else:
                if self.debug: self.logger.debug("Failed to write to file: " + filename)
                return_obj['rc'] = 999

        return return_obj

    def _invoke_request(self, func, description, uri, ignore_error, data={}, requires_modules=None,
                        requires_version=None, warnings=[], requires_model=None):
        """
        Send a request to the LMI.  This function is private and should not be
        used directly.  The invoke_get/invoke_put/etc functions should be used instead.
        """
        self._log_desc(description=description)
        self.session.cookies.pop('LtpaToken2', None)
        self.session.cookies.pop('JSESSIONID', None)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version, requires_model=requires_model,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # There maybe some cases when header should be blank (not json)
        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
        if self.debug: self.logger.debug("Headers are: {0}".format(headers))

        # Process the input data into JSON
        json_data = json.dumps(data)

        if self.debug: self.logger.debug("Input Data: " + json_data)

        self._suppress_ssl_warning()

        try:
            if func == self.session.get or func == self.session.delete:
                if data != {}:
                    r = func(url=self._url(uri), data=json_data, headers=headers, verify=self.verify)
                else:
                    r = func(url=self._url(uri), headers=headers, verify=self.verify)
            else:
                r = func(url=self._url(uri), data=json_data,
                         headers=headers, verify=self.verify, cert=self.cert)

            if func != self.session.get:
                return_obj['changed'] = True  # Anything but GET should result in change

            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError as e:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj, error_message=str(e))

        return return_obj

    def _invoke_request_with_headers(self, func, description, uri, ignore_error, headers, data={},
                                     requires_modules=None, requires_version=None, warnings=[], requires_model=None):
        """
        Send a request to the LMI.  This function is private and should not be
        used directly.  The invoke_get/invoke_put/etc functions should be used instead.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version, requires_model=requires_model,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        self.logger.debug("Headers are: {0}".format(headers))

        # Process the input data into JSON
        json_data = json.dumps(data)

        self.logger.debug("Input Data: " + json_data)

        self._suppress_ssl_warning()

        try:
            if func == self.session.get or func == self.session.delete:

                if data != {}:
                    r = func(url=self._url(uri), data=json_data, headers=headers)
                else:
                    r = func(url=self._url(uri), headers=headers)
            else:
                r = func(url=self._url(uri), data=json_data,
                         headers=headers, verify=self.verify, cert=self.cert)

            if func != self.session.get:
                return_obj['changed'] = True  # Anything but GET should result in change

            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError as e:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj, error_message=str(e))

        return return_obj

    def invoke_put(self, description, uri, data, ignore_error=False, requires_modules=None, requires_version=None,
                   warnings=[], requires_model=None):
        """
        Send a PUT request to the LMI.
        """

        self._log_request("PUT", uri, description)
        response = self._invoke_request(self.session.put, description, uri,
                                        ignore_error, data,
                                        requires_modules=requires_modules, requires_version=requires_version,
                                        requires_model=requires_model, warnings=warnings)
        return response

    def invoke_post(self, description, uri, data, ignore_error=False, requires_modules=None, requires_version=None,
                    warnings=[], requires_model=None):
        """
        Send a POST request to the LMI.
        """

        self._log_request("POST", uri, description)
        response = self._invoke_request(self.session.post, description, uri,
                                        ignore_error, data,
                                        requires_modules=requires_modules, requires_version=requires_version,
                                        requires_model=requires_model,
                                        warnings=warnings)
        return response

    def invoke_post_snapshot_id(self, description, uri, data, ignore_error=False, requires_modules=None,
                                requires_version=None, warnings=[], requires_model=None):
        """
        Send a POST request to the LMI.  Snapshot id is part of the uri.
        Requires different headers to normal post.
        """

        self._log_request("POST", uri, description)
        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version, requires_model=requires_model,
                                                       warnings=warnings)

        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if self.debug: self.logger.debug("Headers are: {0}".format(headers))

        self._suppress_ssl_warning()

        try:
            r = self.session.post(url=self._url(uri=uri), data=data, headers=headers)
            return_obj['changed'] = False  # POST of snapshot id would not be a change
            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError as e:
            if not ignore_error:
                self.logger.critical(f"Failed to connect to server: {str(e)}")
                raise IBMError("HTTP Return code: 502", f"Failed to connect to server : {str(e)}")
            else:
                self.logger.debug(f"Failed to connect to server : {str(e)}")
                return_obj.rc = 502

        return return_obj

    def invoke_get(self, description, uri, ignore_error=False, requires_modules=None, requires_version=None,
                   warnings=[], requires_model=None):
        """
        Send a GET request to the LMI.
        """
        self._log_request("GET", uri, description)

        response = self._invoke_request(self.session.get, description, uri,
                                        ignore_error, requires_modules=requires_modules,
                                        requires_version=requires_version, requires_model=requires_model,
                                        warnings=warnings)
        self._log_response(response)
        return response

    def invoke_get_with_headers(self, description, uri, headers, ignore_error=False, requires_modules=None,
                                requires_version=None,
                                warnings=[], requires_model=None):
        """
        Send a GET request to the LMI with passed in headers.
        """
        self._log_request("GET", uri, description)

        response = self._invoke_request_with_headers(self.session.get, description, uri,
                                                     ignore_error, headers=headers, requires_modules=requires_modules,
                                                     requires_version=requires_version, requires_model=requires_model,
                                                     warnings=warnings)
        self._log_response(response)
        return response

    def invoke_delete(self, description, uri, data={}, ignore_error=False, requires_modules=None, requires_version=None,
                      warnings=[], requires_model=None):
        """
        Send a DELETE request to the LMI.
        """
        self._log_request("DELETE", uri, description)
        if data != {}:
            self.logger.info("Input Data:{0}".format(data))
            response = self._invoke_request(self.session.delete, description, uri, ignore_error, data=data,
                                            requires_modules=requires_modules, requires_version=requires_version,
                                            requires_model=requires_model,
                                            warnings=warnings)
        else:
            response = self._invoke_request(self.session.delete, description, uri, ignore_error,
                                            requires_modules=requires_modules, requires_version=requires_version,
                                            requires_model=requires_model,
                                            warnings=warnings)
        self._log_response(response)
        return response

    def invoke_request(self, description, method, uri, filename=None, ignore_error=False, requires_modules=None,
                       requires_version=None,
                       warnings=[], requires_model=None, **kwargs):
        """
        parse and send a appropriate request to the appliance.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version, requires_model=requires_model,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        args = {}

        for key, value in kwargs.items():
            if key == 'json' and value != {}:
                json_data = json.dumps(value)
                if self.debug: self.logger.debug("Input json Data: " + json_data)
                args['json'] = json_data
            elif key == 'data':
                try:
                    json.loads(value)
                    if self.debug: self.logger.debug("Input Data: " + value)
                    args['data'] = value
                except ValueError:
                    if self.debug: self.logger.debug("Input Data: " + value)
                    args['data'] = value
            else:
                args[key] = value

        self._suppress_ssl_warning()

        try:
            streaminargs = False
            r = self.session.request(method, url=self._url(uri), **args)
            # check for stream=True
            if "stream" in args and args["stream"] == True:
                streaminargs = True
                if filename == None:
                    return_obj['warnings'] = return_obj['warnings'].append(
                        "filename is missing, for stream=True, filename needs to be non null")
                    return return_obj
                # else stream content to file
                else:
                    if (r.status_code != 200 and r.status_code != 204 and r.status_code != 201):
                        self.logger.error("  Request failed: ")
                        self.logger.error("     status code: {0}".format(r.status_code))
                        if r.text != "":
                            self.logger.error("     text: " + r.text)
                        if not ignore_error:
                            raise IBMError("HTTP Return code: {0}".format(r.status_code), r.text)
                        else:
                            return_obj['rc'] = r.status_code
                            return_obj['data'] = {'msg': 'Unable to extract contents to file!'}
                    else:
                        with open(filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:  # filter out keep-alive new chunks
                                    f.write(chunk)
                        return_obj['rc'] = 0
                        return_obj['data'] = {'msg': 'Contents extracted to file: ' + filename}

            if method == "get" or (method == "post" and streaminargs == True):
                return_obj['changed'] = False
            else:
                return_obj['changed'] = True  # Anything but GET or a POST with stream=True set should result in change

            if streaminargs == False:
                self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError as e:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj, error_message=str(e))

        return return_obj

    def get_facts(self):
        """
        Get facts about the appliance
        """
        # Fact collection will abort on any exception
        try:
            self.get_version()

            # Check if appliance is setup before collecting Activation information
            import ibmsecurity.isam.base.setup_complete
            ret_obj = ibmsecurity.isam.base.setup_complete.get(self)
            if ret_obj['data'].get('configured') is True:
                self.get_activations()
        # Be sure to let fatal error unconditionally percolate up the stack
        except IBMFatal:
            raise

        # Exceptions like those connection related will be ignored
        except Exception as e:
            self.logger.error( traceback.print_exc() )
            pass

    def get_version(self):
        """
        Get appliance version (versions API or active partition)

        When firmware are installed or partition are changed, then this value is updated
        """
        self.facts['version'] = None
        import ibmsecurity.isam.base.version
        import ibmsecurity.isam.base.firmware

        try:
            ret_obj = ibmsecurity.isam.base.version.get(self)
            self.facts['version'] = ret_obj['data']['firmware_version']

            if tools.version_compare(self.facts['version'], '9.0.3.0') > 0:
                if 'deployment_model' in ret_obj['data']:
                    self.facts['model'] = ret_obj['data']['deployment_model']

                if 'product_name' in ret_obj['data']:
                    self.facts['product_name'] = ret_obj['data']['product_name']

                if 'product_description' in ret_obj['data']:
                    self.facts['product_description'] = ret_obj['data']['product_description']

                if 'firmware_build' in ret_obj['data']:
                    self.facts['firmware_build'] = ret_obj['data']['firmware_build']

                if 'firmware_label' in ret_obj['data']:
                    self.facts['firmware_label'] = ret_obj['data']['firmware_label']

        # Be sure to let fatal error unconditionally percolate up the stack
        except IBMFatal:
            raise
        except IBMError:
            self.logger.error( traceback.print_exc() )
            try:
                ret_obj = ibmsecurity.isam.base.firmware.get(self)
                for partition in ret_obj['data']:
                    if partition['active'] is True:
                        ver = partition['firmware_version'].split(' ')
                        self.facts['version'] = ver[-1]
                self.facts['model'] = "Appliance"
            except:
                self.logger.error( traceback.print_exc() )
                pass
        return

    def get_activations(self):
        """
        Get  appliance activations

        When new modules are activated or old ones de-activated this value is updated.
        """
        self.facts['activations'] = []
        import ibmsecurity.isam.base.activation

        ret_obj = ibmsecurity.isam.base.activation.get_all(self)
        for activation in ret_obj['data']:
            if activation['enabled'] == 'True':
                self.facts['activations'].append(activation['id'])

    def _log_request(self, method, url, desc):
        self.logger.debug("Request: %s %s desc=%s", method, url, desc)

    def _log_response(self, response):
        if response:
            self.logger.debug("Response: %d", response.get('rc'))
            # self.logger.debug("Response: %i %i warnings:%s",
            #                     response.get('rc'),
            #                     response.get('status_code'),
            #                     response.get('warnings'))
        else:
            self.logger.debug("Response: None")
