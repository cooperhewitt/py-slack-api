#!/usr/bin/env python

from distutils.core import setup

setup(name='slack-api',
      version='0.1',
      description='Simple Python wrapper for Slack API',
      author='Smithsonian Cooper-Hewitt National Design Museum',
      url='https://github.com/cooperhewitt/py-slack-api',
      requires=[],
      packages=[
          'slack',
          'slack.api'
      ],
      scripts=[
          'scripts/slack-chat'
      ],
      download_url='https://github.com/cooperhewitt/py-slack-api/releases/tag/v0.1',
      license='BSD')
