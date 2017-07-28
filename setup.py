# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='countries_lib',
    version='1.0',
    include_package_data=True,
    packages=find_packages(),
    test_suite='tests',
    package_data={'countries_lib': ['database/*', 'documentation/*', 'documentation/html_doc/*',
                                    'documentation/html_doc/_static/*']}
)
