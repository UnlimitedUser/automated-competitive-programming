from utils import fetch_tests, check_problem, create_dir, create_source, open_source # pylint: disable=no-name-in-module
import argparse
import subprocess

# Constants
JUDGES = ['codeforces']
CF_CONTEST_URL_PREFIX = 'http://codeforces.com/contest/'
CF_PROBLEM_URL_PREFIX = 'http://codeforces.com/problemset/problem/'

def main():
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
    
    id = args.problem_id[0:-1]
    name = args.problem_id[-1]

    if args.problem_id is not None:
        create_dir(judge, id)
        create_source(judge, id, name, '.cpp')
        open_source(judge, id, name, '.cpp')
        fetch_tests(judge, CF_PROBLEM_URL_PREFIX, id, name)
    elif args.constest_id is not None:
        pass
    elif args.problem_id_tc is not None:
        check_problem(judge, id, name)

if __name__ == '__main__':
    main()
