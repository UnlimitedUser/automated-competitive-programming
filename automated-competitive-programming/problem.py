from bs4 import BeautifulSoup
import os
import requests
import subprocess
from colors import colors


def fetch_tests(judge, problem_url_prefix, contest_id, name):
    respone = requests.get(problem_url_prefix + contest_id + '/' + name,
                           timeout=5)
    soup = BeautifulSoup(respone.content, 'html.parser')
    test_number = 1
    for test in (soup.find('div', attrs={'class', 'sample-test'})
                 .get_text('\n')[len('Input'):].split('Input')):
        t = test.split('Output')
        test_input = t[0].strip().replace(' \n', '\n')
        test_output = t[1].strip().replace(' \n', '\n')
        open(os.path.join(judge, contest_id,
             'input' + str(test_number) + '.txt'), 'w').write(test_input)
        open(os.path.join(judge, contest_id,
             'output' + str(test_number) + '.txt'), 'w').write(test_output)
        test_number += 1


def check_problem(judge, contest_id, name, compiler, flags):
    subprocess.check_output([compiler, '-o', contest_id, flags,
                            os.path.join(judge, contest_id, name + '.cpp')])
    test_number = 1
    while os.path.isfile(os.path.join(judge, contest_id,
                                      'input' + str(test_number) + '.txt')):
        output = subprocess.check_output(
            ['./' + contest_id],
            input=''.join(open(os.path.join(judge, contest_id,
                          'input' + str(test_number) + '.txt'), 'r')
                          .readlines()).encode())
        correct_output = ''.join(open(os.path.join(judge, contest_id,
                                 'output' + str(test_number) + '.txt'), 'r')
                                 .readlines())
        if (output.decode('utf-8').replace('\n', ' ').strip() ==
                correct_output.replace('\n', ' ').strip()):
            print(('Test number {}: ' + colors.AC +
                  'AC' + colors.ENDC).format(test_number))
        else:
            print(('Test number {}: ' + colors.WA +
                  'WA' + colors.ENDC).format(test_number))
        print('Output:\n{}'.format(output.decode('utf-8')))
        print('Correct output:\n{}'.format(correct_output))
        test_number += 1
    os.remove(contest_id)