import logging
from abc import ABCMeta, abstractmethod


class IBMError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class IBMFatal(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class IBMResponse(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def succeeded_with_data(self):
        """
        Determines whether the execution succeeded with data retrieved.
        :return: True if the execution succeeded and the data is retrieved.
        """
        if self.get('rc', -1) == 0 and self.get("data"):
            return True
        return False

    def succeeded(self):
        """
        Determines whether the execution succeeded.
        :return: True if succeeded.
        """
        if self.get('rc', -1) == 0:
            return True
        return False

    def failed(self):
        """
        Determines whether the execution failed.
        :return: True if the execution failed.
        """
        if self.get('rc', -1) == 0:
            return False
        return True


class IBMAppliance(metaclass=ABCMeta):

    def __init__(self, hostname, user):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating an IBMAppliance')

        self.hostname = hostname
        self.user = user

        self.facts = {}
        self.get_facts()

    @abstractmethod
    def invoke_post_files(self, description, uri, fileinfo, data, ignore_error=False):
        """
        Send multipart/form-data upload file request to the appliance.
        """
        pass

    @abstractmethod
    def invoke_get_file(self, description, uri, filename, ignore_error=False):
        """
        Invoke a GET request and download the response data to a file
        """

    @abstractmethod
    def invoke_put(self, description, uri, data, ignore_error=False):
        """
        Send a PUT request to the LMI.
        """
        pass

    @abstractmethod
    def invoke_post(self, description, uri, data, ignore_error=False):
        """
        Send a POST request to the LMI.
        """
        pass

    @abstractmethod
    def invoke_get(self, description, uri, ignore_error=False):
        """
        Send a GET request to the LMI.
        """
        pass

    @abstractmethod
    def invoke_delete(self, description, uri, ignore_error=False):
        """
        Send a DELETE request to the LMI.
        """
        pass

    @abstractmethod
    def get_facts(self):
        """
        Extracts standard facts from the appliance

        Store it in JSON variable called "facts"
        """
        pass

    def create_return_object(self, rc=0, data={}, warnings=[],
                             changed=False):
        """
        Create a response object with the given properties.
        :param rc: The return code of the call.
        :param data: the data object of the response. Often in Json.
        :param warnings: The warnings of the executed call.
        :param changed: Whether there was any change.
        :return: The IBMResponse object.
        """
        return IBMResponse({'rc': rc,
                            'data': data,
                            'changed': changed,
                            'warnings': warnings,
                            'status_code': 0
                           })
