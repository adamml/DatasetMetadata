Installation
============

Requirements
------------

DatasetMD is written in `Python <https://www.python.org>`_, and works with Python 3. Python 2 is not supported.

DatasetMD additionally requires the following Python supporting libraries:

* `Jinja2 <https://pypi.org/project/Jinja2/>`_ for templating the various serialisations of dataset metadata

Additional Development Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Sphinx <https://pypi.org/project/Sphinx/>`_ for creating documentation webpages
* `sphinx-rtd-theme <https://pypi.org/project/sphinx-rtd-theme/>`_ for styling the documentation

Install
-------

From GitHub
^^^^^^^^^^^

.. code-block:: bash
   :linenos:
   
   git clone git://github.com/adamml/DatasetMD.git
   cd DatasetMD
   python -m build
   python -m install
   