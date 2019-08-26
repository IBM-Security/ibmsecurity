"""
IBM Confidential
Object Code Only Source Materials
5725-V90
(c) Copyright International Business Machines Corp. 2020
The source code for this program is not published or otherwise divested
of its trade secrets, irrespective of what has been deposited with the
U.S. Copyright Office.
"""

import logging
import requests
import time
import urllib3
import sys
import re

from urllib.parse import urlparse

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OidcRp(object):
    """
    This class is used to test the OIDC RP authentication capability of
    IAG.  The class should never be used directly - an OP specific 
    implementation should be used instead.
    """

    def __init__(self, url):
        """
        Initialise this object.  

        \param url  [in] : The URL to the IAG.
        """

        super(OidcRp, self).__init__()

        self.url_ = url

    def authenticate(self, user, password):
        """
        Perform an OIDC authentication against the configured OP using the
        specified user name and password.  The created session will be
        returned upon a successful authentication, otherwise an exception
        will be raised.
        """

        session = requests.session()

        # The first request used to start the flow.
        rsp = session.get(self.url_, verify=False, allow_redirects=False)

        self.check_rsp_code(rsp, 302, "Failed to request the initial WRP page")

        # The second request, for the pkmsoidc page to kick start the OIDC
        # authentication.  The response to this request should be a 302.
        rsp = session.get("{0}/pkmsoidc?iss=default&TAM_OP=login".format(
                self.url_), verify=False, allow_redirects=False)

        self.check_rsp_code(rsp, 302, "Failed to start the OIDC RP flow")

        # The third request should be to the OIDC OP.
        rsp = self.authenticate_at_op(rsp.headers['location'], user, password)

        self.check_rsp_code(rsp, 302, "The OIDC flow failed at the OP")

        # Now we can complete the OIDC flow.  We have to massage the location
        # which is returned by the OP, substituting the fake host with the
        # real address information.
        url = re.sub(
           r"http(s?)://.*/",
           "{0}/".format(self.url_),
           rsp.headers['location']
        )

        rsp = session.get(url, verify=False, allow_redirects=False)

        self.check_rsp_code(rsp, 302, "Failed to complete the OIDC RP flow")

        # We can finally make a request for a protected resource to verify
        # that we are correctly authenticated.
        rsp = session.get(self.url_, verify=False, allow_redirects=False)

        self.check_rsp_code(rsp, 200, "Failed to use the authenticated session")

        return session 

    @classmethod
    def authenticate_at_op(self, location, user, password):
        """
        Perform an authentication at the OP.  This function should be 
        implemented for each type of OP which we support.
        """

        logger.critical("A base class has been used instead of specific OP "
                "implementation!")

        sys.exit(1)

    @classmethod
    def check_rsp_code(self, rsp, expected, description):
        """
        This helper function is used to check the response code contained in
        the HTTP response and display an error if an unexpected response code
        is received.
        """

        if expected != rsp.status_code:
            message = "{0}\nstatus: {1}\nheaders: {2}\nbody: {3}".format(
                description, rsp, rsp.headers, rsp.text)

            logger.critical(message)

            raise Exception(message)

class CIOidcRp(OidcRp):

    @classmethod
    def authenticate_at_op(self, location, user, password):
        """
        Perform an authentication at the CI OP.
        """

        # Create a new session against CI.
        session = requests.session()

        logger.info("Authenticating to CI....")

        # We now need to authenticate against the tenant.  This will involve
        # retrieving the login form, extracting the URL from the login form
        # and then posting the username/password to perform the authentication.
        parts = urlparse(location)

        form_url = "{0}://{1}/authsvc/mtfim/sps/authsvc?" \
            "PolicyId=urn:ibm:security:authentication:asf:basicldapuser".format(
            parts.scheme, parts.netloc)

        rsp = session.get(form_url, verify=False)

        self.check_rsp_code(rsp, 200, 
                                "CI did not return the expected login form")

        # Pull out the action from the body.  We could use a module such as
        # Beautiful Soup to parse the response body, but what we want is pretty
        # simple and so it is easier to just do a regular expression match.
        auth_url = rsp.text

        m = re.search('<body action="(.+?)"', rsp.text)

        if not m:
            message = "The CI login form does not look right: {0}"\
                        .format(rsp.text)

            logger.critical(message)

            raise Exception(message)

        auth_uri = m.group(1)

        rsp = session.post("{0}://{1}{2}".format(
                            parts.scheme, parts.netloc, auth_uri), 
                        data = {
                            "operation" : "verify", 
                            "username"  : user,
                            "password"  : password
                        })

        self.check_rsp_code(rsp, 200, "Failed to authenticate to CI")

        # Now that we have an authenticated session we want to perform the 
        # OIDC flow.
        rsp = session.get(location, verify=False, allow_redirects=False)

        self.check_rsp_code(rsp, 302, "The OIDC flow failed in CI")

        logger.info("Successfully authenticated to CI.")

        return rsp

