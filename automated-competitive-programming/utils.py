from bs4 import BeautifulSoup
import requests
import os
import subprocess
from colors import colors

def fetch_tests(judge, problem_url_prefix, id, name):
    respone = requests.get(problem_url_prefix + id + '/' + name, timeout=5)
    soup = BeautifulSoup(respone.content, 'html.parser')
    test_number = 1
    for test in soup.find('div', attrs={'class', 'sample-test'}).get_text('\n')[len('Input'):].split('Input'):
        t = test.split('Output')
        test_input = t[0].strip().replace(' \n', '\n')
        test_output = t[1].strip().replace(' \n', '\n')
        open(os.path.join(judge, id, 'input' + str(test_number) + '.txt'), 'w').write(test_input)
        open(os.path.join(judge, id, 'output' + str(test_number) + '.txt'), 'w').write(test_output)
        test_number += 1

def check_problem(judge, id, name):
    subprocess.check_output(['g++', '-o', id, '-std=c++14', os.path.join(judge, name, id + '.cpp')])
    test_number = 1
    while os.path.isfile(os.path.join(judge, name, 'input' + str(test_number) + '.txt')):
        output = subprocess.check_output(
            ['./' + id],
            input=''.join(open(os.path.join(judge, name, 'input' + str(test_number) + '.txt'), 'r').readlines()).encode())
        correct_output = ''.join(open(os.path.join(judge, name, 'output' + str(test_number) + '.txt'), 'r').readlines())
        if output.decode('utf-8').replace('\n', ' ').strip() == correct_output.replace('\n', ' ').strip():
            print(('Test number {}: ' + colors.AC + 'AC' + colors.ENDC).format(test_number))
        else:
            print(('Test number {}: ' + colors.WA + 'WA' + colors.ENDC).format(test_number))
        print('Output:\n{}'.format(output.decode('utf-8')))
        print('Correct output:\n{}'.format(correct_output))
        test_number += 1
    os.remove(id)

def create_dir(judge, path):
    if not os.path.isdir(os.path.join(judge, path)):
        os.makedirs(os.path.join(judge, path))

def create_source(judge, path, name, extension):
    content = ''
    if os.path.isfile('default.cpp'):
        content = open('default.cpp', 'r').readlines()
    if not os.path.isfile(os.path.join(judge, path, name + extension)):
        open(os.path.join(judge, path, name + extension), 'w').write(''.join(content))

def open_source(judge, path, name, extension):
    subprocess.call(['subl', os.path.join(judge, path, name + extension)])
