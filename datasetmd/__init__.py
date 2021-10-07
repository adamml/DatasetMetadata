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
        
        return jinja2.Template(datasetmd.templates.iso19139.template()).render(md=self, citation_string=self.cite('string'))
    
    def toDataCiteXML(self):
        """Outputs a DatasetMD object as DataCite MetaData Store compliant 
        XML
        
        :return: A string of text formatted to DataCite XML schema
        :rtype: str
        """
        pass
        
    def cite(self, type):
        """Creates a citation string for the DatasetMD object, or formats a
        citation to a well-known reference manager format.
        
        :param type: The value of type should be one of `string`
        :type type: str
        
        :return: A string for the citation type requested
        :rtype: str, or None is `type` is not supported
        """
        ret_string = ""
        author_count = 0
        affiliation_list = []
        if type.lower() == 'string':
            if self.citation is not None:
                if self.citation.authors is not None:
                    for author in self.citation.authors:
                        if author_count > 0:
                            ret_string += '; '
                        if isinstance(author, Person):
                            if author.family_name is None:
                                ret_string += '{}'.format(author.given_name)
                                author_count += 1
                            elif author.given_name is None:
                                ret_string += '{}'.format(author.family_name)
                                author_count += 1
                            else:
                                ret_string += '{0}, {1}'.format(author.family_name, author.given_name)
                                author_count += 1
                            if author.affiliation is not None:
                                affiliation_count = 0
                                for affiliation in author.affiliation:
                                    if affiliation.name is not None:
                                        if affiliation.country is not None:
                                            citation_affiliation = '{0}, {1}'.format(affiliation.name, affiliation.country)
                                        else:
                                            citation_affiliation = '{}'.format(affiliation.name)
                                        if citation_affiliation not in affiliation_list:
                                            affiliation_list.append(citation_affiliation)
                                        try:
                                            if affiliation_count > 0:
                                                ret_string += ','
                                            ret_string += ' ({})'.format(affiliation_list.index(citation_affiliation) + 1)
                                            affiliation_count += 1
                                        except ValueError:
                                            pass
                        elif isinstance(author, Organisation):
                            if author.name is not None:
                                ret_string += '{}'.format(author.name)
                                if author.country is not None:
                                    citation_affiliation = '{0}, {1}'.format(author.name, author.country)
                                else:
                                    citation_affiliation = '{}'.format(author.name)
                                if citation_affiliation not in affiliation_list:
                                    affiliation_list.append(citation_affiliation)
                                try:
                                    ret_string += ' ({})'.format(affiliation_list.index(citation_affiliation) + 1)
                                except ValueError:
                                    pass
                                author_count += 1
                if ret_string:
                    ret_string = '{}. '.format(ret_string)
                if self.citation.doi_publication_date is not None:
                    ret_string += '({})'.format(self.citation.doi_publication_date.year)
                if ret_string:
                    ret_string = '{}. '.format(ret_string)
                if self.base.title is not None:
                    ret_string += '{}'.format(self.base.title)
                if ret_string:
                    ret_string = '{}. '.format(ret_string)
                if self.citation.doi_publisher is not None:
                    if self.citation.doi_publisher.name is not None:
                        if self.citation.doi_publisher.country is not None:
                            ret_string += '{}, {}'.format(self.citation.doi_publisher.name, self.citation.doi_publisher.country)
                        else:
                            ret_string += '{}'.format(self.citation.doi_publisher.name)
                if ret_string:
                    ret_string = '{}. '.format(ret_string)
                if self.citation.prefer_short_doi:
                    if self.citation.short_doi is not None:
                        ret_string += 'doi: {}'.format(self.citation.short_doi)
                    elif self.citation.doi is not None:
                        ret_string += 'doi: {}'.format(self.citation.doi)
                else:
                    if self.citation.doi is not None:
                        ret_string += 'doi: {}'.format(self.citation.doi)
                    elif self.citation.short_doi is not None:
                        ret_string += 'doi: {}'.format(self.citation.short_doi)
                if ret_string:
                    ret_string = '{}. '.format(ret_string)
                if affiliation_list:
                    affiliation_count = 1
                    for affiliation in affiliation_list:
                        ret_string += '({0}) {1}. '.format(affiliation_count, affiliation)
                        affiliation_count += 1
        ret_string = ret_string.strip()
        if not ret_string:
            ret_string = None
        return ret_string
        

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
    
    :param authors: A list of authors for the dataset
    :type authors: list of Person or Organisation objects, defaults to None
    :param doi:
    :type doi: str, defaults to None
    :param doi_publication_date:
    :type doi_publication_date: datetime.datetime.date, defaults to None
    :param doi_publisher:
    :type doi_publisher: Organisation, defaults to None
    :param prefer_short_doi:
    :type prefer_short_doi: bool, defaults to False
    :param short_doi:
    :type short_doi: str, defaults to None
    """
    def __init__(self, authors=None,
                        doi=None, 
                        doi_publication_date=None,
                        doi_publisher=None,
                        prefer_short_doi=False,
                        short_doi=None):
        self.doi = doi
        self.doi_publication_date = doi_publication_date
        self.short_doi = short_doi
        self.authors = authors
        self.doi_publisher = doi_publisher
        self.prefer_short_doi = prefer_short_doi
                        
    def __str__(self):
        return """
        authors: {0}
        doi: {1}
        doi_publication_date: {2}
        doi_publisher: {3}
        prefer_short_doi: {4}
        short_doi: {5}
        """.format(self.authors,
                    self.doi,
                    self.doi_publication_date,
                    str(self.doi_publisher),
                    self.prefer_short_doi,
                    self.short_doi)

class Person:
    """This class describe a person, who may be affiliated with one or more 
    Organisations and have one or more roles associated in some way with a 
    DatasetMD object
    
    :param affiliation:
    :tyoe affiliation: list of Organisation objects, defaults to None
    :param family_name:
    :type family_name: str, defaults to None
    :param given_name: 
    :type given_name: str, defaults to None
    """
    def __init__(self,
                    affiliation=None,
                    family_name=None,
                    given_name=None,
                    role=None):
        self.affiliation = affiliation
        self.family_name = family_name
        self.given_name = given_name
        self.role = role
    
    def __str__(self):
        return """
            affiliation: {0}
            family_name: {1}
            given_name: {2}
            role: {3}
        """.format(self.affiliation,
                    self.family_name,
                    self.given_name,
                    self.role)
                    