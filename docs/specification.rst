=============
Specification
=============

This is the field specification for QuAACS.

Field Types
===========

The following field types are defined:

* String
* Integer
* Float
* Boolean
* Date
* Time
* Array

Primary Fields
==============

``version``
-----------

(**String**). The version of the QuAAC specification.

``data points``
---------------

(**Array[DataPoints]**). The individual QA data points. See :ref:`data-point`.

``equipment``
-------------

(**Array[Equipment]**). The equipment referenced by the data points. See :ref:`equipment`.

``users``
---------

(**Array[User]**). The users referenced by the data points. See :ref:`users`.

``files``
---------

(**Array[File]**). The supporting files referenced by the data points. See :ref:`file`.


.. _data-point:

Data Point
==========

The following fields are defined for a data point:

``name``
--------

(**String**, Required). The name of the data point. Usually this is the name of the QA test. E.g. "Output 6 MV".

``performer``
-------------

(**String**, Required). The name of the person who performed the QA test.

``date``
--------

(**Date**, Required). The date the QA test was performed.

``measurement value``
---------------------

(**Float**, Required). The measurement value of the QA test.

``measurement unit``
-------------------

(**String**, Required). The measurement unit of the QA test.

``measurement type``
-------------------

(**String**, Required). The measurement type of the QA test.

``description``
---------------

(**String**, Optional). A description of the QA test.

``primary equipment``
--------------------

(**String**, Required). The name of the primary equipment used to perform the QA test.

``ancillary equipment``
----------------------

(**Array[String]**, Optional). The names of the ancillary equipment used to perform the QA test.

``files``
---------

(**Array[String]**, Optional). The names of the files used to perform the QA test.

``comments``
------------

(**String**, Optional). Comments about the QA test.

``procedure``
-------------

(**String**, Optional). The procedure used to perform the QA test.

``reference``
-------------

(**String**, Optional). The reference used to perform the QA test.

``review status``
-----------------

(**String**, Optional). The review status of the QA test.

``review date``
---------------

(**Date**, Optional). The date the QA test was reviewed.

``reviewer name``
-----------------

(**String**, Optional). The name of the person who reviewed the QA test.

``reviewer id``
---------------

(**String**, Optional). The ID of the person who reviewed the QA test.

``reviewer comments``
---------------------

(**String**, Optional). Comments about the review of the QA test.

``parameters``
--------------

(**Array[Any]**, Optional). The parameters of the QA test. See :ref:`parameter`.

.. _parameter:

Parameter
=========

Parameters are an optional and free-form key-value store. These are
relevant parameters that related to either how the QA test was performed
or how the data was performed, processed, or acquired.

Examples include:

* energy
* field size
* gantry angle
* collimator angle
* MU
* SSD
* Processing algorithm
* Etc.

There is no limit to parameters and are encouraged for specificity.

.. _equipment:

Equipment
=========

``name``
--------

(**String**, Required). The name of the equipment.

``type``
--------

(**String**, Required). The type of the equipment.

``serial number``
-----------------

(**String**, Required). The serial number of the equipment.

``model``
---------

(**String**, Optional). The model of the equipment.

``manufacturer``
----------------

(**String**, Optional). The manufacturer of the equipment.

.. _user:

User
====

``name``
--------

(**String**, Required). The name of the user. Should be the full name. Can contain spaces.

``email``
---------

(**String**, Required). The email of the user.

``id``
------

(**String**, Optional). The ID of the user. This could be a username, employee ID, etc.

.. _file:

File
====

``name``
--------

(**String**, Required). The name of the file.

``type``
--------

(**String**, Required). The type of the file. This is a `MIME <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types>`__ type.

Purpose: Assist in reading the file correctly. E.g. ``image/png`` refers to a PNG image. The content itself
may or may not be obvious.

``compression``
---------------

(**String**, Required). The compression algorithm used to compress the file.

Must be one of:

* ``gzip``

``encoding``
------------

(**String**, Required). The encoding of the file.

Must be one of:

* ``base64``

``content``
-----------

(**String**, Required). The content of the file encoded as a string.
