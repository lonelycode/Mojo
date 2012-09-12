Mojo.ObjectMapper
=================

The Mojo object mapper is not strictly database-bound ORM, the purpose of the ORM is to offer data integrity and validation
as part of the data solution. As Mojo is mainly built around MongoDB (for now), the models offer a way to ensure some consistency
in a schemaless database.

The Object Mapper defines two main things: ``Fields`` that can be used to set up validation rules on data types and ``Models``,
collections of fields that will validate all of their containing fields and map to dictionaries under the hood.

``Models`` come with multiple database functions (``save``, ``find``, ``find_one``, ``delete``, ``delete_bulk``) that also have asynchronous variants
(``save_async``, ``find_async``, ``find_one_async``, ``delete_async``, ``delete_bulk_async``) that need to be called depending on the underlying
database back-end that has been chosen.


Base Field Type
---------------

This is the base field type that all others inherit from, it can be subclassed to create custom model fields to
extend your models.

..  automodule:: Mojo.ObjectMapper.FieldPrototype
    :members:

Default Mojo Field Types
------------------------

These fields are the default field types that come with Mojo and are used throughout the framework.

..  automodule:: Mojo.ObjectMapper.Fields
    :members:

..  autoclass:: Mojo.ObjectMapper.ModelPrototype.EmbeddedModelField
    :members:

Models
------

``Models`` represent collections of ``Fields``, and are subclasses of ``dict``, so are easy to implement into Mongo-style queries
which use BSON-style data structures.

..  autoclass:: Mojo.ObjectMapper.ModelPrototype.Model
    :members:
