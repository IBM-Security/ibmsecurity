import logging
from abc import ABCMeta, abstractmethod


class IBMError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class IBMAppliance:
    __metaclass__ = ABCMeta

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


    def create_return_object(self, rc=0, data={}, warnings=[], changed=False):
        return {'rc': rc, 'data': data, 'changed': changed, 'warnings': warnings}
