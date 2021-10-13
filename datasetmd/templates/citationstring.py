import datasetmd

def template(md=None):
    """This function creates a suggested citation string for a DatasetMD
    object.
    
    :param md:
    :type md: DatasetMD, defaults to None
    
    :rtype: str, or None
    """
    ret_string = ""
    author_count = 0
    affiliation_list = []
    if md is not None:
        if md.citation is not None:
            if md.citation.authors is not None:
                for author in md.citation.authors:
                    if author_count > 0:
                        ret_string += '; '
                    if isinstance(author, datasetmd.Person):
                        if author.family_name is None:
                            ret_string += '{}'.format(author.given_name)
                            author_count += 1
                        elif author.given_name is None:
                            ret_string += '{}'.format(author.family_name)
                            author_count += 1
                        else:
                            ret_string += '{0}, {1}'.format(author.family_name, 
                                                                author.given_name)
                            author_count += 1
                        if author.affiliation is not None:
                            affiliation_count = 0
                            for affiliation in author.affiliation:
                                if affiliation.name is not None:
                                    if affiliation.country is not None:
                                        citation_affiliation = '{0}, {1}'.format(affiliation.name, 
                                                                    affiliation.country)
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
                    elif isinstance(author, datasetmd.Organisation):
                        if author.name is not None:
                            ret_string += '{}'.format(author.name)
                            if author.country is not None:
                                citation_affiliation = '{0}, {1}'.format(author.name, 
                                                                    author.country)
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
            if md.citation.doi_publication_date is not None:
                ret_string += '({})'.format(md.citation.doi_publication_date.year)
            if ret_string:
                ret_string = '{}. '.format(ret_string)
            if md.base.title is not None:
                ret_string += '{}'.format(md.base.title)
            if ret_string:
                ret_string = '{}. '.format(ret_string)
            if md.citation.doi_publisher is not None:
                if md.citation.doi_publisher.name is not None:
                    if md.citation.doi_publisher.country is not None:
                        ret_string += '{}, {}'.format(md.citation.doi_publisher.name, 
                                                md.citation.doi_publisher.country)
                    else:
                        ret_string += '{}'.format(md.citation.doi_publisher.name)
            if ret_string:
                ret_string = '{}. '.format(ret_string)
            if md.citation.prefer_short_doi:
                if md.citation.short_doi is not None:
                    ret_string += 'doi: {}'.format(md.citation.short_doi)
                elif md.citation.doi is not None:
                    ret_string += 'doi: {}'.format(md.citation.doi)
            else:
                if md.citation.doi is not None:
                    ret_string += 'doi: {}'.format(md.citation.doi)
                elif md.citation.short_doi is not None:
                    ret_string += 'doi: {}'.format(md.citation.short_doi)
            if ret_string:
                ret_string = '{}. '.format(ret_string)
            if affiliation_list:
                affiliation_count = 1
                for affiliation in affiliation_list:
                    ret_string += '({0}) {1}. '.format(affiliation_count, 
                                                                affiliation)
                    affiliation_count += 1
    ret_string = ret_string.strip()
    if not ret_string:
        ret_string = None
    return ret_string