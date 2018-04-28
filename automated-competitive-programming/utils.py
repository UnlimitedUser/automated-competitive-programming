import os
import subprocess


def create_dir(judge, path):
    if not os.path.isdir(os.path.join(judge, path)):
        os.makedirs(os.path.join(judge, path))


def create_source(judge, path, name, extension, default_code_path):
    content = ''
    if os.path.isfile(default_code_path):
        content = open(default_code_path, 'r').readlines()
    if not os.path.isfile(os.path.join(judge, path, name + extension)):
        open(os.path.join(
             judge, path, name + extension), 'w').write(''.join(content))


def open_source(judge, path, name, extension, editor):
    subprocess.call([editor, os.path.join(judge, path, name + extension)])


def create_sources(judge, contest_id, sources, default_code_path):  # TODO
    pass


def open_sources(judge, contest_id, sources, extension, editor):  # TODO
    pass
