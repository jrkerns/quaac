===================
Writing QuAAC files
===================

.. important::

  This example uses the ``quaac`` Python package to create QuAAC files. You can create QuAAC files using any method you like, as long as the resulting file is a valid QuAAC file.


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

As stated in :ref:`data_models`, a QuAAC document can have any number of datapoints.
Multiple points can be given to the :class:`~quaac.models.Document` object as items in a list
at the time of document creation.

.. code-block:: python

    d1 = DataPoint(...) # d2 and d3 are similar
    doc = Document(version='1.0', datapoints=[d1, d2, d3])
    doc.to_yaml_file('my_qa_data.yaml')

Additionally, the :meth:`~quaac.models.Document.merge` method can be used to join two documents together.
This is useful for example to record the tendendy of a measurement over time.

.. code-block:: python

    # Read a previous stored document
    doc = Document.from_yaml_file('qa_data.yaml')

    # Create a new data point and document
    d2 = DataPoint(name="DP", perform_datetime=datetime.datetime.now(), measurement_value=4, measurement_unit="cGy", performer=u, primary_equipment=e, ancillary_equipment=[e], attachments=[a], reviewer=u, parameters={'field size': '10x10cm', 'ssd': '100cm'})
    doc2 = Document(version='1.0', datapoints=[d2])

    # Merge the two documents and save
    new_doc = doc.merge([doc2])
    new_doc.to_yaml_file('my_qa_data.yaml')

A QuAAC document does not necesarly has to have related kind of
measurements. A simple python fuction can be used to filter data points
using the `name` attribute.

.. code-block:: python

    # Define a function to get the points by name attribute
    def get_points_by_name(doc, name: str):
        return [dp for dp in doc.datapoints if dp.name == name]

    # Read a previous stored document
    doc = Document.from_yaml_file('qa_data.yaml')

    # Get the data points by name
    points = get_points_by_name(doc, 'DP')
    measurements = [dp.measurement_value for dp in points]
    date = [dp.perform_datetime for dp in points]

Plot the data

.. code-block:: python

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    fig, ax = plt.subplots()
    ax.plot(date, measurements)
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    