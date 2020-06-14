import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from .ibmappliance import IBMAppliance
from .ibmappliance import IBMError
from ibmsecurity.utilities import tools
from io import open

try:
    basestring
except NameError:

    basestring = (str, bytes)


class ISDSAppliance(IBMAppliance):
    def __init__(self, hostname, user, lmi_port=443):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating an ISDSAppliance')
        if isinstance(lmi_port, str):
            self.lmi_port = int(lmi_port)
        else:
            self.lmi_port = lmi_port

        IBMAppliance.__init__(self, hostname, user)

    def _url(self, uri):
        # Build up the URL
        url = "https://" + self.hostname + ":" + str(self.lmi_port) + uri
        self.logger.debug("Issuing request to: " + url)

        return url

    def _log_desc(self, description):
        if description != "":
            self.logger.info('*** ' + description + ' ***')

    def _suppress_ssl_warning(self):
        # Disable https warning because of non-standard certs on appliance
        try:
            self.logger.debug("Suppressing SSL Warnings.")
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        except AttributeError:
            self.logger.warning("load requests.packages.urllib3.disable_warnings() failed")

    def _process_response(self, return_obj, http_response, ignore_error):

        return_obj['rc'] = http_response.status_code

        # Examine the response.
        if (http_response.status_code != 200 and http_response.status_code != 204 and http_response.status_code != 201):
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
        except ValueError:
            return_obj['data'] = http_response.content
            return

        self.logger.debug("Status Code: {0}".format(http_response.status_code))
        if http_response.text != "":
            self.logger.debug("Text: " + http_response.content.decode("utf-8"))

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

    def _process_connection_error(self, ignore_error, return_obj):
        if not ignore_error:
            self.logger.critical("Failed to connect to server.")
            raise IBMError("HTTP Return code: 502", "Failed to connect to server")
        else:
            self.logger.debug("Failed to connect to server.")
            return_obj['rc'] = 502

    def _process_warnings(self, uri, requires_modules, requires_version, warnings=[]):
        # flag to indicate if processing needs to return and not continue
        return_call = False
        self.logger.debug("Checking for minimum version: {0}.".format(requires_version))
        if requires_version is not None and 'version' in self.facts and self.facts['version'] is not None:
            if self.facts['version'] < requires_version:
                return_call = True
                warnings.append(
                    "API invoked requires minimum version: {0}, appliance is of lower version: {1}.".format(
                        requires_version, self.facts['version']))
        # Detecting modules from uri if none is provided
        if requires_modules is None and not requires_modules:
            if uri.startswith("/wga"):
                requires_modules = ['wga']
                self.logger.debug("Detected module: {0} from uri: {1}.".format(requires_modules, uri))
            elif uri.startswith("/mga"):
                requires_modules = ['mga']
                self.logger.debug("Detected module: {0} from uri: {1}.".format(requires_modules, uri))

        self.logger.debug("Checking for one of required modules: {0}.".format(requires_modules))
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

        self.logger.debug("Warnings: {0}".format(warnings))
        return warnings, return_call

    def invoke_post_files(self, description, uri, fileinfo, data, ignore_error=False, requires_modules=None,
                          requires_version=None, warnings=[], json_response=True):
        """
        Send multipart/form-data upload file request to the appliance.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version,
                                                       warnings=warnings)
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
        self.logger.debug("Headers are: {0}".format(headers))

        files = list()
        for file2post in fileinfo:
            files.append((file2post['file_formfield'],
                          (tools.path_leaf(file2post['filename']), open(file2post['filename'], 'rb'),
                           file2post['mimetype'])))

        self._suppress_ssl_warning()

        try:
            r = requests.post(url=self._url(uri=uri), data=data, auth=(self.user.username, self.user.password),
                              files=files, verify=False, headers=headers)
            return_obj['changed'] = True  # POST of file would be a change
            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError:
            if not ignore_error:
                self.logger.critical("Failed to connect to server.")
                raise IBMError("HTTP Return code: 502", "Failed to connect to server")
            else:
                self.logger.debug("Failed to connect to server.")
                return_obj.rc = 502

        return return_obj

    def invoke_put_files(self, description, uri, fileinfo, data, ignore_error=False, requires_modules=None,
                         requires_version=None, warnings=[]):
        """
        Send multipart/form-data upload file request to the appliance.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # Build up the URL and header information.
        headers = {
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml'
        }
        self.logger.debug("Headers are: {0}".format(headers))

        files = list()

        for file2post in fileinfo:
            files.append((file2post['file_formfield'],
                          (file2post['filename'], open(file2post['filename'], 'rb'), file2post['mimetype'])))

        self._suppress_ssl_warning()

        try:
            r = requests.put(url=self._url(uri=uri), data=data, auth=(self.user.username, self.user.password),
                             files=files, verify=False, headers=headers)
            return_obj['changed'] = True  # POST of file would be a change
            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError:
            if not ignore_error:
                self.logger.critical("Failed to connect to server.")
                raise IBMError("HTTP Return code: 502", "Failed to connect to server")
            else:
                self.logger.debug("Failed to connect to server.")
                return_obj.rc = 502

        return return_obj

    def invoke_get_file(self, description, uri, filename, no_headers=False, ignore_error=False, requires_modules=None,
                        requires_version=None, warnings=[]):
        """
        Invoke a GET request and download the response data to a file
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version,
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
        self.logger.debug("Headers are: {0}".format(headers))

        self._suppress_ssl_warning()

        try:
            r = requests.get(url=self._url(uri=uri), auth=(self.user.username, self.user.password), verify=False,
                             stream=True, headers=headers)

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

        except requests.exceptions.ConnectionError:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj)

        except IOError:
            if not ignore_error:
                self.logger.critical("Failed to write to file: " + filename)
                raise IBMError("HTTP Return code: 999", "Failed to write to file: " + filename)
            else:
                self.logger.debug("Failed to write to file: " + filename)
                return_obj['rc'] = 999

        return return_obj

    def _invoke_request(self, func, description, uri, ignore_error, data={}, requires_modules=None,
                        requires_version=None, warnings=[]):
        """
        Send a request to the LMI.  This function is private and should not be
        used directly.  The invoke_get/invoke_put/etc functions should be used instead.
        """
        self._log_desc(description=description)

        warnings, return_call = self._process_warnings(uri=uri, requires_modules=requires_modules,
                                                       requires_version=requires_version,
                                                       warnings=warnings)
        return_obj = self.create_return_object(warnings=warnings)
        if return_call:
            return return_obj

        # There maybe some cases when header should be blank (not json)
        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
        self.logger.debug("Headers are: {0}".format(headers))

        # Process the input data into JSON
        json_data = json.dumps(data)

        self.logger.debug("Input Data: " + json_data)

        self._suppress_ssl_warning()

        try:
            if func == requests.get or func == requests.delete:

                if data != {}:
                    r = func(url=self._url(uri), data=json_data, auth=(self.user.username, self.user.password),
                             verify=False, headers=headers)
                else:
                    r = func(url=self._url(uri), auth=(self.user.username, self.user.password),
                             verify=False, headers=headers)
            else:
                r = func(url=self._url(uri), data=json_data,
                         auth=(self.user.username, self.user.password),
                         verify=False, headers=headers)

            if func != requests.get:
                return_obj['changed'] = True  # Anything but GET should result in change

            self._process_response(return_obj=return_obj, http_response=r, ignore_error=ignore_error)

        except requests.exceptions.ConnectionError:
            self._process_connection_error(ignore_error=ignore_error, return_obj=return_obj)

        return return_obj

    def invoke_put(self, description, uri, data, ignore_error=False, requires_modules=None, requires_version=None,
                   warnings=[]):
        """
        Send a PUT request to the LMI.
        """
        return self._invoke_request(requests.put, description, uri, ignore_error, data,
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    warnings=warnings)

    def invoke_post(self, description, uri, data, ignore_error=False, requires_modules=None, requires_version=None,
                    warnings=[]):
        """
        Send a POST request to the LMI.
        """
        return self._invoke_request(requests.post, description, uri, ignore_error, data,
                                    requires_modules=requires_modules, requires_version=requires_version,
                                    warnings=warnings)

    def invoke_get(self, description, uri, ignore_error=False, requires_modules=None, requires_version=None,
                   warnings=[]):
        """
        Send a GET request to the LMI.
        """
        return self._invoke_request(requests.get, description, uri, ignore_error, requires_modules=requires_modules,
                                    requires_version=requires_version, warnings=warnings)

    def invoke_delete(self, description, uri, ignore_error=False, requires_modules=None, requires_version=None,
                      warnings=[]):
        """
        Send a DELETE request to the LMI.
        """
        return self._invoke_request(requests.delete, description, uri, ignore_error, requires_modules=requires_modules,
                                    requires_version=requires_version, warnings=warnings)

    def get_facts(self):
        """
        Get facts about the appliance
        """
        # Fact collection will abort on any exception
        try:
            self.get_version()

            # Check if appliance is setup before collecting Activation information
            import ibmsecurity.isds.setup_complete
            ret_obj = ibmsecurity.isds.setup_complete.get(self)
            if ret_obj['data'].get('configured') is True:
                self.get_activations()
        # Exceptions like those connection related will be ignored
        except:
            pass

    def get_version(self):
        """
        Get  appliance version (active partition)

        When firmware are installed or partition are changed, then this value is updated
        """
        self.facts['version'] = None
        import ibmsecurity.isds.firmware

        ret_obj = ibmsecurity.isds.firmware.get(self)
        for partition in ret_obj['data']:
            if partition['active'] is True:
                ver = partition['firmware_version'].split(' ')
                self.facts['version'] = ver[-1]

    def get_activations(self):
        """
        Get  appliance activations

        When new modules are activated or old ones de-activated this value is updated.
        """
        self.facts['activations'] = []
        import ibmsecurity.isds.activation

        ret_obj = ibmsecurity.isds.activation.get(self)
        for activation in ret_obj['data']:
            if activation['enabled'] == 'True':
                self.facts['activations'].append(activation['id'])
