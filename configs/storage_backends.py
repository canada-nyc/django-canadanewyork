from storages.backends.s3boto import S3BotoStorage
from django.contrib.staticfiles.storage import CachedFilesMixin


class S3HashedFilesStorage(CachedFilesMixin, S3BotoStorage):
    """
    Extends S3BotoStorage to also save hashed copies (i.e.
    with filenames containing the file's MD5 hash) of the
    files it saves.
    """
    pass
