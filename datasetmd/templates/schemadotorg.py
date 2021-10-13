def template():
    """
    This class provides a  Jinja2 template for creating an Schema.org record
    as JSON-LD from a DatasetMD object. The template follows the guidelines
    from the Earth Science Informatics Partnership's Science on Schema project.
    
    :return:
    :rtype: str
    """
    return """{
    "@context": {
        "@vocab": "https://schema.org/"
    },
    "@type": "Dataset",
    "name": "{{ md.base.title }}",
    "description": "{{ md.base.abstract | truncate(5000) }}",
    "version": "{{ md.base.modified }}"{%if md.keywords is not none%},
    "keywords": [{% for kw in md.keywords%}{% if loop.index > 1 %}, {% endif %}"{{ kw.title }}"{% endfor %}]{%endif%}{% if md.citation.short_doi is not none %},
    "sameAs": "https://doi.org/{{ md.citation.short_doi }}"{% endif %}{% if md.citation.doi is not none %},
    "identifier": {
        "@id": "https://doi.org/{{ md.citation.doi }}",
        "@type": "PropertyValue",
        "propertyID": {"@id": "https://registry.identifiers.org/registry/doi"},
        "value": "doi:{{ md.citation.doi }}",
        "url": "https://doi.org/{{ md.citation.doi }}"
    }{% endif %}{% if md.observed_properties is not none %},
    "variableMeasured":  [{% for obsprop in md.observed_properties %}
        {% if loop.index > 1 %}, {% endif %}{
            "@type": "PropertyValue"{% if obsprop.title is not none %},
            "name": "{{ obsprop.title }}"{% endif %}{% if obsprop.url is not none %},
            "propertyID": {"@id": "{{ obsprop.url }}"}{% endif %}
        }{% endfor %}
    ] {% endif %}
    {% if md.license is not none %}{% if md.license.spdx_url is not none %}{% if md.license.spdx_url.url is not none %}{% if md.license.url is not none %}{% if md.license.url.url is not none %}, "license": ["{{ md.license.spdx_url.url }}", "{{ md.license.url.url }}"]{%  else %}, "license": "{{ md.license.spdx_url.url }}" {% endif %}{% endif%}{% endif %}{% elif md.license.url is not none %}{% if md.license.url.url is not none %}, "license": "{{ md.license.url.url }}"{% endif %}{% endif %}{% else %}{% if md.license.name is not none %}, "license": "{{ md.license.name }}"{% endif %}{% endif %}{% if md.included_in_data_catalogue is not none %}{% if md.included_in_data_catalogue.url is not none %},
    "includedInDataCatalog": {
        "@id": "{{ md.included_in_data_catalogue.url }}",
        "@type": "DataCatalog"
    }{% endif %}{% endif %}{% if citation_string is not none %}, "citation": "{{ citation_string }}"{% endif %}{% if authors is not none %},
    "creator": [{% for cre in authors %}
        {% if loop.index > 1 %}, {% endif %}{
            "@type": "{{ cre.type }}"{% if cre.name is not none %},
            "name": "{{ cre.name }}"{% endif %}{% if cre.familyName is not none %},
            "familyName": "{{ cre.familyName }}"{% endif %}{% if cre.givenName is not none %},
            "givenName": "{{ cre.givenName }}"{% endif %}
        }{% endfor %}
    ]{% endif %}{% if md.publisher is not none %},
    "publisher": {
        "@type": "Organization"{% if md.publisher.website is not none %}{% if md.publisher.website.url is not none %},
        "@id": "{{ md.publisher.website.url }}"{% endif %}{% endif %}{% if md.publisher.name is not none %},
        "name": "{{ md.publisher.name }}"{% endif %}{% if md.publisher.country is not none %},
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "{{ md.publisher.country }}"
        }{% endif %}
    }{% endif %}{% if md.owning_organisations is not none %},
    "provider": [
        {% for org in md.owning_organisations %}{% if loop.index > 1 %}, {% endif %}{
            "@type": "Organization"{% if org.website is not none %}{% if org.website.url is not none %},
            "@id": "{{ org.website.url }}"{% endif %}{% endif %}{% if org.name is not none %},
            "name": "{{ org.name }}"{% endif %}{% if org.country is not none %},
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "{{ org.country }}"
        }{% endif %}
        }{% endfor %}
    ]{% endif %}
}"""