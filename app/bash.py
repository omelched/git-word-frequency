import subprocess
import os
import sys


def get_commits(path: str) -> list:
    os.chdir(os.path.relpath(path, os.getcwd()))
    process = subprocess.Popen(['git', 'rev-list', '--all'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.split()


def clone_to_safe_dir(path: str) -> bytes:
    os.chdir(os.path.relpath(path, os.getcwd()))
    base_dir_name = os.getcwd().split('/')[-1]
    os.chdir('../')
    process = subprocess.Popen(
        'mkdir {}_junk; cd {}_junk; git init; git remote add origin ../{}; git pull origin master; pwd'.format(
            base_dir_name,
            base_dir_name,
            base_dir_name),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        sys.stdout.buffer.write(line)
    return line


def reset_commit(path: str, commit: str):
    os.chdir(os.path.relpath(path, os.getcwd()))
    process = subprocess.Popen(
        'git reset --hard {}'.format(commit),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        sys.stdout.buffer.write(line)


def is_git_repo(path: str) -> bool:
    os.chdir(os.path.relpath(path, os.getcwd()))
    process = subprocess.Popen('git rev-parse --is-inside-work-tree',
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    o, e = process.communicate()
    if e:
        return False
    else:
        return True


def get_file_paths(path) -> list:
    os.chdir(os.path.relpath(path, os.getcwd()))
    cmd = b'find . -type f -a -not -path "*.git*" -a -not -name "*~" -exec sh -c "for f do git check-ignore -q "$f" ' \
          + b'|| printf "%s\\\\n" "$f" done" find-sh {} +'
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.split()


def get_line_count(path) -> bytes:
    process = subprocess.Popen(
        'wc -l "$f" | tr -s ' ' | cut -d ' ' -f 2'.format(path),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output
