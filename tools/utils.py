from data.operations import BulkOperationOption
from data.indexes import IndexQuery
from custom_exceptions import exceptions
import urllib
import sys
import re


class Utils(object):
    @staticmethod
    def quote_key(key):
        reserved = '%:=&?~#+!$,;\'@()*[]'
        if key:
            # To be able to work on python 2.x and 3.x
            if sys.version_info.major > 2:
                return urllib.parse.quote(key, safe=reserved)
            else:
                return urllib.quote(key, safe=reserved)
        else:
            return ''

    @staticmethod
    def name_validation(name):
        if name is None:
            raise ValueError("None name is not valid")
        result = re.match(r'([A-Za-z0-9_\-\.]+)', name, re.IGNORECASE)
        if not result:
            raise exceptions.InvalidOperationException(
                "Database name can only contain only A-Z, a-z, \"_\", \".\" or \"-\" but was: " + name)

    @staticmethod
    def build_path(index_name, query, options):
        if index_name is None:
            raise ValueError("None index_name is not valid")
        path = "bulk_docs/{0}?".format(Utils.quote_key(index_name) if index_name else "")
        if query is None:
            raise ValueError("None query is not valid")
        if not isinstance(query, IndexQuery):
            raise ValueError("query must be IndexQuery type")
        if query.query:
            path += "&query={0}".format(Utils.quote_key(query.query))
        if options is None:
            options = BulkOperationOption()
        if not isinstance(options, BulkOperationOption):
            raise ValueError("options must be BulkOperationOption type")

        path += "&pageSize={0}&allowStale={1}&details={2}".format(query.page_size, options.allow_stale,
                                                                  options.retrieve_details)
        if options.max_ops_per_sec:
            path += "&maxOpsPerSec={0}".format(options.max_ops_per_sec)
        if options.stale_timeout:
            path += "&staleTimeout={0}".format(options.stale_timeout)

        return path

    @staticmethod
    def object_equality(entity, other_entity):
        return entity is other_entity

    @staticmethod
    def import_class(name):
        components = name.split('.')
        try:
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod
        except (ImportError, ValueError):
            pass
        return None
