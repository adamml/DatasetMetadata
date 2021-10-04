class DatasetMD:
    """This class is the base class for encapsulating scientific / 
    environmental Metadata to give detailed descriptions of datasets.
    
    :param base:
    :param feature: 
    :type feature: Feature, defaults to None
    :param publisher:
    :type publisher: Organisation, defaults to None
    """
    def __init__(self):
        """Constructor method"""
        self.base = None
        self.feature = None
        self.publisher = None
        
    def toISO19139(self):
        """Outputs a DatasetMD object as ISO 19139 compliant XML
        
        :return: A string of text formatted to ISO 19139 XML
        :rtype: str
        """
        return ""
    
    def toDataCiteXML(self):
        """Outputs a DatasetMD onject as DataCite MetaData Store compliant 
        XML
        
        :return: A string of text formatted to DataCite XML schema
        :rtype: str
        """
        pass

class Feature:
    """This class describes a geographic feature (point, line or polygon)
    associated with a dataset,
    
    """
    def __init__(self):
        self.id = None
        self.crs_epsg_code = None
        self.southernmost_latitude = None
        self.northernmost_latitude = None
        self.westernmost_longitude = None
        self.easternmost_longitude = None

class Organisation:
    """This class describes an Organisation, typically a data provider, a 
    metadata publisher, or carrying another role in relation to a dataset.
    
    :param name:
    :type name: str, defaults to None:
    """
    def __init__(self):
        self.name = None
        self.delivery_point = None
        self.city = None
        self.administrative_area = None
        self.postal_code = None
        self.country = None
        self.email_address = None
        self.website = None
        
class WebAddress:
    pass
        