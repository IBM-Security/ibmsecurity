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
import subprocess

logger = logging.getLogger(__name__)

class Command(object):
    """
    This class is used to execute a single command.
    """

    def __init__(self):
        super(Command, self).__init__()

    def execute(self, cmd, capture_out = True):
        """
        This function will execute the specified command and return the
        exit code of the command, along with the output.
    
        @param cmd         [in] : An array which represents the command to be 
                                  executed, or a string representation of the
                                  command.
        @param capture_out [in] : Should we capture stdout?
    
        @retval A tuple containing the exit code and output.
        """

        try:
            useShell = False

            if type(cmd) is str:
                useShell = True
                logger.info("executing: {0}".format(cmd))
            else:
                logger.info("executing: {0}".format(" ".join(cmd)))

            if capture_out:
                out = subprocess.check_output(
                        cmd, shell=useShell, stderr=subprocess.STDOUT);
            else:
                out = subprocess.check_call(
                        cmd, shell=useShell, stderr=subprocess.STDOUT)

            if capture_out:
                logger.debug("  output: {0}".format(out))

            return 0, out

        except OSError as exc:
            logger.info("An exception occurred: {0}".format(exc))

            return 1, exc

        except subprocess.CalledProcessError as exc:
            logger.info("An exception occurred: {0}".format(exc))

            return exc.returncode, exc.output

