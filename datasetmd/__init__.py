"""
.. data:: CITE_STRING

      Used on :py:meth:`datasetmd.DatasetMD.cite` to indicate that the
      response should be a citation string

.. data:: FAMILY_THEN_GIVEN

      Used on :py:class:`datasetmd.Person` to indicate the full name should
      be rendered in the order `family_name` followed by `given_name`
      
.. data:: GIVEN_THEN_FAMILY

      Used on :py:class:`datasetmd.Person` to indicate the full name should
      be rendered in the order `given_name` followed by `family_name`
"""

import datetime, datasetmd.templates, jinja2

CITE_STRING = 'CITE_STRING'
FAMILY_THEN_GIVEN = 'FAMILY_THEN_GIVEN'
GIVEN_THEN_FAMILY = 'GIVEN_THEN_FAMILY'


class DatasetMD:
    """This class is the base class for encapsulating scientific / 
    environmental Metadata to give detailed descriptions of datasets.
    
    :param base: Base metadata for a dataset (e.g. title, abstract)
    :type base: Base, defaults to None
    :param citation: Decribes any formal citation (such as a digital
                object identifier from an authority like DataCite) which should
                be used to refer to the dataset in documents including reports
                or academic journal papers
    :type citation: Citation
    :param cross_references: A list of references to other relevant metadata
                entities, including other related instances of 
                :py:class:`datasetmd.DatasetMD`
    :type cross_references: list of :py:class:`datasetmd.CrossReference`
                objects, defaults to None
    :param feature: A geographic feature describing the spatial extent of the
                dataset
    :type feature: Feature, defaults to None
    :param included_in_data_catalogue:
    :type included_in_data_catalogue: WebAddress, defaults to None
    :param keywords: A list of lexical labels which are used to classify
                the content of the dataset described by the 
                :py:class:`datasetmd.DatasetMD` instance
    :type list of DefinedTerm objects, defaults to None:
    :param limitations: Describes any usage or legal limitations, outside of
                license agreement, which apply to the  dataset described by the
                :py:class:`datasetmd.DatasetMD`
    :type limitations: Limitations, defaults to None
    :param observed_properties:
    :type observed_properties: list of :py:class:`datasetmd.ObservedProperty`
                objects, defaults to None
    :param owning_organisations: A list of the 
                :py:class:`datasetmd.Organisation` s who have a claim on
                ownsership of the :py:class:`datasetmd.Dataset` instance
    :type owning_organisations: list of :py:class:`datasetmd.Organisation` 
                objects, defaults to None
    :param publisher: Indicates the :py:class:`datasetmd.Organisation` 
                responsible for publishing the dataset described by the 
                :py:class:`datasetmd.DatasetMD` instance
    :type publisher: Organisation, defaults to None
    """
    def __init__(self,
                            base=None,
                            citation=None,
                            cross_references=None,
                            feature=None,
                            included_in_data_catalogue=None,
                            keywords=None,
                            limitations=None,
                            observed_properties=None,
                            owning_organisations=None,
                            publisher=None):
        self.base = base
        self.citation = citation
        self.feature = feature
        self.limitations = limitations
        self.cross_references = cross_references
        self.publisher = publisher
        self.observed_properties = observed_properties
        self.keywords = keywords
        self.included_in_data_catalogue = included_in_data_catalogue
        
    def __str__(self):
        return """
    base: {0}
    citation: {1}
    feature: {2}
    observed_properties: {3}
    owning_organisations: {4}
    publisher: {5}
""".format(str(self.base),
                str(self.citation),
                str(self.feature),
                str(self.observed_properties),
                str(self.owning_organisations),
                str(self.publisher))
        
    def toISO19139(self):
        """Outputs a :py:class:`datasetmd.DatasetMD` object as ISO 19139 
        compliant XML
        
        :return: A string of text formatted to ISO 19139 XML
        :rtype: str
        """
        
        keyword_groups = []
        keywords = []
        
        if self.observed_properties is not None:
            for op in self.observed_properties:
                if op.in_defined_term_set is not None:
                    this_group = {'name': op.in_defined_term_set.title,
                                    'url': op.in_defined_term_set.url}
                    this_term = {'name': op.title,'url': op.url}
                    if this_group not in keyword_groups:
                        keyword_groups.append(this_group)
                        keywords.append({'name': op.in_defined_term_set.title,
                                    'url': op.in_defined_term_set.url,
                                    'keywords':[{'name': op.title,'url': op.url
                                }]})
                    elif this_group not in keywords[keyword_groups.index(this_group)]['keywords']:
                        keywords[keyword_groups.index(this_group)]['keywords'].append(this_term)
        
        if self.keywords is not None:
            for kw in self.keywords:
                if kw.in_defined_term_set is not None:
                    this_group = {'name': kw.in_defined_term_set.title,
                                    'url': kw.in_defined_term_set.url}
                    this_term = {'name': kw.title,'url': kw.url}
                    if this_group not in keyword_groups:
                        keyword_groups.append(this_group)
                        keywords.append({'name': kw.in_defined_term_set.title,
                                    'url': kw.in_defined_term_set.url,
                                    'keywords':[{'name': kw.title,'url': op.url
                                }]})
                    elif this_term not in keywords[keyword_groups.index(this_group)]['keywords']:
                        keywords[keyword_groups.index(this_group)]['keywords'].append(this_term)
        
        if not keywords:
            keywords = None
        
        return jinja2.Template(datasetmd.templates.iso19139.template()).render(md=self, 
                        citation_string=self.cite(CITE_STRING), keywords=keywords)
    
    def toDataCiteXML(self):
        """Outputs a :py:class:`datasetmd.DatasetMD` object as DataCite 
        MetaData Store compliant XML
        
        :return: A string of text formatted to DataCite XML schema
        :rtype: str
        """
        pass
        
    def toSchemaDotOrg(self):
        """Outputs a :py:class:`datasetmd.DatasetMD` as a JSON string, 
        following the Earth Science Informatics Partnership's Science on
        Schema patterns.
        
        :return: A JSON-LD formatted string using the Schema.org vocabulary
        :rtype: str
        """
        authors = datasetmd.templates.schemadotorg_creatorlist.template(self)
        return jinja2.Template(datasetmd.templates.schemadotorg.template()).render(md=self,
                    citation_string=self.cite(CITE_STRING),authors=authors)
        
    def cite(self, citationtype):
        """Creates a citation string for the :py:class:`datasetmd.DatasetMD` 
        object, or formats a citation to a well-known reference manager 
        format.
        
        :param citationtype: The value of type should be one of 
                                * :py:data:`datasetmd.CITE_STRING`
        :type citationtype: str
        
        :return: A string for the citation type requested
        :rtype: str, or None is `type` is not supported
        """
        return_value = None
        if citationtype.lower() == CITE_STRING:
            return_value = datasetmd.templates.citationstring.template(self)
        return return_value

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
    which describes the spatial extent of a dataset,
    
    :param crs_epsg_code: A four digit integer used to identify the co-ordinate
            reference system used in defining the 
            :py:class:`datasetmd.Feature`. The code is taken from the EPSG 
            Geodetic Parameter Dataset
    :type crs_epsg_code: int
    :param id: A unique or persistent identifier to the geographic feature
    :type id: str, defaults to None
    :param latitude_northernmost: The northernmost extent of the spatial 
            coverage described by the :py:class:`datasetmd.Feature`.
    :type latitude_northernmost: float
    :param latiude_southernmost: The southernmost extent of the spatial 
            coverage described by the :py:class:`datasetmd.Feature`.
    :type latiude_southernmost: float
    :param longitude_easternmost: The easternmost extent of the spatial 
            coverage described by the :py:class:`datasetmd.Feature`.
    :type longitude_easternmost: float
    :param longitude_westernmost: The westernmost extent of the spatial 
            coverage described by the :py:class:`datasetmd.Feature`.
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
    
    :param administrative_area: The geographic region in which the
            :py:class:`datasetmd.Organisation` is situated
    :type administrative_area: str, defaults to None
    :param city: The city in which the :py:class:`datasetmd.Organisation` is 
            situated
    :type city: str, defaults to None
    :param country: The country in which the :py:class:`datasetmd.Organisation`
            is situated
    :type country: str, defaults to None
    :param delivery_point: The street address of the
            :py:class:`datasetmd.Organisation` 
    :type delivery_point: str, defaults to None
    :param email_address: A central contact e-mail for the 
            :py:class:`datasetmd.Organisation`
    :type email_address: str, defaults to None
    :param name: The name of the :py:class:`datasetmd.Organisation`
    :type name: str, defaults to None
    :param postal_code: A postal code (for example post code, zipcode or
            EirCode) for the :py:class:`datasetmd.Organisation`
    :type postal_code: str, defaults to None
    :param website: A website associated with the 
            :py:class:`datasetmd.Organisation`
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
    """ This class describes an HTTP, FTP or other such web address
     
    :param title: A label or title for the :py:class:`datasetmd.WebAddress` that
            can be used in human readable serialisations of the metadata
    :type title: str
    :param url: The machine actionable link of the WebAddress
    :type url: str
    """
    def __init__(self, title=None, url=None):
        self.url = url
        self.title = title
    
    def __str__(self):
        return """
            title: {0}
            url: {1}
        """.format(self.title, self.url)

class Citation:
    """This class describes any formal citation identifier associated with a
    :py:class:`datasetmd.DatasetMD` object
    
    :param authors: A list of authors for the dataset
    :type authors: list of :py:class:`datasetmd.Person` or 
            :py:class:`datasetmd.Organisation` objects, defaults to None
    :param doi: A digital object identifier associated with the parent
            :py:class:`datasetmd.DatasetMD` instance. The doi given here
            should not use any prefix like http:// or doi:
    :type doi: str, defaults to None
    :param doi_publication_date: The date on which the digital object 
            identifier was issued
    :type doi_publication_date: datetime.datetime.date, defaults to None
    :param doi_publisher: The :py:class:`datasetmd.Organisation` responsible
            for minting the digital object identifier
    :type doi_publisher: Organisation, defaults to None
    :param prefer_short_doi: A boolean indicating if the short doi is the
            preferred identifier to use when outputting a citation string
    :type prefer_short_doi: bool, defaults to False
    :param short_doi: A shortened form of the digital object identifier
            as created by the `Short doi service <https://shortdoi.org/>`__
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
    
    :param affiliation: A list of :py:class:`datasetmd.Organisation`s that
            a :py:class:`datasetmd.Person` is affilitated with
    :type affiliation: list of :py:class:`datasetmd.Organisation` objects, 
            defaults to None
    :param family_name: The py:class:`datasetmd.Person`'s family name,
            in Europe and the US, most often their last name
    :type family_name: str, defaults to None
    :param given_name: The py:class:`datasetmd.Person`'s given name,
            in Europe and the US, most often their first name
    :type given_name: str, defaults to None
    :param name_order: The order in ehich the :py:class:`datasetmd.Person`'s
            family and given names should be rendered
    :type name_order: str, use the value of 
            :py:data:`datasetmd.FAMILY_THEN_GIVEN` or 
            :py:data:`datasetmd.GIVEN_THEN_FAMILY`, defaults to 
            :py:data:`datasetmd.GIVEN_THEN_FAMILY`
    :param role:
    :type role:
    """
    
    def __init__(self,
                    affiliation=None,
                    family_name=None,
                    given_name=None,
                    name_order=GIVEN_THEN_FAMILY,
                    role=None):
        self.affiliation = affiliation
        self.family_name = family_name
        self.given_name = given_name
        self.role = role
        self.name_order = name_order
    
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

class DefinedTerm(WebAddress):
    """This class describes a term defined in a controlled vocabulary,
    taxonomy or as an individual in an ontology.
    
    :param in_defined_term_set: The vocabulary or ontology from which
            the :py:class:`datasetmd.DefinedTerm` is taken
    :type in_defined_term_set: DefinedTermSet, defaults to None
    :param publication_date: The date on which the
            :py:class:`datasetmd.DefinedTerm` was published
    :type publication_date: `datetime.datetime.Date`, defaults to None
    :param term_code: A code taken from the 
            :py:class:`datasetmd.DefinedTermSet` which is used in the
            context of that ontology or vocabulary to identify the
            :py:class:`datasetmd.DefinedTerm`. Foe example, 
            `SDN:P01:ALATZZ01`
    :type term_code: str, defaults to None
    :param title: A lexical label, such as a `skos:prefLabel` which describes
            the term
    :type title: str, defaults to None
    :param url: The URL which links to the original controlled vocabulary
            or ontology term
    :type url: str, defaults to None
    """
    def __init__(self, in_defined_term_set=None, 
                                        publication_date=None, 
                                        term_code=None,
                                        title=None, url=None):
        super().__init__(title=title, url=url)
        self.in_defined_term_set = in_defined_term_set
        self.term_code = term_code
        self.publication_date = publication_date
        
    def __str__(self):
        return """
                in_defined_term_set: {0}
                term_code: {1}
                title: {2}
                url: {3}
        """.format(str(self.in_defined_term_set),
                    self.term_code,
                    self.title,
                    self.url)

class DefinedTermSet(WebAddress):
    """This class gives details of a vocabulary or ontology which describes a
    number of :py:class:`datasetmd.DefinedTerm` s
    
    :param publication_date: The date on which the
            :py:class:`datasetmd.DefinedTermSet` was published
    :type publication_date: `datetime.datetime.Date`, defaults to None
    :param term_code: A short code which is commonly used to identify the
            :py:class:`datasetmd.DefinedTermSet`, such as `SDN:P01::`
    :type term_code: str, defaults to None
    :param title: A lexical label, such as a `skos:prefLabel` which describes
            the :py:class:`datasetmd.DefinedTermSet`
    :type title: str, defaults to None
    :param url: The URL of the controlled vocabulary or ontology
    :type url: str, defaults to None
    """
    def __init__(self, publication_date=None, 
                                        term_code=None,
                                        title=None, url=None):
        super().__init__(title=title, url=url)
        self.publication_date = publication_date
                    
class ObservedProperty(DefinedTerm):
    """This class describes properties that have been observed or modelled
    and recorded within the dataset described by a 
    :py:class`datasetmd.DatasetMD` instance
    
    :param in_defined_term_set: The vocabulary or ontology from which
            the :py:class:`datasetmd.ObservedProperty` is taken
    :type in_defined_term_set: DefinedTermSet, defaults to None
    :param publication_date:
    :type publication_date: `datetime.datetime.Date`
    :param term_code:
    :type term_code: str, defaults to None
    :param title:
    :type title: str, defaults to None
    :param url:
    :type url: str,defaults to None
    """
    def __init__(self, in_defined_term_set=None, 
                            publication_date=None,
                            term_code=None, 
                            title=None, 
                            url=None):
        super().__init__(in_defined_term_set=in_defined_term_set, 
                                publication_date=publication_date,
                                title=title, url=url, term_code=term_code,)
        
    def __str__(self):
        return """
                in_defined_term_set: {0}
                term_code: {1}
                title: {2}
                url: {3}
        """.format(str(self.in_defined_term_set),
                    self.term_code,
                    self.title,
                    self.url)

class License:
    """This class describes the license associated with an instance of the
    :py:class:`datasetmd.DatasetMD` class. The license describes how a
    dataset may be distributed and reused. The class definition is informed
    by the Schema.org CreativeWork pattern, and the recommendations of the 
    Earth Science Informatics Partnership's Science on Schema working group.
    
    :param description:
    :type description: str, defaults to None
    :param in_defined_term_set: 
    :type in_defined_term_set: DefinedTermSet, defaults to None
    :param name:
    :type name: str, defaults to None
    :param spdx_url:
    :type spdx_url: WebAddress, defaults to None
    :param url: 
    :type url: WebAddress, defaults to None
    """
    def __init__(self, description=None,
                        in_defined_term_set=None,
                        name=None,
                        spdx_url=None,
                        url=None):
        self.description = description
        self.in_defined_term_set = in_defined_term_set
        self.name = name
        self.spdx_url = spdx_url
        self.url = url
        
class Limitations:
    """
    
    :param use_limitations:
    :type use_limitations: list of str, defaults to None
    """
    def __init__(self, use_limitations=None):
        self.use_limitations = use_limitations
        
class CrossReference(WebAddress):
    def __init__(self):
        """This class defines cross-references to other datasets
        and relevant metadata objects
    
        :param cross_reference_type:
        :type cross_reference_type: DefinedTerm, defaults to None
        :param title:
        :type title: str, defaults to None
        :param url:
        :type url: str, defaults to None
    """
    def __init__(self, cross_reference_type=None, 
                                        title=None, url=None):
        super().__init__(title=title, url=url)
        self.cross_reference_type = cross_reference_type