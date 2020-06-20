from app.utils import ConfigClass
from app.bash import get_commits


class Application(ConfigClass):
    def __init__(self, path):
        self.path = path
        self.commits_list = self.get_commits_list()
        for commit in self.commits_list:



    @staticmethod
    def get_commits_list() -> list:
        return [commit_bytestr.decode('utf-8') for commit_bytestr in get_commits('../../git_repo/trade_test')]
