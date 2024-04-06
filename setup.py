import os
import re        
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read_version():
    version_file_path = os.path.join(here, 'src', 'xmonkey_curator', '__version__.py')
    with open(version_file_path, encoding='utf-8') as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xmonkey-curator',
    version=read_version(),
    description="Automated OSS curation scanner",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    url='https://github.com/Xpertians/xmonkey-curator',
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'click>=7.0',
        'lief>=0.11.5',
        'python-magic',
        'libmagic',
        'pygments',
        'ssdeep',
        'tqdm',
        'rpmfile',
        'zstandard',
        'requests',
    ],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'xmonkey-curator=xmonkey_curator.scanner:cli',
        ],
    },
    include_package_data=True,
    package_data={
        'xmonkey_curator': ['signatures/*.json', 'licenses/*.json', 'rules/*.json'],
    },
    test_suite="tests",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
