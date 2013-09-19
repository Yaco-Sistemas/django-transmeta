0.7.3 (2013-09-02)
-------------------

- Update the metainfo

0.7.2 (2013-09-02)
-------------------

- The project has moved to github

0.7.1 (2013-09-02)
-------------------

- Add manifest

0.7.0 (2013-09-02)
-------------------

- Python3 compatible
- Fix the readme

0.6.11 (2013-08-20)
-------------------

- Added get_mandatory_fieldname function.

0.6.10 (2013-03-18)
-------------------

- New TRANSMETA_MANDATORY_LANGUAGE setting, to control which field will be NOT NULL in the models.

0.6.9 (2012-10-24)
------------------

- Support in method get_field_language for field names with underscores

0.6.8 (2012-06-22)
------------------

- Fix a little bug in the command sync_transmeta_db (UnboundLocalError: local variable 'f' referenced before assignment)

0.6.7 (2012-03-20)
------------------

- Change the representation (verbose_name) of the transmeta labels 


0.6.6 (2012-02-06)
------------------

- Improvements and usability in the command sync_transmeta_db
- Fix some bugs
- Documentation


0.6.5 (2012-01-13)
------------------

- Improvements and usability in the command sync_transmeta_db
- Works with the last django (the command sync_transmeta_db)
- Works with mysql (the command sync_transmeta_db)


0.6.4 (2011-11-29)
------------------

- Fixes error with inheritance in models.

0.6.3 (2011-11-29)
------------------

- Allow to use a TRANSMETA_LANGUAGES settings.
- Added two options to sync_transmeta_db: -y (assume yes on all) and -d (default language code)


0.6.2 (2011-03-22)
------------------

- works when default locale have spelling variants as es-ES or en-US.


0.6.1 (2011-03-17)
------------------

- get_all_translatable_fields does not returned the correct tuple. Problems with inheritance.

0.6.0 (2011-02-24)
------------------

- Make compatible with Django 1.2 and 1.3 when using ugettext_lazy in models verbose_name, fixing a hidden bug also for Django 1.1

