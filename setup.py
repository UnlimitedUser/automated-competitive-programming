from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

setup(
    name = 'automated-competitive-programming',
    version = '0.1.0',
    description = 'Problem fetcher/checker for competitive programming',
    long_description = readme,
    long_description_content_type='text/markdown',
    licenses = 'MIT',
    author = 'Sclearov Dan',
    author_email = 'sclearovdan@gmail.com',
    url = 'https://github.com/sclearovdan/automated-competitive-programming',
    download_url = 'https://github.com/sclearovdan/automated-competitive-programming/archive/0.1.tar.gz',
    keywords = ['competitive programming', 'online judge', 'automatic tester',
                'codeforces', 'c++'],
    install_requires=['Beautiful Soup'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: MIT License',
        'Intended Audience :: Competitive Programmers',
        'Topic :: Competitive Programming',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3',
)