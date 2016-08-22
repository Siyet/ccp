from StringIO import StringIO
from zipfile import ZipFile


class ArchiveFile(object):

    def __init__(self, filename, content):
        self.filename = filename
        self.content = content


class ArchiveGenerator(object):
    
    def __init__(self, files=None):
        if files is None:
            self._files = []
        else:
            self._files = files

    def add(self, filename, content):
        self._files.append(ArchiveFile(filename, content))

    def archive(self):
        if not self._files:
            return None
        result = StringIO()
        with ZipFile(result, 'w') as fz:
            for file in self._files:
                fz.writestr(file.filename, file.content)
        return result.getvalue()
