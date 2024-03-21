from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xmonkey-curator',
    version='0.1.0',
    description="Automated OSS curation scanner",
    long_description=long_description,
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    url='https://github.com/Xpertians/xmonkey-curator',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'click>=7.0',
        'lief>=0.11.5',
        'python-magic',
    ],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'xmonkey-curator=xmonkey_curator.scanner:scan',
        ],
    },
    include_package_data=True,
    package_data={
    },
    test_suite="tests",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
