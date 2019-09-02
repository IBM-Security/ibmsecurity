"""
IBM Confidential
Object Code Only Source Materials
5725-V90
(c) Copyright International Business Machines Corp. 2020
The source code for this program is not published or otherwise divested
of its trade secrets, irrespective of what has been deposited with the
U.S. Copyright Office.
"""

import abc

from enum import Enum

##############################################################################

class Base(metaclass=abc.ABCMeta):
    """
    This class serves as the base class for all of the configuration objects.
    It can be used as a template, and is mostly used to ensure that all of
    the required functions of a configurator object have been implemented.
    """

    @abc.abstractmethod
    def version(self):
        """
        Return the minimal IAG version for this object.  All config objects 
        must implement this function.
        """

    def getData(self, version):
        """
        Return the data which is managed by this object.  The data should be
        in the form of a dictionary.
        """

        data = {}

        for name, value in vars(self).items():
            if value is not None:
                version = Base.__processData(name, value, data, version)

        if (self.version() > version):
            version = self.version()

        return data, version

    @classmethod
    def _check(self, data_type, data):
        """
        This function is used to check to ensure that the specified data is
        of the correct data type.  An exception will be thrown if the data
        type is incorrect.

        @param data_type : The type of data
        @param data      : The data itself

        @retval The data
        """

        if data is None:
            return data

        if isinstance(data_type, list):
            found = False

            for inst_type in data_type:
                if isinstance(data, inst_type):
                    found = True
                    break

            if not found:
                raise Exception("Data of an incorrect type was specified.")
        else:
            if not isinstance(data, data_type):
                raise Exception("Data of an incorrect type was specified.")

        return data

    @classmethod
    def _checkList(self, data_type, data):
        """
        This function is used to check to ensure that the specified data is
        of the correct data type.  An exception will be thrown if the data
        type is incorrect.

        @param data_type : The type of data
        @param data      : The data itself

        @retval The data
        """

        if data is not None:
            if not isinstance(data, list):
                raise Exception("Data of an incorrect type was specified.")

            if len(data) > 0 and not isinstance(data[0], data_type):
                raise Exception("Data of an incorrect type was specified.")

        return data

    @staticmethod
    def __processData(name, value, data, version):
        """
        The following static method is a recursive function which is used to 
        build the data map based on the value of the supplied data.

        @param name    : The name of the data.
        @param value   : The value of the data.
        @param data    : The resultant data map.
        @param version : The current IAG version information associated with 
                         the data.
        """

        if isinstance(value, list):
            data[name] = []

            for inst in value:
                Base.__processData(name, inst, data[name], version)

        elif isinstance(value, dict):
            data[name] = {}

            for entry_name, entry_value in value.items(): 
                Base.__processData(entry_name, entry_value, data[name], version)

        else:
            item_value, version = value.getData(version)

            if item_value is not None:
                if isinstance(data, list):
                    data.append(item_value)
                else:
                    data[name] = item_value

        return version

##############################################################################

class Simple(Base):
    """
    This class is used to manage a simple data type.
    """

    def __init__(self, data_type, value):
        """
        Initialise this class instance.  The parameters are as follows:

        @param data_type : The expected data type.
        @param value     : The value associated with this simple data type.
        """

        self.value_ = self._check(data_type, value)

    def version(self):
        """
        Return the minimal IAG version for this instance.  A simple piece of
        data does not actually need/use a version.  The version of the 
        'owning' class will be used instead.
        """
        
        return "0"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        return self.value_, version

##############################################################################

class SimpleList(Base):
    """
    This class is used to manage a list of simple data types.
    """

    def __init__(self, data_type, value):
        """
        Initialise this class instance.  The parameters are as follows:

        @param data_type : The expected data type.
        @param value     : The value associated with this simple data type.
        """

        self.value_ = self._checkList(data_type, value)

    def version(self):
        """
        Return the minimal IAG version for this instance.  A simple piece of
        data does not actually need/use a version.  The version of the 
        'owning' class will be used instead.
        """
        
        return "0"

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        return self.value_, version

##############################################################################

class AutoNumber(Enum):
    """
    This class comes directly from the python documentation and provides a
    way to automatically assign a number to an enum value.
    """

    def __new__(cls):
        value       = len(cls.__members__) + 1
        obj         = object.__new__(cls)
        obj._value_ = value

        return obj

    def getData(self, version):
        """
        Return the data which is managed by this object.  
        """

        if (self.version() > version):
            version = self.version()

        return self.name.replace("__"," "), version

##############################################################################

