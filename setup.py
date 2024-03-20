from setuptools import setup, find_packages

setup(
    name='xmonkey-curator',
    description="Automated OSS curation scanner",
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    version='0.1.0',
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
