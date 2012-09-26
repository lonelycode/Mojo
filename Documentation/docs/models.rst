The Mojo ORM and Models
=======================

To make working with databases easier, and to ensure a consistent set of tools when saving and moving data, Mojo
uses models to define validation and data structures, and then uses these to set up how data will look in the database.

Currently, Mojo only supports MongoDB, but we are hoping to add support for Redis and CouchDB soon. We actively encourage
contributors, so anyone feeling the urge to help us write a new backend for their favourite datastore can drop us a line
in our Google Group.

What are Models?
----------------

For anyone familiar with Django, Mojo Models will seem very similar, and take heavy influence from the framework. Models
are a way for you to organise and structure your data as python objects so you can transparently use them (without a
data store) in your application.

Models are very simple - they are a defined class, with a series of fields that you can use to represent your data and the
various validation methods you would like run against those fields before the object is written to the database.

Why Models?
-----------

Because our first database to support was MongoDB, it became apparent that what was really missing was a good way to
enforce structure and a certain degree of validation on stored data. Being Schema-less, it becomes very easy to not
validate stored input due to the extra burden of writing the validation code, as well as not manging schema evolutions
as schemas change over the lifecycle of your project.

Models make this process easiewr by pre-defining data types, relations and object properties prior to saving, while exposing
all the benefits of having a neat python object to represent your data set without resporting to direct database access.

Do I have to use Models?
------------------------

Not at all, you can completely ignore the ORM and model structure in your project and directly access your database using your
favourite driver.

Using Models
============

To implement a model for your app, simply define it in the ``models.py`` file in your app directory::

    from Mojo.ObjectMapper.ModelPrototype import Model
    from Mojo.ObjectMapper.Fields import *
    import datetime

    #This is a non-database class, not stored in the DB but embedded in the BlogPost class below
    #the key difference is the lack of an _id field
    class Tag(Model):
        tag_name = StringField()

    #a simple model to hold blog posts
    class BlogPost(Model):
        _id = ObjectIDField()
        title = StringField(allow_empty=False)
        slug = StringField(allow_empty=False)
        post_intro = StringField()
        post_body = StringField()
        date_published = DateTimeField(default=datetime.datetime.now())
        tags = ListField(of=Tag)
        visible = BooleanField(default=True)

In the above example we've defined two models, the first ``Tag`` model is a straightforward class that is **not** a database object
the key distinction here is the lack of the ``_id`` field (this is only relevant to the MongoDB backend as it requires an ID to be
explicitly defined).

The second model ``BlogPost`` is the real model, and lists a series of fields to represent data types, fields can be anything, so
long as they subclass the ``Mojo.ObjectMapper.FieldPrototype.Field`` object.

Accessing model data
^^^^^^^^^^^^^^^^^^^^

You can access the above model quite easily in your code::

    new_minimal_post = BlogPost({
        'title':u'a new post',
        'slug' : 'newpost'
    })

    #access some properties
    print new_minimal_post.title
    > a new post

    #save it (assuming synchronous DB backend):
    thispost = new_minimal_post.save()

    print thispost._id
    > 50571e5f3d941cdc4487bdf1

Models can be assigned data in dictionary format as part of their initialisation, or empty and then using dot-notation
for each of their properties. So, in the example above, the following would work just as well::

    new_minimal_post = BlogPost()
    new_minimal_post.title = u'a new post'
    new_minimal_post.slug = 'newpost'

    #access some properties
    print new_minimal_post.title
    > a new post

    #save it (assuming synchronous DB backend):
    thispost = new_minimal_post.save()

    print thispost._id
    > 50571e5f3d941cdc4487bdf1

``Model`` objects are dictionaries, so if you print out or access them in any way, they should behave in the same way as a
stamdard python ``dict`` object.

Saving, Updating, Finding and Deleting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Saving is very straightforward in mojo, and as can be seen from the example above, can easily be accomplished with the ``save()``
instance method.

The main read/write operations of a model are as follows:

- ``save()``: Called on an instance of the model, this will attempt to save the data to the database, if the object has an initialised ``_id`` value then it will be updated, otherwise it will perform an insert
- ``delete()``: Called on an instance of the model, thjis will delete it from the database
- ``find()``: Called on the Model object (class method), will use the criteria passed to find to return a list of instantiated model instances
- ``find_one()``: Called on the model object (class method), will use the criteria passed to find a single model object
- ``delete_bulk([list])``: Pass a list of objects ot this function for a bulk delete operation

Both the ``find()`` and ``find_one()`` operations take MongoDB style ``dict`` objects as request parameters and follow the pymongo style of queries.

Asynchronous operations
^^^^^^^^^^^^^^^^^^^^^^^

One of the most appealing aspects of Tornado is it's ability to work asynchronously, and Mojo takes that to heart, ensuring taht you can just as well
use the asynchronous style of development with the ORM and Models.

To use the Asynchronous driver, make sure that you have changed it in your ``settings.py`` file::

    DATABASE = {
        'backend': 'Mojo.Backends.AsyncmongoBackend.asyncmongo_backend',
        'name': 'YOUR_DB_NAME',
        'host': '127.0.0.1',
        'port': 27017
    }

To start using it in your code, all models make an ``_async`` version of all operations available, that can be used with
traditional callback-style async handling or Tornado's ``gen`` module style (for more readable code)::


