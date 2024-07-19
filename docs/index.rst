.. QuAAC documentation master file, created by
   sphinx-quickstart on Fri Jan 19 14:13:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to QuAAC's documentation!
=================================

===========
About QuAAC
===========

Intent
------

The Quality Assurance Archive & Communication (QuAAC) project is a standardization effort for the
storage and exchange of routine quality assurance data that spans vendors and
inter-clinical sites.

Rationale
---------

The QuAAC project was born out of the need to store and exchange routine QA data
in a vendor- and clinic-neutral format. Clinics that move between commercial vendors of QA
equipment and software are often faced with the challenge of converting their
data from one paradigm to another, depending on the vendor. This can also
happen when migrating from a in-house solution to a commercial solution.
There currently exists no reasonable standard for the storage and exchange of
this QA data. The QuAAC project aims to fill this gap.

Philosophy
----------

#. The QuAAC project is a community effort.
#. The QuAAC project is a living standard and will evolve as use cases are identified and addressed.
#. QuAAC is meant to store both "interpreted" data as well as raw data.
#. Raw data (e.g. PDFs, DICOM, spreadsheets) is expected and encouraged to be linked with the interpreted data.
#. The QuAAC project is not a replacement for DICOM.
#. Data should be stored in a format that is easily parsed by humans or machines [#]_.
#. QuAAC is not a QA platform.
#. QuAAC is not meant for patient data.
#. QuAAC is vendor- and clinic-neutral.

.. [#]

   This does not mean all data is simple text, but rather that any of the supported formats should be easily parsed
   by tools commonly and freely available to the larger community.


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
no easier than using simple file formats. Finally, there is plenty of
QA data that is not image or naturally file-based.

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
performance. Raw data is intermediate data that is used to generate QA data but is not itself the evaluation.
For example, a profile scan is raw data, but the flatness and symmetry values
are QA data. Although critical in many cases to generate the QA data, the raw
data itself is not QA data.

Why use it?
-----------

Reasons to use QuAAC include:

* Standardization of QA data storage
* Easy to implement
* Vendor-neutral storage
* Easy to parse and read
* clinic-to-clinic communication compatibility
* Vendor switchover compatibility



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   data_models
   formats
   library
   reading_quaac
   writing_quaac
   joining_quaac



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
