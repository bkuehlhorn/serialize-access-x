#!/usr/bin/env python
from setuptools import setup, find_packages


setup_requires = [
    'pytest',
    'nose',
    'coverage',
]
install_requires = [
    'pathlib2>=2.3',
]
tests_require = []


description = "A flexible utility for accessing json objects in Python."

long_description = """\
Please visit  the `GitHub repository <https://github.com/bkuehlhorn/serialize-access>`_
for more information.\n
"""
with open('README.rst') as fp:
    long_description += fp.read()


setup(
    name='serialize-access',
    version="0.0.4",
    description=description,
    long_description=long_description,
    author='Bernard Kuehlhorn',
    url='https://github.com/bkuehlhorn/serialize-access',
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    license="BSD 2-Clause License",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: BSD License',
    ],
    test_suite='nose.collector',
    packages=find_packages(),
)
