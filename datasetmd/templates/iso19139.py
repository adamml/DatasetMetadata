def template():
    """
    This class provides a  Jinja2 template for creating an ISO19139 XML record
    from a DatasetMD object
    """
    return """<gmd:MD_Metadata
        xmlns:gco="http://www.isotc211.org/2005/gco"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:gmx="http://www.isotc211.org/2005/gmx"
        xmlns:xlink="http://www.w3.org/1999/xlink">
    
    <!-- File identifier -->
    
    <gmd:fileIdentifier>
        <gco:CharacterString>{{ md.base.identifier }}</gco:CharacterString>
    </gmd:fileIdentifier>
    
    <!-- Metadata language -->
    
    <gmd:language>
        <gco:languageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="eng">eng</gco:languageCode>
    </gmd:language>
    
    <!-- Metadata record heirarchy level -->
    
    <gmd:hierarchyLevel>
        <gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#MD_ScopeCode" codeListValue="dataset">dataset</gmd:MD_ScopeCode>
    </gmd:hierarchyLevel>
    
    <!-- Metadata publishing organisation -->
    
    <gmd:contact>
        <gmd:CI_ResponsibleParty>
            <gmd:organisationName>
                <gco:CharacterString>{{ md.publisher.name }}</gco:CharacterString>
            </gmd:organisationName>
            <gmd:contactInfo>
                <gmd:CI_Contact>
                    <gmd:address>
                        <gmd:CI_Address>
                            <gmd:deliveryPoint>
                                <gco:CharacterString>{{ md.publisher.delivery_point }}</gco:CharacterString>
                            </gmd:deliveryPoint>
                            <gmd:city>
                                <gco:CharacterString>{{ md.publisher.city }}</gco:CharacterString>
                            </gmd:city>
                            <gmd:administrativeArea>
                                <gco:CharacterString>{{ md.publisher.administrative_area }}</gco:CharacterString>
                            </gmd:administrativeArea>
                            <gmd:postalCode>
                                <gco:CharacterString>{{ md.publisher.postal_code }}</gco:CharacterString>
                            </gmd:postalCode>
                            <gmd:country>
                                <gco:CharacterString>{{ md.publisher.country }}</gco:CharacterString>
                            </gmd:country>
                            <gmd:electronicMailAddress>
                                <gco:CharacterString>{{ md.publisher.email_address }}</gco:CharacterString>
                            </gmd:electronicMailAddress>
                        </gmd:CI_Address>
                    </gmd:address>
                </gmd:CI_Contact>
            </gmd:contactInfo>
            <gmd:role>
                <gmd:CI_RoleCode codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_RoleCode" codeListValue="pointOfContact">pointOfContact</gmd:CI_RoleCode>
            </gmd:role>
        </gmd:CI_ResponsibleParty>
    </gmd:contact>
    
    <!-- Metadata record version date stamp -->
    
    <gmd:dateStamp>
        <gco:Date>{{ md.base.modified }}</gco:Date>
    </gmd:dateStamp>
    
    <!-- Metadata standard name and version information -->
    
    <gmd:metadataStandardName>
        <gco:CharacterString>ISDI Metadata Profile</gco:CharacterString>
    </gmd:metadataStandardName>
  
    <gmd:metadataStandardVersion>
        <gco:CharacterString>1.2</gco:CharacterString>
    </gmd:metadataStandardVersion>
    
    <!-- Dataset doi -->
    
    {%- if md.citation.doi is not none %}
    <gmd:dataSetURI>
        <gco:CharacterString>{{ md.citation.doi }}</gco:CharacterString>
    </gmd:dataSetURI>
    {% endif %}
    
    <!-- Dataset coordinate reference system -->
    
    <gmd:referenceSystemInfo>
        <gmd:MD_ReferenceSystem>
            <gmd:referenceSystemIdentifier>
                <gmd:RS_Identifier>
                    <gmd:code>
                        <gco:CharacterString>http://www.opengis.net/def/crs/EPSG/0/{{ md.feature.epsg_code }}</gco:CharacterString>
                    </gmd:code>
                    <gmd:codeSpace>
                        <gco:CharacterString>INSPIRE RS registry</gco:CharacterString>
                    </gmd:codeSpace>
                </gmd:RS_Identifier>
            </gmd:referenceSystemIdentifier>
        </gmd:MD_ReferenceSystem>
    </gmd:referenceSystemInfo>
  
    <gmd:identificationInfo>
        <gmd:MD_IdentificationInfo>
            <gmd:citation>
                <gmd:CI_Citation>
                
                    <!-- Dataset title -->
                
                    <gmd:title>
                        <gco:CharacterString>{{ md.base.title }}</gco:CharacterString>
                    </gmd:title>
                
                    <!-- Dates to go in here -->
                    
                    <gmd:identifier>
                        <gmd:MD_Identifier uuid="{{ md.base.identifier }}">
                            <gmd:code>
                                <gco:CharacterString>{{ md.base.identifier }}</gco:CharacterString>
                            </gmd:code>
                        </gmd:MD_Identifier>
                    </gmd:identifier>
                    
                    {%- if md.citation.short_doi is not none %}
                    <!-- Dataset short doi -->
                    
                    <gmd:identifier>
                        <gmd:MD_Identifier uuid="{{ md.base.identifier }}">
                            <gmd:code>
                                <gco:CharacterString>{{ md.citation.short_doi }}</gco:CharacterString>
                            </gmd:code>
                        </gmd:MD_Identifier>
                    </gmd:identifier>
                    {% endif %}
                    
                    {%- if md.citation.doi is not none %}
                    <!-- Dataset doi -->
                    
                    <gmd:identifier>
                        <gmd:MD_Identifier uuid="{{ md.base.identifier }}">
                            <gmd:code>
                                <gco:CharacterString>{{ md.citation.doi }}</gco:CharacterString>
                            </gmd:code>
                        </gmd:MD_Identifier>
                    </gmd:identifier>
                    {% endif %}
                    
                    <!-- TODO: doi suggested citation text to go here -->
                    
                    <!-- Dataset owning organisation(s) -->
                    {%- for org in md.owning_organisations %}
                    
                    <gmd:pointOfContact>
                        <gmd:CI_ResponsibleParty>
                            <gmd:organisationName>
                                <gco:CharacterString>{{ org.name }}</gco:CharacterString>
                            </gmd:organisationName>
                            <gmd:contactInfo>
                                <gmd:CI_Contact>
                                    <gmd:address>
                                        <gmd:CI_Address>
                                            <gmd:deliveryPoint>
                                                <gco:CharacterString>{{ org.delivery_point }}</gco:CharacterString>
                                            </gmd:deliveryPoint>
                                            <gmd:city>
                                                <gco:CharacterString>{{ org.city }}</gco:CharacterString>
                                            </gmd:city>
                                            <gmd:administrativeArea>
                                                <gco:CharacterString>{{ org.administrative_area }}</gco:CharacterString>
                                            </gmd:administrativeArea>
                                            <gmd:postalCode>
                                                <gco:CharacterString>{{ org.postal_code }}</gco:CharacterString>
                                            </gmd:postalCode>
                                            <gmd:country>
                                                <gco:CharacterString>{{ org.country }}</gco:CharacterString>
                                            </gmd:country>
                                            <gmd:electronicMailAddress>
                                                <gco:CharacterString>{{ org.email }}</gco:CharacterString>
                                            </gmd:electronicMailAddress>
                                        </gmd:CI_Address>
                                    </gmd:address>
                                    <gmd:onlineResource>
                                        <gmd:CI_OnlineResource>
                                            <gmd:linkage>
                                                <gmd:URL>{{ org.url }}</gmd:URL>
                                            </gmd:linkage>
                                            <gmd:name>
                                                <gco:CharacterString>Marine Institute home page</gco:CharacterString>
                                            </gmd:name>
                                            <gmd:description>
                                                <gco:CharacterString>Marine Institute home page</gco:CharacterString>
                                            </gmd:description>
                                            <gmd:function>
                                                <gmd:CI_OnLineFunctionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="information"/>
                                            </gmd:function>
                                        </gmd:CI_OnlineResource>
                                    </gmd:onlineResource>
                                </gmd:CI_Contact>
                            </gmd:contactInfo>
                            <gmd:role>
                                <gmd:CI_RoleCode codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_RoleCode" codeListValue="originator">originator</gmd:CI_RoleCode>
                            </gmd:role>
                        </gmd:CI_ResponsibleParty>
                    </gmd:pointOfContact>
                    {% endfor %}
                    
                    <!-- Dataset abstract -->
                    
                    <gmd:abstract>
                        <gco:CharacterString>{{ md.base.abstract }}</gco:CharacterString>
                    </gmd:abstract>
                    
                    <!-- Dataset update frequency-->
                    
                    <gmd:resourceMaintenance>
                        <gmd:MD_MaintenanceInformation>
                            <gmd:maintenanceAndUpdateFrequency>
                                <gmd:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode" codeListValue="asNeeded">asNeeded</gmd:MD_MaintenanceFrequencyCode>
                            </gmd:maintenanceAndUpdateFrequency>
                        </gmd:MD_MaintenanceInformation>
                    </gmd:resourceMaintenance>
                
                </gmd:CI_Citation>
            </gmd:citation>
        </gmd:MD_IdentificationInfo>
    </gmd:identificationInfo>
  
</gmd:MD_Metadata>"""