import datetime, jinja2, datasetmd.templates.iso19139

class DatasetMD:
    """This class is the base class for encapsulating scientific / 
    environmental Metadata to give detailed descriptions of datasets.
    
    :param base: Base metadata for a dataset (e.g. title, abstract)
    :type base: Base, defaults to None
    :param citation:
    :type citation: Citation
    :param feature: 
    :type feature: Feature, defaults to None
    :param owning_organisations:
    :type owning_organisations: list of Organisation objects, defaults to None
    :param publisher:
    :type publisher: Organisation, defaults to None
    """
    def __init__(self,
                    base=None,
                    citation=None,
                    feature=None,
                    owning_organisations=None,
                    publisher=None):
        """Constructor method"""
        self.base = base
        self.citation = citation
        self.feature = feature
        self.publisher = publisher
        
    def __str__(self):
        return """
    base: {0}
    citation: {1}
    feature: {2}
    owning:organisations: {3}
    publisher: {4}
""".format(str(self.base),
                str(self.citation),
                str(self.feature),
                str(self.owning_organisations),
                str(self.publisher))
        
    def toISO19139(self):
        """Outputs a DatasetMD object as ISO 19139 compliant XML
        
        :return: A string of text formatted to ISO 19139 XML
        :rtype: str
        """
        
        return print(jinja2.Template(datasetmd.templates.iso19139.template()).render(md=self))
    
    def toDataCiteXML(self):
        """Outputs a DatasetMD object as DataCite MetaData Store compliant 
        XML
        
        :return: A string of text formatted to DataCite XML schema
        :rtype: str
        """
        pass

class Base:
    """This class adds basic metadata to a DatasetMD object
    
    :param abstract: A detailed description of the dataset (who, what, when, 
            where, how, why)
    :type abstract: str, defaults to none
    :param created:
    :type created: datetime.datetime.date, defaults to None
    :param identifier: A unique identifier to the dataset
    :type identifier: str
    :param modified:
    :type modified: datetime.datetime.date, defaults to None
    :param title: A descriptive title for the dataset
    :type title: str, defaults to None
    """
    def __init__(self, 
                        abstract=None,
                        created=None,
                        identifier=None,
                        modified=None,
                        title=None):
        self.title = title
        self.abstract = abstract
        self.identifier = identifier
        self.modified = modified
        self.created = created
    
    def __str__(self):
        return("""
        abstract: {1}
        created: {3}
        modified: {4}
        identifier: {2}
        title: {0}
        """.format(self.title, 
                                    self.abstract,
                                    self.identifier,
                                    self.created,
                                    self.modified))

class Feature:
    """This class describes a geographic feature (point, line or polygon)
    associated with a dataset,
    
    :param crs_epsg_code:
    :type crs_epsg_code: int
    :param id:
    :type id: str, defaults to None
    :param latitude_northernmost:
    :type latitude_northernmost: float
    :param latiude_southernmost:
    :type latiude_southernmost: float
    :param longitude_easternmost:
    :type longitude_easternmost: float
    :param longitude_westernmost:
    :type longitude_westernmost: float
    """
    def __init__(self, 
                        crs_epsg_code=None,
                        id=None,
                        latitude_northernmost=None,
                        latiude_southernmost=None,
                        longitude_easternmost=None,
                        longitude_westernmost=None):
        self.id = id
        self.crs_epsg_code = crs_epsg_code
        self.latiude_southernmost = latiude_southernmost
        self.latitude_northernmost = latitude_northernmost
        self.longitude_easternmost = longitude_easternmost
        self.longitude_westernmost = longitude_westernmost
        
    def __str__(self):
        return """
        crs_epsg_code: {0}
        id: {1}
        latitude_northernmost: {2}
        latiude_southernmost: {3}
        longitude_easternmost: {4}
        longitude_westernmost: {5}
        """.format(self.crs_epsg_code,
                                self.id,
                                self.latitude_northernmost,
                                self.latiude_southernmost,
                                self.longitude_easternmost,
                                self.longitude_westernmost)

class Organisation:
    """This class describes an Organisation, typically a data provider, a 
    metadata publisher, or carrying another role in relation to a dataset.
    
    :param administrative_area:
    :type administrative_area: str, defaults to None
    :param city:
    :type city: str, defaults to None
    :param name:
    :type name: str, defaults to None:
    :param website:
    :type website: WebAddress, defaults to None
    """
    def __init__(self,
                        administrative_area=None,
                        city=None,
                        country=None,
                        delivery_point=None,
                        email_address=None,
                        name=None,
                        postal_code=None,
                        website=None):
        self.name = name
        self.delivery_point = delivery_point
        self.city = city
        self.administrative_area = administrative_area
        self.postal_code = postal_code
        self.country = country
        self.email_address = email_address
        self.website = website
        
    def __str__(self):
        return """
        name: {0}
        delivery_point: {1}
        city: {2}
        administrative_area: {3}
        postal_code: {4}
        country: {5}
        email_address: {6}
        website: {7}
        """.format(self.name,
                        self.delivery_point,
                        self.city,
                        self.administrative_area,
                        self.postal_code,
                        self.country,
                        self.email_address,
                        str(self.website))
        
class WebAddress:
    def __init__(self, url=None):
        self.url = url
    
    def __str__(self):
        return """
            url: {}
        """.format(self.url)

class Citation:
    """This class describes any formal citation identifier associated with a
    DatasetMD object
    
    :param doi:
    :type doi: str, defaults to None
    :param doi_publication_date:
    :type doi_publication_date: datetime.datetime.date, defaults to None
    :param short_doi:
    :type short_doi: str, defaults to None
    """
    def __init__(self, doi=None, 
                        doi_publication_date=None,
                        short_doi=None):
        self.doi = doi
        self.doi_publication_date = doi_publication_date
        self.short_doi = short_doi
                        
    def __str__(self):
        return """
        doi: {0}
        doi_publication_date: {1}
        short_doi: {2}
        """.format(self.doi,
                    self.doi_publication_date,
                    self.short_doi)
        
