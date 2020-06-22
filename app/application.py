from app.utils import ConfigClass
import app.bash
import os
from app.utils import DirectoryIsNotGitRepoError


class Application(ConfigClass):
    def __init__(self, path: str):
        self.cloned_repo_path = ''
        self.junk_paths = []
        self.commits_list = []

        self.path = os.path.abspath(path)
        self.check_repo()

        self.clone_to_safe_dir()
        self.get_commits_list()

        self.commits_list = self.commits_list

        print(self.commits_list)

        for commit in self.commits_list:
            self.reset_to_commit(commit)
            print(self.get_repo_line_count())

        self.delete_junk()

    def check_repo(self):
        if not app.bash.is_git_repo(self.path):
            raise DirectoryIsNotGitRepoError

    def clone_to_safe_dir(self):
        self.cloned_repo_path = str(app.bash.clone_to_safe_dir(self.path).split()[0], 'utf-8')
        self.junk_paths.append(self.cloned_repo_path)

    def get_commits_list(self):
        self.commits_list = [commit_bytestr.decode('utf-8') for commit_bytestr in
                             app.bash.get_commits(self.cloned_repo_path)]

    def reset_to_commit(self, commit: str):
        app.bash.reset_commit(self.cloned_repo_path, commit)

    def get_repo_line_count(self):
        line_sum = 0
        for file_path in [path_bytestr.decode('utf-8') for path_bytestr in
                          app.bash.get_file_paths(self.cloned_repo_path)]:
            line_count = app.bash.get_line_count(file_path)
            print('{}: {}'.format(file_path, int(line_count.decode('utf-8'))))
            line_sum += line_count
        print('total: {}'.format(line_sum))

    def delete_junk(self):
        pass
