.. QuACS documentation master file, created by
   sphinx-quickstart on Fri Jan 19 14:13:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to QuACS's documentation!
=================================

Intent
------

The Quality Assurance and Archiving Communication Standard (QuAACS) project is a standardization effort for the
storage and exchange of routine quality assurance data that spans vendors and
inter-clinical sites.

Rationale
---------

The QuACS project was born out of the need to store and exchange routine QA data
in a vendor-neutral format. Clinics that move between commercial vendors of QA
equipment and software are often faced with the challenge of converting their
data from one paradigm to another, depending on the vendor. This can also
happen when migrating from a in-house solution to a commercial solution.
There currently exists no reasonable standard for the storage and exchange of
this QA data. The QuACS project aims to fill this gap.

Philosophy
----------

#. The QuACS project is a community effort.
#. The QuACS project is a living standard and will evolve as use cases are identified and addressed.
#. QuACS is meant to store both "interpreted" data as well as raw data.
#. Raw data is expected and encouraged to be linked with the interpreted data.
#. The QuACS project is not a replacement for DICOM, but rather a complement.
#. Data is stored in a format that is easily parsed by humans and machines.
#. QuACS is not a QA platform.
#. QuACS is not meant for patient data.


Comparison with DICOM
---------------------

The advent of the DICOM standard has been a boon to the medical imaging
community. It has allowed for the exchange of medical images and metadata
between vendors and clinical sites. However, QA data is a niche
area that involves more than just images and metadata. There is often extra
data associated with QA data that doesn't fit into standard DICOM fields.
Further, this project does not define a standard for the **exchange** of QA data.
Per philosophy #6, any QuAACS archive is readable by humans and machines. By
keeping the format simple, it is easy to parse and extract data from a QuAACS
using commonly-available software tools.

Compared to DICOM, the scope is significantly smaller, both in terms of the
addressed needs as well as the number of definitions. QA data is diverse,
but DICOM has a much larger scope.

Why not use private DICOM tags?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Private DICOM tags are a great way to store extra data in a DICOM file.
However, they are not standardized and are not guaranteed to be readable
by other vendors. Further, parsing the data from a private DICOM tag is
no easier than using simple file formats.

Examples of QA data
-------------------

* Daily high-dose rate afterloader timing check
* Machine Performance Check MLC bank A max error
* Cone-beam CT uniformity
* Planar MV contrast
* An ion chamber reading
* Flatness and symmetry from a water tank profile scan

.. important::

   These are individual data points, usually part of a larger dataset. A "daily QA"
   usually involves a number of these data points. Also note that these data points
   might be based on raw data, such as a profile scan or DICOM images.

QA data vs raw data
^^^^^^^^^^^^^^^^^^^

We make an important distinction between QA data and raw data. QA data is
either raw or interpreted data, useful for the evaluation of a machine's
performance. Raw data is intermediate data that is used to generate QA data.
For example, a profile scan is raw data, but the flatness and symmetry values
are QA data. Although critical in many cases to generate the QA data, the raw
data itself is not QA data.

Serialization Formats
---------------------

The QuACS project defines two serialization formats: YAML and SQLite.

Yet another markup language (`YAML <https://en.wikipedia.org/wiki/YAML>`__) is a human-readable file
format and most programming languages can easily read and write to YAML.

SQLite is a relational database that is commonly used in software applications.
It is unique in that it is contained within a single file. It can hold
many types of data including images and text. Although it is not human-readable
in its raw form, many programming languages have libraries to read and write
to SQLite databases and many open-source and freely-available applications
exist to view and edit SQLite databases.


SQLite Applications
-------------------

The following are free applications that can be used to view and edit SQLite:

* `DB Browser for SQLite <https://sqlitebrowser.org/>`__
* `SQLiteStudio <https://sqlitestudio.pl/>`__

YAML Libraries
--------------

The following are free libraries that can be used to read and write YAML:

* Python: `PyYAML <https://pyyaml.org/>`__
* C#: `YamlDotNet <https://github.com/aaubry/YamlDotNet>`__
* Javascript: `yaml <https://github.com/eemeli/yaml>`__

Many other exist. The point is that YAML is easily usable for most programming
languages.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   specification
   data_models
   python_library




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
