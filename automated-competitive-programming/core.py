from utils import (
    create_dir,
    open_source,
    create_source,
    create_sources,
    open_sources
)
from contest import (
    fetch_sources,
    fetch_all_tests
)
from problem import (
    fetch_tests,
    check_problem
)
import argparse
import json


JUDGES = ['codeforces', 'cf']


def main():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    parser = argparse.ArgumentParser(
        description='Automatic testcase checker for competitive programming.')
    parser.add_argument('-j', '--judge',
                        choices=JUDGES, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-fp', '--fetch-problem', dest='contest_id',
                       metavar='problem',
                       help='fetch a problem and create source files')
    group.add_argument('-fc', '--fetch-contest', dest='contest_id_full',
                       metavar='contest',
                       help='fetch a contest and create source files')
    group.add_argument('-rt', '--run-testcases', dest='contest_id_tc',
                       metavar='problem',
                       help='run fetched testcases')
    args = parser.parse_args()

    judge = args.judge
    if judge == 'cf':
        judge = 'codeforces'

    editor = data['editor']

    if args.contest_id is not None:
        contest_id = args.contest_id[0:-1]
        name = args.contest_id[-1]
        create_dir(judge, contest_id)
        create_source(judge, contest_id, name, '.cpp',
                      data['default_code']['path'])
        open_source(judge, contest_id, name, '.cpp', editor)
        fetch_tests(judge, data['url']['problem_prefix'][judge],
                    contest_id, name)
    elif args.contest_id_full is not None:
        contest_id = args.contest_id_full
        create_dir(judge, contest_id)
        sources = fetch_sources(judge, data['url']['contest_prefix'][judge])
        create_sources(judge, contest_id, sources, '.cpp',
                       data['default_code']['path'])
        open_sources(judge, contest_id, sources, '.cpp')
        fetch_all_tests(judge, data['url']['contest_prefix'][judge],
                        contest_id, sources)
    elif args.contest_id_tc is not None:
        contest_id = args.contest_id_tc[0:-1]
        name = args.contest_id_tc[-1]
        check_problem(judge, contest_id, name,
                      data['compiler']['name'], data['compiler']['flags'])


if __name__ == '__main__':
    main()
