class ConfigClass(object):
    pass


class LoggedException(BaseException):
    pass


class DirectoryIsNotGitRepoError(LoggedException):
    pass
