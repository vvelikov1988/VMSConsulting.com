from django.utils.deconstruct import deconstructible

import os
from uuid import uuid4


@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)
