============
Joining data
============

.. important::

  These examples uses the ``quaac`` Python package to create QuAAC files. You can create QuAAC files using any method you like, as long as the resulting file is a valid QuAAC file.

As stated in :ref:`data_models`, a QuAAC document can have any number of data points.
Multiple points can be passed to the :class:`~quaac.models.Document` as items in a list.

.. code-block:: python

    from quaac.models import Document, DataPoint, User, Equipment

    u = User(name="Luis Olivares", email="luis@phys.com")
    e = Equipment(name = "Clinac iX", type="Linac", serial_number="54321", manufacturer="Varian", model="iX")

    d1 = DataPoint(name="symmetry", perform_datetime="2024-07-17", measurement_value=101, measurement_unit="%", performer = user, primary_equipment=e)
    d2 = DataPoint(name="symmetry", perform_datetime="2024-07-18", measurement_value=102, measurement_unit="%", performer = user, primary_equipment=e)
    d3 = DataPoint(name="symmetry", perform_datetime="2024-07-19", measurement_value=99, measurement_unit="%", performer = user, primary_equipment=e)
    doc = Document(version='1.0', datapoints=[d1, d2, d3])
    doc.to_yaml_file('my_qa_data.yaml')

Additionally, the :meth:`~quaac.models.Document.merge` method can be used to join documents together.
This is useful, for example, to record the trend of a measurement over time.

.. code-block:: python
    :emphasize-lines: 11,12

    # Read a previous stored document
    doc = Document.from_yaml_file('my_qa_data.yaml')

    # Create a new data point
    u = User(name="Luis Olivares", email="luis@phys.com")
    e = Equipment(name = "Clinac iX", type="Linac", serial_number="54321", manufacturer="Varian", model="iX")
    dp2 = DataPoint(name="symmetry", perform_datetime="2024-07-20", measurement_value=99.5, measurement_unit="%", performer = user, primary_equipment=e)
    doc2 = Document(version='1.0', datapoints=[dp2])

    # Merge the two documents and save
    new_doc = doc.merge([doc2])
    new_doc.to_yaml_file('my_qa_data.yaml')

Filtering
---------

A QuAAC document can contain any kind of measurement not necessarily related to each other.
A simple Python function can be used to filter data points, for example, using the ``name`` attribute.

.. code-block:: python

    from quaac.models import Document, DataPoint

    # Define a function to get the points by name
    def get_points_by_name(doc: Document, name: str) -> list[DataPoint]:
        return [dp for dp in doc.datapoints if dp.name == name]

    # Load a document
    doc = Document.from_yaml_file('my_qa_data.yaml')

    # Get the data points with name 'symmetry'
    points = get_points_by_name(doc, 'symmetry')

    measurements = [p.measurement_value for p in points]
    date = [p.perform_datetime for p in points]

Plot the data

.. code-block:: python

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    fig, ax = plt.subplots()

    ax.plot(date, measurements, "g+", markersize=15, mew=2)

    # Show reference and tolerance lines
    ax.axhline(103, linestyle = "--", linewidth = 3, color = "r", alpha = 0.7)
    ax.axhline(97, linestyle = "--", linewidth = 3, color = "r", alpha = 0.7)
    ax.axhline(100, linestyle = "--", linewidth = 3, color = "g", alpha = 0.7)
    ax.grid(which="both")

    # Format the date on the x-axis
    locator = mdates.AutoDateLocator(maxticks=7)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    