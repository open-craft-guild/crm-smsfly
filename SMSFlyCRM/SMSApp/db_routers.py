"""Database apps router

This module has been shamelessly copy-pasted from
http://diegobz.net/2011/02/10/django-database-router-using-settings/
and then improved a little then

Thanks to answerers @ http://stackoverflow.com/a/18548287/595220
"""

import logging

from django.conf import settings


logger = logging.getLogger(__name__)


class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """

    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""

        return settings.DATABASE_APPS_MAPPING.get(getattr(model._meta, 'db_route', None), 'default')

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""

        return settings.DATABASE_APPS_MAPPING.get(getattr(model._meta, 'db_route', None), 'default')

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""

        db_obj1 = settings.DATABASE_APPS_MAPPING.get(getattr(obj1._meta, 'db_route', None), 'default')
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(getattr(obj2._meta, 'db_route', None), 'default')
        allow_relation = db_obj1 == db_obj2

        logger.debug('Deciding whether to allow relation between {obj1} ({obj1_db}) and {obj2} ({obj2_db}): {allow}'.
                     format(obj1=obj1, obj2=obj2, obj1_db=db_obj1, obj2_db=db_obj2, allow=allow_relation))

        return allow_relation

    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""

        if db in settings.DATABASE_APPS_MAPPING.values() or db == 'default':
            return settings.DATABASE_APPS_MAPPING.get(getattr(model._meta.db_route, 'db_route', None), 'default') == db
        elif model._meta.db_route in settings.DATABASE_APPS_MAPPING:
            return False
        return None
