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
import os

# Check to see if the debugging environment variable has been set, and if so
# we want to enable the specified log level.
if "IAG_DEBUG" in os.environ:
    logging.basicConfig(level=os.environ['IAG_DEBUG'])

