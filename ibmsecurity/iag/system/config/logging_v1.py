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

logger = logging.getLogger(__name__)

from ibmsecurity.iag.system.config.base import Base
from ibmsecurity.iag.system.config.base import Simple
from ibmsecurity.iag.system.config.base import AutoNumber

##############################################################################

class LoggingV1(Base):
    """
    This class is used to represent the logging configuration of an IAG
    container.
    """

    def __init__(self,
                    components     = None,
                    request_log    = None,
                    statistics     = None,
                    tracing        = None,
                    transaction    = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param components    : An array of 
                               ibmsecurity.iag.system.config.LoggingComponent
                               objects to indicate which logging components 
                               should be enabled.
        @param request_log:    An ibmsecurity.iag.system.config.request_log
                               object which controls the format and location
                               of the request log.  
        @param statistics    : An array of 
                               ibmsecurity.iag.system.config.LoggingStatistic 
                               objects which control which statistics will be
                               gathered.
        @param tracing       : An array of
                               ibmsecurity.iag.system.config.tracing objects
                               which control which trace levels will be set.
        @param transaction   : An ibmsecurity.iag.system.config.transaction
                               object which can be used to enable transaction
                               logging.
        """

        super(LoggingV1, self).__init__()

        self.components     = self._checkList(LoggingComponentV1, components)
        self.statistics     = self._checkList(LoggingStatisticV1, statistics)
        self.tracing        = self._checkList(TracingV1, tracing)
        self.transaction    = self._check(TransactionV1, transaction)
        self.request_log    = self._check(RequestLogV1, request_log)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class LoggingComponentV1(AutoNumber):
    """
    This class is used to represent a single logging component.
    """

    audit_azn    = ()
    audit_authn  = ()

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("_","."), version

##############################################################################

class LoggingStatisticV1(Base):
    """
    This class is used to represent the configuration of statistics logging
    within an IAG container.
    """

    def __init__(self,
                    component,
                    file_name,
                    interval  = 30,
                    count     = 5):
        """
        Initialise this class instance.  The parameters are as follows:

        @param component : The name of the statistics component.
        @param file_name : The name of the file to which the statistics will
                           be written.
        @param interval  : The interval at which the statistics will be
                           gathered.
        @param count     : The number of intervals to gather statistics for.
        """

        super(LoggingStatisticV1, self).__init__()

        self.component = Simple(str, component)
        self.file_name = Simple(str, file_name)
        self.interval  = Simple(int, interval)
        self.count     = Simple(int, count)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class TracingV1(Base):
    """
    This class is used to represent the configuration of a tracing component
    within an IAG container.
    """

    def __init__(self, component, file_name, level):
        """
        Initialise this class instance.  The parameters are as follows:

        @param component : The name of the tracing component.
        @param file_name : The name of the file to which the tracing will
                           be written.
        @param level     : The level at which the tracing component will be
                           enabled.
        """

        super(TracingV1, self).__init__()

        self.component = Simple(str, component)
        self.file_name = Simple(str, file_name)
        self.level     = Simple(int, level)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class TransactionV1(Base):
    """
    This class is used to represent the configuration of a transaction logging
    component within an IAG container.
    """

    def __init__(self,
                    file_name,
                    max_file_size = 1024000,
                    max_files     = 1,
                    compress      = False):
        """
        Initialise this class instance.  The parameters are as follows:

        @param file_name     : The name of the file which will be generated.
        @param max_file_size : The maximum size of the generated file.
        @param max_files     : The maximum number of rollover files generated.
        @param compress      : Should rolled over files be compressed?
        """

        super(TransactionV1, self).__init__()

        self.file_name     = Simple(str, file_name)
        self.max_file_size = Simple(int, max_file_size)
        self.max_files     = Simple(int, max_files)
        self.compress      = Simple(bool, compress)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

class RequestLogV1(Base):
    """
    This class is used to represent the configuration of the request logging
    within an IAG container.
    """

    def __init__(self,
                    format    = None,
                    file_name = None):
        """
        Initialise this class instance.  The parameters are as follows:

        @param format        : The format of the request log.  If no format
                               is specified a default format will be used.  See
                               the documentation for information on how to
                               construct the format string.
        @param file_name     : The name of the file which will be generated.
                               If no file is specified the request log will
                               be written to stdout.
        """

        super(RequestLogV1, self).__init__()

        self.format    = Simple(str, format)
        self.file_name = Simple(str, file_name)

    def version(self):
        """
        Return the minimal IAG version for this object.
        """
        return "19.12"

##############################################################################

