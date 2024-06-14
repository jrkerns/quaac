.. _library:

==============
Python Library
==============

The QuAAC project includes a Python library that can be used to interact with
YAML and JSON QuAAC documents. It is not required to use the library to interact with QuAAC documents, but it can be useful for
reading and writing QuAAC documents.

Installation
------------

To install the ``quaac`` package, you must have Python installed. If you do not have Python installed, you can download it from
`Python's website <https://www.python.org/downloads/>`_.

Once you have Python installed, you can install the ``quaac`` package using pip. Open a terminal and run the following command:

.. code-block:: bash

    pip install quaac


Versioning
----------

The Python library uses semantic versioning and the major and minor versions will always be versioned to match the QuAAC version it
will process. The patch version will be incremented for bug fixes and minor changes.
E.g. QuAAC specification 1.0.0 will be processed by the Python library 1.0.x versions.

Model API
---------

.. automodule:: quaac.models
    :members:
    :show-inheritance:
    :exclude-members: model_computed_fields, serialize_performer, serialize_attachments, serialize_reviewer, serialize_primary_equipment, serialize_ancillary_equipment

Attachment Options API
----------------------

.. autoclass:: quaac.attachments.Compression
    :members:

.. autoclass:: quaac.attachments.Encoding
    :members:

