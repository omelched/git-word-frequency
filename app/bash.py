import subprocess
import os


def get_commits(path: str) -> list:
    os.chdir(path)
    process = subprocess.Popen(['git', 'rev-list', '--all'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.split()

