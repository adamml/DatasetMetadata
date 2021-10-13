API Documentation
=================

.. toctree::
   :maxdepth: 3

.. graphviz::

   digraph foo {
      "datasetmd.DatasetMD" -> "datasetmd.Citation" [label="citation"];
	  "datasetmd.DatasetMD" -> "datasetmd.Feature" [label="feature"];
	  "datasetmd.DatasetMD" -> "datasetmd.Organisation" [label="owning_organisations, publisher"];
	  "datasetmd.DatasetMD" -> "datasetmd.ObservedProperty" [label="observed_properties"];
	  "datasetmd.DatasetMD" -> "datasetmd.DefinedTerm" [label="keywords"];
	  "datasetmd.DefinedTerm" -> "datasetmd.DefinedTermSet" [label="in_defined_term_set"];
	  "datasetmd.Organisation" -> "datasetmd.WebAddress" [label="website"];
	  "datasetmd.Citation" -> "datasetmd.Organisation" [label="authors, doi_publisher"];
	  "datasetmd.Citation" -> "datasetmd.Person" [label="authors"];
	  "datasetmd.Person" -> "datasetmd.Organisation" [label="affiliation"];
	  "datasetmd.DefinedTerm" -> "datasetmd.WebAddress" [label="is sub class of", style="dashed"];
	  "datasetmd.ObservedProperty" -> "datasetmd.DefinedTerm" [label="is sub class of", style="dashed"];
	  "datasetmd.DefinedTermSet" -> "datasetmd.WebAddress" [label="is sub class of", style="dashed"];
	  "datasetmd.ObservedProperty" -> "datasetmd.DefinedTermSet" [label="in_defined_term_set"];
	  "datasetmd.DatasetMD" -> "datasetmd.License" [label="license"];
	  "datasetmd.License" -> "datasetmd.DefinedTermSet" [label="in_defined_term_set"];
	  "datasetmd.DatasetMD" -> "datasetmd.CrossReference" [label="cross_references"];
	  "datasetmd.CrossReference" -> "datasetmd.WebAddress" [label="is sub class of", style="dashed"];
	  "datasetmd.DatasetMD" -> "datasetmd.WebAddress" [label="included_in_data_catalogue"];
	  "datasetmd.DatasetMD" -> "datasetmd.Limitations" [label="limitations"];
   }

datasetmd
---------

.. automodule:: datasetmd
    :members:
    :undoc-members:
    :show-inheritance:
	
datasetmd.templates
-------------------

.. automodule:: datasetmd.templates.citationstring
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: datasetmd.templates.iso19139
    :members:
    :undoc-members:
    :show-inheritance:
	
.. automodule:: datasetmd.templates.schemadotorg
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: datasetmd.templates.schemadotorg_creatorlist
    :members:
    :undoc-members:
    :show-inheritance: