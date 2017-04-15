import functools
import gzip
import hashlib
import inspect
import os.path
import time


def args_to_hash_filename(*args):
    hashable = '|'.join(map(repr, args))
    kernel = hashlib.md5(hashable.encode('utf-8')).hexdigest()[: 16]
    return '.'.join(('', kernel, 'gz'))


def dump_to_gzip(filename, content):
    with gzip.open(filename, 'wt') as f:
        f.write(content)


def io_cache_with_ttl(seconds=None):

    def decorator(function):

        def io_cache(self, *args):

            if seconds is not None:
                filename = args_to_hash_filename(*args, truncated_epoch(seconds))
            else:
                filename = args_to_hash_filename(*args)

            if os.path.isfile(filename):
                content = load_from_gzip(filename)
            else:
                content = function(self, *args)
                dump_to_gzip(filename, content)

            return content

        return io_cache

    if inspect.isfunction(seconds):
        # No parameters were provided:
        # The function is being decorated so we must perform the decoration ourselves
        seconds = None
        return decorator(seconds)
    else:
        # A seconds parameter has been provided:
        # The function isn't being decorated, so we return the decorator
        return decorator


def load_from_gzip(filename):
    with gzip.open(filename, 'rt') as f:
        return f.read()


def truncated_epoch(truncation_in_seconds):
    epoch = int(time.time())
    return epoch - (epoch % truncation_in_seconds)


def two_level_cache(function):

    @functools.lru_cache(maxsize=None)
    def io_cache(self, *args):

        filename = args_to_hash_filename(*args)

        if os.path.isfile(filename):
            content = load_from_gzip(filename)
        else:
            content = function(self, *args)
            dump_to_gzip(filename, content)

        return content

    return io_cache
