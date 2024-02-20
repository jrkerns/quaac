


Writing a YAML QuAAC file
-------------------------

QuAAC files can be written from a Python dictionary using the following:

.. code-block:: python

    import quaac

    with open('example.yaml', 'w') as f:
        quaac.dump_spec_file(quaac_data, f)

This function will also perform validation of the data before writing
to ensure the dictionary format is correct.