#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup
import pathlib
# import sdist_upip

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = "Some long description"

# load elements of version.py
exec(open(here / 'sample_version.py').read())

setup(
    name='micropython-package-validation-example',
    version=__version__,
    description="Validate MicroPython package JSON file ",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brainelectronics/micropython-package-validation',
    author='brainelectronics',
    author_email='info@brainelectronics.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='micropython, validation, package',
    project_urls={
        'Bug Reports': 'https://github.com/brainelectronics/micropython-package-validation/issues',
        'Source': 'https://github.com/brainelectronics/micropython-package-validation',
    },
    license='MIT',
    # cmdclass={'sdist': sdist_upip.sdist},
    packages=[
        'subdir1',
        'other_dir',
    ],
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    data_files=[
        (
            'static',
            [
                'static/style.css',
                'static/favicon.ico',
                'static/js/function.js',
            ]
        ),
        (
            'other_files',
            [
                'other_files/index.tpl',
                'other_files/page.tpl',
            ]
        )
    ],
    install_requires=[
        'dependency_1',
        'dependency_2',
    ]
)
