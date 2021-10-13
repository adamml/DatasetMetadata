import datasetmd

def template(md=None):
    """
    Create a list of authors from a :py:class:`datasetmd.DatasetMD`
    instance.
    
    :param md:
    :type md: :py:class:`datasetmd.DatasetMD`, defaults to None
    
    :returns: A dictionary of authors for use in the Schema.org
        template, :py:func:`datasetmd.templates.schemadotorg.template`
    :rtype: dict or None
    """
    
    author_list = []
    
    if md is not None:
        if md.citation is not None:
            if md.citation.authors is not None:
                for auth in md.citation.authors:
                    this_author = {}
                    if isinstance(auth, datasetmd.Person):
                        this_author = {"type": "Person"}
                        if auth.given_name is not None:
                            this_author['givenName'] = auth.given_name
                            this_author['name'] = auth.given_name
                        if auth.family_name is not None:
                            this_author['familyName'] = auth.family_name
                            if auth.name_order == datasetmd.FAMILY_THEN_GIVEN:
                                if auth.given_name is not None:
                                    this_author['name'] = '{0} {1}'.format(auth.family_name, auth.given_name)
                                else:
                                    this_author['name'] = auth.family_name
                            else:
                                if auth.given_name is not None:
                                    this_author['name'] = '{0} {1}'.format(auth.given_name, auth.family_name)
                                else:
                                    this_author['name'] = auth.family_name
                        
                    elif isinstance(auth, datasetmd.Organisation):
                        this_author = {"type": 'Organization'}
                        if auth.name is not None:
                            this_author['name'] = auth.name
                        if auth.website is not None:
                            if auth.website.url is not None:
                                this_author['@id'] = auth.website.url
                                this_author['url'] = auth.website.url
                    if this_author:
                        if this_author not in author_list:
                            author_list.append(this_author)
    
    if not author_list:
        author_list = None
    
    return author_list