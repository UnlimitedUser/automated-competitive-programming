from bs4 import BeautifulSoup
import requests
import argparse
import os
import subprocess

# Constants
JUDGES = ['codeforces', 'cf']
CF_CONTEST_URL_PREFIX = 'http://codeforces.com/contest/'
CF_PROBLEM_URL_PREFIX = 'http://codeforces.com/problemset/problem/'

class colors:
    AC = '\033[92m'
    WA = '\033[93m'
    ENDC = '\033[0m'

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

# Command line parsing
parser = argparse.ArgumentParser(description='Automatic testcase checker for competitive programming.')
parser.add_argument('-j', '--judge',
                    choices=JUDGES, required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-fp', '--fetch-problem', dest='problem_id',
                   metavar='problem', help='fetch a problem and create source files')
group.add_argument('-fc', '--fetch-contest', dest='constest_id',
                   metavar='contest', help='fetch a contest and create source files')
group.add_argument('-rt', '--run-testcases', dest='problem_id_tc',
                   metavar='problem', help='run fetched testcases')
args = parser.parse_args()

judge = args.judge
if judge == 'cf': judge = 'codeforces'

if args.problem_id is not None:
    create_dir(judge, args.problem_id[0:-1])
    create_source(judge, args.problem_id[0:-1], args.problem_id[-1], '.cpp')
    open_source(judge, args.problem_id[0:-1], args.problem_id[-1], '.cpp')
    respone = requests.get(CF_PROBLEM_URL_PREFIX + args.problem_id[0:-1] + '/' + args.problem_id[-1], timeout=5)
    soup = BeautifulSoup(respone.content, 'html.parser')
    test_number = 1
    for test in soup.find('div', attrs={'class', 'sample-test'}).get_text('\n')[len('Input'):].split('Input'):
        t = test.split('Output')
        test_input = t[0].strip().replace(' \n', '\n')
        test_output = t[1].strip().replace(' \n', '\n')
        open(os.path.join(judge, args.problem_id[0:-1], 'input' + str(test_number) + '.txt'), 'w').write(test_input)
        open(os.path.join(judge, args.problem_id[0:-1], 'output' + str(test_number) + '.txt'), 'w').write(test_output)
        test_number += 1
elif args.constest_id is not None:
    pass
elif args.problem_id_tc is not None:
    subprocess.check_output(['g++', '-o', args.problem_id_tc[-1], '-std=c++14', os.path.join(judge, args.problem_id_tc[0:-1], args.problem_id_tc[-1] + '.cpp')])
    test_number = 1
    while os.path.isfile(os.path.join(judge, args.problem_id_tc[0:-1], 'input' + str(test_number) + '.txt')):
        output = subprocess.check_output(
            ['./' + args.problem_id_tc[-1]],
            input=''.join(open(os.path.join(judge, args.problem_id_tc[0:-1], 'input' + str(test_number) + '.txt'), 'r').readlines()).encode())
        correct_output = ''.join(open(os.path.join(judge, args.problem_id_tc[0:-1], 'output' + str(test_number) + '.txt'), 'r').readlines())
        if output.decode('utf-8').replace('\n', ' ').strip() == correct_output.replace('\n', ' ').strip():
            print(('Test number {}: ' + colors.AC + 'AC' + colors.ENDC).format(test_number))
        else:
            print(('Test number {}: ' + colors.WA + 'WA' + colors.ENDC).format(test_number))
        print('Output:\n{}'.format(output.decode('utf-8')))
        print('Correct output:\n{}'.format(correct_output))
        test_number += 1
    os.remove(args.problem_id_tc[-1])
