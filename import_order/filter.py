import os


class FilterMixin(object):

    def apply(self):
        raise NotImplementedError()


class Exclude(FilterMixin):

    def __init__(self, excludes):
        excludes = [os.path.abspath(path) for path in excludes]
        self.file_excluds = [path for path in excludes if os.path.isfile(path)]
        self.dir_excluds = ['{path}{sep}'.format(path=path, sep=os.sep)
                            for path in excludes if os.path.isdir(path)]

    def apply(self, files):
        results = []
        for filename in files:
            abs_name = os.path.abspath(filename)
            exclude = False
            if abs_name in self.file_excluds:
                exclude = True
            for path in self.dir_excluds:
                if abs_name.startswith(path):
                    exclude = True
                    break
            if not exclude:
                results.append(filename)
        return results
