import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from ibmsecurity.appliance.ibmappliance import IBMAppliance
from ibmsecurity.appliance.isvgappliance import ISVGAppliance
from ibmsecurity.appliance.ibmappliance import IBMError
from ibmsecurity.utilities import tools

try:
    basestring
except NameError:
    basestring = (str, bytes)


class ISVGApplianceAdminProxy(ISVGAppliance):
    def __init__(self, adminProxyHostname, user, hostname, adminProxyProtocol='https', adminProxyPort=443,
                 adminProxyApplianceShortName=False):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Creating an ISVGAppliance over AdminProxy')

        self.adminProxyProtocol = adminProxyProtocol
        self.adminProxyHostname = adminProxyHostname

        # Type checking and tranformation to safely reuse this variable later on
        if isinstance(adminProxyPort, basestring):
            self.adminProxyPort = int(adminProxyPort)
        else:
            self.adminProxyPort = adminProxyPort

        self.adminProxyApplianceShortName = adminProxyApplianceShortName

        ISVGAppliance.__init__(self, hostname, user)

    def _url(self, uri):
        # shorten the junction name from hostname parameter
        # e.g.  isvg.ibm.com -junction-> /isvg          (with short name)
        #       isvg.ibm.com -junction-> /isvg.ibm.com  (without short name)
        if self.adminProxyApplianceShortName:
            applianceJunction = self.hostname.split('.')[0]
        else:
            applianceJunction = self.hostname

        # Build up the URL
        url = self.adminProxyProtocol + "://" + self.adminProxyHostname + ":" + str(
            self.adminProxyPort) + "/" + applianceJunction + uri
        self.logger.info("Issuing request to Appliance over AdminProxy: " + url)

        return url
