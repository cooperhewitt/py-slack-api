#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='slack.api',
    namespace_packages=['slack'],
    version='0.4',
    description='Simple Python wrapper for the Slack API',
    author='Smithsonian Cooper-Hewitt National Design Museum',
    url='https://github.com/cooperhewitt/py-slack-api',
    install_requires=[
        'requests'
        ],
    packages=packages,
    scripts=[
        'scripts/slack-chat',
        'scripts/slack-hook'        
        ],
    download_url='https://github.com/cooperhewitt/py-slack-api/releases/tag/v0.3',
    license='BSD')
