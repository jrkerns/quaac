===========
Data Models
===========

The QuAAC specification has 4 data models:

* User
* Equipment
* Files
* Data Points

Each of these models represent one of the main components in a QA workflow.
The following flowchart shows how these models are related to each other:

.. image:: QuAAC_models.png
   :align: center
   :alt: QuAAC Data Models

Following the flowchart, the data models are described in detail below.

A piece of equipment generates some form of data. Other equipment could be used
to measure such data or to process it. Sometimes, the data is saved to a file
to be processed by other ancillary equipment. This data is performed by a user
and, ideally, is reviewed by a user.

