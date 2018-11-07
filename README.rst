Introduction
============

.. image:: https://badge.fury.io/py/django-transmeta.png
    :target: https://badge.fury.io/py/django-transmeta

.. image:: https://pypip.in/d/django-transmeta/badge.png
    :target: https://pypi.python.org/pypi/django-transmeta

Transmeta is an application for to make Django model fields translatable.
Each language is stored and managed automatically in a different database column.


Features
========

* Automatic schema creation for translatable fields.
* Translatable fields integrated into Django's admin interface.
* Command to synchronize database schema for new or removed translatable fields and languages.

Using transmeta
===============

Creating translatable models
----------------------------

Example model::

    class Book(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField()
        body = models.TextField(default='')
        price = models.FloatField()

Suppose you want to make ``description`` and ``body`` translatable.
The resulting model after using ``transmeta``::


    from transmeta import TransMeta

    class Book(models.Model):
        __metaclass__ = TransMeta

        title = models.CharField(max_length=200)
        description = models.TextField()
        body = models.TextField(default='')
        price = models.FloatField()

        class Meta:
            translate = ('description', 'body', )

In python 3::

    from transmeta import TransMeta

    class Book(models.Model, metaclass=transmeta.TransMeta):

        title = models.CharField(max_length=200)
        description = models.TextField()
        body = models.TextField(default='')
        price = models.FloatField()

        class Meta:
            translate = ('description', 'body', )

Make sure you have set both, the default language and other available languages in your ``settings.py``::

    LANGUAGE_CODE = 'es'

    ugettext = lambda s: s # dummy ugettext function, as django's docs say

    LANGUAGES = (
        ('es', ugettext('Spanish')),
        ('en', ugettext('English')),
    )

Notes:

* It's possible to set another language as default for the content::

    TRANSMETA_DEFAULT_LANGUAGE = 'it'

  This would show the interface in one language and the content in another one.

* You can do the same with available content languages::

    TRANSMETA_LANGUAGES = (
        ('es', ugettext('Spanish')),
        ('en', ugettext('English')),
        ('it', ugettext('Italian')),
    )

SQL generated using ``./manage.py sqlall``::

    BEGIN;
    CREATE TABLE "fooapp_book" (
        "id" serial NOT NULL PRIMARY KEY,
        "title" varchar(200) NOT NULL,
        "description_en" text,
        "description_es" text,
        "description_it" text NOT NULL,
        "body_en" text,
        "body_es" text,
        "body_it" text NOT NULL,
        "price" double precision NOT NULL
    )
    ;
    COMMIT;

Notes:

* ``transmeta`` creates one column for each language. Don't worry if you need new languages in the future, ``transmeta`` solves this problem for you.
* If one field has ``null=False`` and doesn't have a default value, ``transmeta`` will create only one ``NOT NULL`` field, for the default language.
  Fields for other secondary languages will be nullable. The primary language will be required in the admin app,
  while the other fields will be optional (with ``blank=True``).
  This was done because the normal approach for content translation is to add first the content fo the main language and
  complete other translations afterwards.
* You can use ``./manage.py syncdb`` to create database schema.

Playing with the Python shell
-----------------------------

``transmeta`` creates one field for every translatable field of a model. Field names are suffixed with language short codes,
e.g.: ``description_es``, ``description_en``, and so on. In addition it creates a ``field_name`` getter to retrieve the field value for the active language.

Let's play a bit in the python shell to understand how this works::

    >>> from fooapp.models import Book
    >>> b = Book.objects.create(description_es=u'mi descripcion', description_en=u'my description')
    >>> b.description
    u'my description'
    >>> from django.utils.translation import activate
    >>> activate('es')
    >>> b.description
    u'mi descripcion'
    >>> b.description_en
    u'my description'

Adding new languages
--------------------

If you need to add new languages to the existing ones you only need to change your settings.py and ask transmeta to sync the database again.
For example, to add French to our project, you need to add it to LANGUAGES in ``settings.py``::

    LANGUAGES = (
        ('es', ugettext('Spanish')),
        ('en', ugettext('English')),
        ('fr', ugettext('French')),
    )

and execute the ``sync_transmeta_db`` command::

    $ ./manage.py sync_transmeta_db

    This languages can change in "description" field from "fooapp.book" model: fr

    SQL to synchronize "fooapp.book" schema:
       ALTER TABLE "fooapp_book" ADD COLUMN "description_fr" text

    Are you sure that you want to execute the previous SQL: (y/n) [n]: y
    Executing SQL... Done

    This languages can change in "body" field from "fooapp.book" model: fr

    SQL to synchronize "fooapp.book" schema:
       ALTER TABLE "fooapp_book" ADD COLUMN "body_fr" text

    Are you sure that you want to execute the previous SQL: (y/n) [n]: y
    Executing SQL... Done

And done!

Adding new translatable fields
------------------------------

Now imagine that, after several months using this web app (with many books created), you need to make the book price translatable
(e.g., because book price depends on currency).

To achieve this, first add ``price`` to the model's translatable fields list::

    class Book(models.Model):
        ...
        price = models.FloatField()

        class Meta:
            translate = ('description', 'body', 'price', )

You only have to run the ``sync_transmeta_db`` command to update the database schema::

    $ ./manage.py sync_transmeta_db

    This languages can change in "price" field from "fooapp.book" model: es, en

    SQL to synchronize "fooapp.book" schema:
        ALTER TABLE "fooapp_book" ADD COLUMN "price_es" double precision
        UPDATE "fooapp_book" SET "price_es" = "price"
        ALTER TABLE "fooapp_book" ALTER COLUMN "price_es" SET NOT NULL
        ALTER TABLE "fooapp_book" ADD COLUMN "price_en" double precision
        ALTER TABLE "fooapp_book" DROP COLUMN "price"

    Are you sure that you want to execute the previous SQL: (y/n) [n]: y
    Executing SQL...Done

So what does this command do?

The ``sync_transmeta_db`` command not only creates new database columns for new translatable fields,
it also copies data from the old ``price`` field into the new default tranlated field (here ``prices_es``).
It's very important that the LANGUAGE_CODE and LANGUAGES (or TRANSMETA_DEFAULT_LANGUAGE, TRANSMETA_LANGUAGES) settings have the correct values.

This command is also needed if you want to add a new language to the site or the default language is changed.
For the latter case, you can define a variable in the settings file::

    TRANSMETA_VALUE_DEFAULT = '---'


Removing languages
------------------

Since version 0.7.4, fields for unused languages can also be removed by using the ``-D`` option when running the ``sync_transmeta_db`` command.

Admin integration
-----------------

``transmeta`` transparently displays all translatable fields in the admin interface. This is easy because models have in fact many fields (one for each language).

Changing form fields in the admin is quite a common task, and ``transmeta`` includes the
``canonical_fieldname`` utility function to apply these changes for all language fields at once. This is better explained with an example::

    from transmeta import canonical_fieldname

    class BookAdmin(admin.ModelAdmin):
        def formfield_for_dbfield(self, db_field, **kwargs):
            field = super(BookAdmin, self).formfield_for_dbfield(db_field, **kwargs)
            db_fieldname = canonical_fieldname(db_field)
            if db_fieldname == 'description':
                # this applies to all description_* fields
                field.widget = MyCustomWidget()
            elif field.name == 'body_es':
                # this applies only to body_es field
                field.widget = MyCustomWidget()
            return field
