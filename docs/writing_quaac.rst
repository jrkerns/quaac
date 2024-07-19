===================
Writing QuAAC files
===================

.. important::

  The next examples uses the ``quaac`` Python package to create QuAAC files. You can create QuAAC files using any method you like, as long as the resulting file is a valid QuAAC file.


Creating instances of QuAAC data
---------------------------------

Assuming you are using the ``quaac`` package, you can create a QuAAC file by creating a :class:`~quaac.models.Document` object and adding the required data to it.

.. code-block:: python

  import datetime
  from pathlib import Path

  from quaac.models import Document, DataPoint, User, Equipment, Attachment

  a = Attachment.from_file(Path(r"C:\path\to\screenshot.png"))
  e = Equipment(name="TrueBeam 1", type="Linac", serial_number="12345", manufacturer="Varian", model="TrueBeam")
  u = User(name="John Doe", email="john@doe.com")
  d = DataPoint(name="DP", perform_datetime=datetime.datetime.now(), measurement_value=3, measurement_unit="cGy", performer=u, primary_equipment=e, ancillary_equipment=[e], attachments=[a], reviewer=u, parameters={'field size': '10x10cm', 'ssd': '100cm'})
  doc = Document(version='1.0', datapoints=[d])

Above, we have created an attachment, which is any binary file that is associated with the data point. We can load straight from disk.
We have also created an equipment object, which represents the equipment used to perform the measurement.
We have also created a user object, which represents the person who performed and (optionally) reviewed the measurement.
Finally, we have created a data point object, which represents the measurement itself which references the equipment, user, and attachment.
We then create a document object and add the data point to it.

Writing a QuAAC file
--------------------

QuAAC files can be written to disk using the ``quaac`` library. Continuing from the previous example, we can write the document to a file like so:

.. code-block:: python

    doc = Document(...)  # from above

    doc.to_json_file('my_qa_data.json')
    doc.to_yaml_file('my_qa_data.yaml')

These methods will also perform validation of the data before writing
to ensure the format is correct.

Joining data
------------

As stated in :ref:`data_models`, a QuAAC document can have any number of data points.
Multiple points can be passed to the :class:`~quaac.models.Document` as items in a list.

.. code-block:: python

    d1 = DataPoint(...) # d2 and d3 are similar
    doc = Document(version='1.0', datapoints=[d1, d2, d3])
    doc.to_yaml_file('my_qa_data.yaml')

Additionally, the :meth:`~quaac.models.Document.merge` method can be used to join two documents together.
This is useful, for example, to record the trend of a measurement over time.

.. code-block:: python
    :emphasize-lines: 9,10

    # Read a previous stored document
    doc = Document.from_yaml_file('my_qa_data.yaml')

    # Create a new data point
    d4 = DataPoint(name="DP", perform_datetime=datetime.datetime.now(), measurement_value=4, ...)
    doc4 = Document(version='1.0', datapoints=[d4])

    # Merge the two documents and save
    new_doc = doc.merge([doc4])
    new_doc.to_yaml_file('my_qa_data.yaml')

A QuAAC document can contain any kind of measurement not necessarily related to each other.
A simple Python function can be used to filter data points, for example, using the ``name`` attribute.

.. code-block:: python

    from quaac.models import Document

    # Define a function to get the points by name
    def get_points_by_name(doc: Document, name: str) -> list[DataPoint]:
        return [dp for dp in doc.datapoints if dp.name == name]

    # Load a document
    doc = Document.from_yaml_file('my_qa_data.yaml')

    # Get the data points with name 'DP'
    points = get_points_by_name(doc, 'DP')
    
    measurement = [p.measurement_value for p in points]
    date = [p.perform_datetime for p in points]

Plot the data

.. code-block:: python

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    fig, ax = plt.subplots()

    ax.plot(date, measurement)
    
    # Format the date on the x-axis
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    