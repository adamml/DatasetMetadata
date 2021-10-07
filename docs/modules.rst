API Documentation
=================

.. toctree::
   :maxdepth: 3

.. graphviz::

   digraph foo {
      "datasetmd.DatasetMD" -> "datasetmd.Citation";
	  "datasetmd.DatasetMD" -> "datasetmd.Feature";
	  "datasetmd.DatasetMD" -> "datasetmd.Organisation";
	  "datasetmd.Organisation" -> "datasetmd.WebAddress";
   }

datasetmd
---------

.. automodule:: datasetmd
    :members:
    :undoc-members:
    :show-inheritance:
	
datasetmd.templates.iso19139
----------------------------

.. automodule:: datasetmd.templates.iso19139
    :members:
    :undoc-members:
    :show-inheritance: