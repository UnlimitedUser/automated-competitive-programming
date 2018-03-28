import os
import subprocess


def create_dir(judge, path):
    if not os.path.isdir(os.path.join(judge, path)):
        os.makedirs(os.path.join(judge, path))


def create_source(judge, path, name, extension):
    content = ''
    if os.path.isfile('default.cpp'):
        content = open('default.cpp', 'r').readlines()
    if not os.path.isfile(os.path.join(judge, path, name + extension)):
        open(os.path.join(
             judge, path, name + extension), 'w').write(''.join(content))


def open_source(judge, path, name, extension):
    subprocess.call(['subl', os.path.join(judge, path, name + extension)])
