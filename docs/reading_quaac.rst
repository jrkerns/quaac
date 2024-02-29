=============
Reading QuAAC
=============

A QuAAC document is a record of QA data and can be written in
different :ref:`formats`. These formats are meant to be human-readable.
Even without a library, you can often read the data in a text editor.
This is useful for transparency, debugging, and being language-agnostic.
That being said, a QuAAC library is provided to help read and write
these files in a programmatic way. See :ref:`library`.


Reading a YAML QuAAC file
--------------------------

The following code snippet shows how to read a YAML QuAAC file into a
Python dictionary. Assume we have a file called ``qa_data.yaml`` with the
following content. This represents a single QA datapoint on a TrueBeam
using a CatPhan 504 phantom.

.. code-block:: yaml
  :caption: qa_data.yaml

  version: '1'
  datapoints:
  - name: Center Uniformity
    perform datetime: '2024-02-20T14:48:33.894431'
    measurement_value: 38
    measurement_unit: HU
    reference_value: 40
    description: ''
    procedure: ''
    performer: 00a5823df7e34298664b8ee8a79e43b2
    performer_comment: ''
    primary_equipment: 5e766755c7692fd477a61f24e8c896ad
    reviewer: 00a5823df7e34298664b8ee8a79e43b2
    parameters:
      kVp: 120
      mAs: 20
    ancillary_equipment:
    - ce820ce095b7937449ed3105d0261283
    attachments: []
    hash: 558f83e110647c2c945a26a22a735dc7
  hash: 4a52df5e9cc5d6ce651eb9e3066b5ea4
  equipment:
  - name: TrueBeam 1
    type: Linac
    serial_number: '12345'
    manufacturer: Varian
    model: TrueBeam
    hash: 5e766755c7692fd477a61f24e8c896ad
  - name: CatPhan 504
    type: Phantom
    serial_number: A4321
    manufacturer: Image Laboratory
    model: '504'
    hash: ce820ce095b7937449ed3105d0261283
  users:
  - name: John Doe
    email: john@clinic.com
    hash: 00a5823df7e34298664b8ee8a79e43b2
  attachments: []

We can then load that file like so:

.. code-block:: python

    from quaac import Document

    doc = Document.from_yaml_file('qa_data.yaml')

The ``quaac_data`` variable will now contain a dictionary with all
the data from the QuAAC file that can be referenced, written elsewhere to disk,
loaded into a database, etc.


