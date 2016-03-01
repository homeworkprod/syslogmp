# -*- coding: utf-8 -*-

import codecs
import sys

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


# Require the 'enum34' package on Python versions before 3.4.
install_requires = []
if sys.version_info[:2] < (3, 4):
    install_requires.append('enum34')


setup(
    name='syslogmp',
    version='0.2.2',
    description='A parser for BSD syslog protocol (RFC 3164) messages',
    long_description=long_description,
    url='http://homework.nwsnet.de/releases/76d6/#syslogmp',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: System :: Logging',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    packages=['syslogmp'],
    install_requires=install_requires,
    tests_require=['freezegun>=0.3.6', 'nose2', 'tox'],
    test_suite='nose2.collector.collector',
)
