==============
Python library
==============

Alongside the QuAAC specification, a Python library is provided to help
read and write files written in the QuAAC format. Examples are given
below for how to perform these operations.


Reading a YAML QuAAC file
--------------------------

The following code snippet shows how to read a YAML QuAAC file into a
Python dictionary:

.. code-block:: python

    import quaac

    with open('example.yaml', 'r') as f:
        quaac_data = quaac.load_spec_file(f)

The ``quaac_data`` variable will now contain a dictionary with all
the data from the QuAAC file that can be referenced, written elsewhere to disk,
loaded into a database, etc.

Writing a YAML QuAAC file
-------------------------

QuAAC files can be written from a Python dictionary using the following:

.. code-block:: python

    import quaac

    with open('example.yaml', 'w') as f:
        quaac.dump_spec_file(quaac_data, f)

This function will also perform validation of the data before writing
to ensure the dictionary format is correct.

