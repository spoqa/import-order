import os


class Exclude:
    def __init__(self, excludes):
        excludes = [os.path.abspath(path) for path in excludes]
        self.file_excluds = [path for path in excludes if os.path.isfile(path)]
        self.dir_excluds = [str.format('{path}{sep}', path=path, sep=os.sep)
                            for path in excludes if os.path.isdir(path)]

    def __call__(self, files):
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
