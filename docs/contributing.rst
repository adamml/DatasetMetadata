Contributing
============

New output formats
------------------

Each output format consists of a Python file in the `datasetmd/templates`
directory. For example, the ISO19139 XML output format is defined in
`iso19139.py`.

To add a new output format, create the Python file in the correct
directory, and add it to both the import list and the `__all__` directive
of the `datasetmd/templates/__init__.py` file. This will ensure that your 
output format is available to the main :py:class:`datasetmd` module.

Each Python file in `datasetmd/templates` must describe exactly one function, 
named `template`, for example :py:func:`datasetmd.templates.iso19139.template`. This function may:

* take zero arguments and return as a `str` a Jinja2 template which can be rendered against a class defined in the :py:class:`datasetmd` module, e.g. :py:func:`datasetmd.templates.iso19139.template`.
* or take exactly on argument, a :py:class:`datasetmd.DatasetMD` object, and return as a `str` or a mapping object some output based on the attributes of the object, e.g. :py:func:`datasetmd.templates.citationstring.template` or :py:func:`datasetmd.templates.schemadotorg_creatorlist.template`.

For example, the declarations of

If there is nothing to return from the `template` function, or the response 
would be empty, the function must return a `None` value.

A method invoking the template must be added to the relevant class in :py:class:`datasetmd`,
unless the new output format is for a new citation type, in which case the
:py:meth:`datasetmd.DatasetMD.cite` method must be extended appropriately.