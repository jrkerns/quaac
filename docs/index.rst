.. QuAAC documentation master file, created by
   sphinx-quickstart on Fri Jan 19 14:13:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to QuAAC's documentation!
=================================



Serialization Formats
---------------------

The QuAAC project defines two serialization formats: YAML and SQLite.

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

   about
   data_models
   formats
   reading_quaac
   writing_quaac




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
