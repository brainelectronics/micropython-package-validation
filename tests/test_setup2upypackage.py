#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Unittest for testing the setup2upypackage file"""

import json
import logging
import unittest
from pathlib import Path
from random import shuffle
from sys import stdout
from unittest.mock import PropertyMock, mock_open, patch

from nose2.tools import params

from setup2upypackage.setup2upypackage import (Setup2uPyPackage,
                                               Setup2uPyPackageError)


class TestSetup2uPyPackage(unittest.TestCase):

    def setUp(self) -> None:
        """Run before every test method"""
        # define a format
        custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                        ' %(funcName)-15s:%(lineno)4s] %(message)s'

        # set basic config and level for all loggers
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=stdout)

        # create a logger for this TestSuite
        self.test_logger = logging.getLogger(__name__)
        self.package_logger = logging.getLogger('UpdateVersion')

        # set the test logger level
        self.test_logger.setLevel(logging.DEBUG)
        self.package_logger.setLevel(logging.DEBUG)

        self._here = Path(__file__).parent

        self.setup_file = self._here / 'data' / 'setup.py'
        self.package_changelog_file = \
            self._here / 'data' / 'sample_changelog.md'
        self.package_file = self._here / 'data' / 'package.json'

        self.test_package_expectation = {
            'version': '1.2.3',
            'install_requires': [
                'dependency_1',
                'dependency_2'
            ],
            'url': 'https://github.com/brainelectronics/micropython-package-validation',    # noqa: E501
            'packages': [
                'subdir1',
                'other_dir'
            ],
            'data_files': [
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
            ]
        }
        # 2 files in "other_files", 3 in "static"
        self.data_files_expectation = [
            Path('static/style.css'),
            Path('static/favicon.ico'),
            Path('static/js/function.js'),
            Path('other_files/index.tpl'),
            Path('other_files/page.tpl'),
        ]
        # 3 .py files in "other_dir", 1 in "subdir1"
        self.package_files_expectation = [
            Path('subdir1/asdf.py'),
            Path('other_dir/bar.py'),
            Path('other_dir/baz.py'),
            Path('other_dir/foo.py')
        ]

        self.s2pp = Setup2uPyPackage(
            setup_file=self.setup_file,
            package_file=None,
            package_changelog_file=None,
            logger=self.package_logger
        )

    def tearDown(self) -> None:
        """Run after every test method"""
        pass

    def test__create_logger(self):
        """Test logger creation"""
        logger_name = "Test Logger"
        named_logger = Setup2uPyPackage._create_logger(logger_name=logger_name)

        self.assertIsInstance(named_logger, logging.Logger)
        self.assertEqual(named_logger.name, logger_name)
        self.assertEqual(named_logger.level, logging.DEBUG)
        self.assertEqual(named_logger.disabled, False)

        logger_without_name = Setup2uPyPackage._create_logger()

        self.assertIsInstance(logger_without_name, logging.Logger)
        self.assertEqual(logger_without_name.name,
                         "setup2upypackage.setup2upypackage")
        self.assertEqual(logger_without_name.level, logging.DEBUG)

    def test__parse_setup_file_content(self) -> None:
        """Test parsing setup.py file"""
        for key, val in self.test_package_expectation.items():
            self.assertEqual(self.s2pp._setup_data[key], val)

    def test_package_version(self) -> None:
        """Test setup version property"""
        val = self.s2pp.package_version
        self.assertIsInstance(val, str)
        self.assertEqual(val, self.test_package_expectation['version'])

        self.s2pp._setup_data.pop('version')
        val = self.s2pp.package_version
        self.assertIsInstance(val, str)
        self.assertEqual(val, '-1.-1.-1')

        s2pp = Setup2uPyPackage(
            setup_file=self.setup_file,
            package_file=None,
            package_changelog_file=self.package_changelog_file,
            logger=self.package_logger
        )

        val = s2pp.package_changelog_version
        self.assertIsInstance(val, str)
        self.assertEqual(val, "9.8.7")

    def test_package_changelog_version_no_changelog(self) -> None:
        """Test package changelog version property"""
        val = self.s2pp.package_changelog_version
        self.assertIsInstance(val, str)
        self.assertEqual(val, '-1.-1.-1')

    def test_package_deps(self) -> None:
        """Test setup install_requires property"""
        val = self.s2pp.package_deps
        self.assertIsInstance(val, list)
        self.assertEqual(val,
                         self.test_package_expectation['install_requires'])

        self.s2pp._setup_data.pop('install_requires')
        val = self.s2pp.package_deps
        self.assertIsInstance(val, list)
        self.assertEqual(val, [])

    def test_package_url(self) -> None:
        """Test setup URL property"""
        val = self.s2pp.package_url
        self.assertIsInstance(val, str)
        self.assertEqual(val, self.test_package_expectation['url'])

        self.s2pp._setup_data.pop('url')
        with self.assertRaises(SystemExit) as context:
            val = self.s2pp.package_url

        self.assertEqual(context.exception.code, 'Project URL is mandatory')

    def test_package_files(self) -> None:
        """Test setup packages property"""
        val = self.s2pp.package_files
        self.assertIsInstance(val, list)
        self.assertEqual(len(val), len(self.package_files_expectation))

        self.assertTrue(all(isinstance(ele, Path) for ele in val))
        self.assertEqual(sorted(val), sorted(self.package_files_expectation))

        self.s2pp._setup_data.pop('packages')
        val = self.s2pp.package_files
        self.assertIsInstance(val, list)
        self.assertEqual(len(val), 0)
        self.assertEqual(val, [])

    def test_data_files(self) -> None:
        """Test setup data_files property"""
        val = self.s2pp.data_files
        self.assertIsInstance(val, list)
        self.assertEqual(len(val), len(self.data_files_expectation))

        self.assertTrue(all(isinstance(ele, Path) for ele in val))
        self.assertEqual(val, self.data_files_expectation)

        self.s2pp._setup_data.pop('data_files')
        val = self.s2pp.data_files
        self.assertIsInstance(val, list)
        self.assertEqual(len(val), 0)
        self.assertEqual(val, [])

    def test__create_url_elements(self) -> None:
        """Test creation of package URL elements"""
        expectation_base_url = 'base.com/url'
        package_files = [
            'asdf.py',
            'index.txt',
            'sub/dir/bar.py',
            'files/index.tpl',
        ]

        urls = self.s2pp._create_url_elements(package_files=package_files,
                                              url=expectation_base_url)

        self.assertIsInstance(urls, list)
        self.assertTrue(all(isinstance(ele, list) for ele in urls))
        self.assertTrue(all(len(ele) == 2 for ele in urls))
        self.assertEqual(len(urls), len(package_files))

        for expectation, ele in zip(package_files, urls):
            this_expectation = [
                expectation,
                expectation_base_url + '/' + expectation
            ]
            self.assertEqual(this_expectation, ele)

    @params(
        (True),
        (False),
    )
    def test_package_data(self, use_package_changelog_file: bool) -> None:
        """Test package data creation"""
        self.package_logger.disabled = True

        package_changelog_file = None
        if use_package_changelog_file:
            package_changelog_file = self.package_changelog_file
            self.test_package_expectation['version'] = '9.8.7'

        s2pp = Setup2uPyPackage(
            setup_file=self.setup_file,
            package_file=None,
            package_changelog_file=package_changelog_file,
            logger=self.package_logger
        )
        package_data = s2pp.package_data

        expected_keys = ['urls', 'deps', 'version']
        self.assertTrue(all(ele in package_data) for ele in expected_keys)
        self.assertEqual(package_data['version'],
                         self.test_package_expectation['version'])

        self.assertEqual(package_data['deps'],
                         self.test_package_expectation['install_requires'])

        all_files = \
            self.data_files_expectation + self.package_files_expectation
        base_url = \
            self.test_package_expectation['url'].replace('https://github.com/',
                                                         'github:')

        for expectation, ele in zip(sorted(all_files),
                                    sorted(package_data['urls'])):
            this_expectation = [
                str(expectation),
                base_url + '/' + str(expectation)
            ]
            self.assertIsInstance(ele, list)
            self.assertEqual(len(ele), 2)   # consist of [path, url]
            self.assertEqual(this_expectation, ele)

    def test_package_json_data(self) -> None:
        """Test package.json data property"""
        with self.assertRaises(Setup2uPyPackageError) as context:
            val = self.s2pp.package_json_data

        self.assertEqual(str(context.exception),
                         "No package.json data specified")

        s2pp = Setup2uPyPackage(
            setup_file=self.setup_file,
            package_file=self.package_file,
            package_changelog_file=None,
            logger=self.package_logger
        )
        val = s2pp.package_json_data
        self.assertIsInstance(val, dict)

    def test_validate(self) -> None:
        """Test validation of existing package.json against setup.py file"""
        self.package_logger.disabled = True

        s2pp = Setup2uPyPackage(
            setup_file=self.setup_file,
            package_file=self.package_file,
            package_changelog_file=None,
            logger=self.package_logger
        )
        is_valid = s2pp.validate()
        if is_valid:
            self.assertTrue(is_valid)
        else:
            self.test_logger.warning(s2pp.validation_diff)

        # check for differently sorted URL list entries
        shuffeled_package_json_data = dict(s2pp.package_json_data)
        shuffle(shuffeled_package_json_data["urls"])
        self.assertNotEqual(
            shuffeled_package_json_data["urls"],
            s2pp.package_json_data
        )
        with patch('setup2upypackage.setup2upypackage.Setup2uPyPackage.package_json_data', new_callable=PropertyMock) as patched:     # noqa: E501
            patched.return_value = shuffeled_package_json_data
            is_valid = s2pp.validate()
            if is_valid:
                self.assertTrue(is_valid)
            else:
                self.test_logger.warning(s2pp.validation_diff)

        # check for different version entries
        diff_version_package_json_data = dict(s2pp.package_json_data)
        diff_version_package_json_data["version"] = "93.10.22"
        self.assertNotEqual(
            diff_version_package_json_data["version"],
            s2pp.package_json_data
        )
        with patch('setup2upypackage.setup2upypackage.Setup2uPyPackage.package_json_data', new_callable=PropertyMock) as patched:     # noqa: E501
            patched.return_value = diff_version_package_json_data
            is_valid = s2pp.validate(ignore_version=True)
            if is_valid:
                self.assertTrue(is_valid)
            else:
                self.test_logger.warning(s2pp.validation_diff)

        # check for different dependencies entries
        diff_deps_package_json_data = dict(s2pp.package_json_data)
        diff_deps_package_json_data["deps"] = [
            "github:brainelectronics/dependency_1",
            "github:brainelectronics/dependency_2"
        ]
        self.assertNotEqual(
            diff_deps_package_json_data["deps"],
            s2pp.package_json_data
        )
        with patch('setup2upypackage.setup2upypackage.Setup2uPyPackage.package_json_data', new_callable=PropertyMock) as patched:     # noqa: E501
            patched.return_value = diff_deps_package_json_data
            is_valid = s2pp.validate(ignore_deps=True)
            if is_valid:
                self.assertTrue(is_valid)
            else:
                self.test_logger.warning(s2pp.validation_diff)

    @unittest.skip("Not yet implemented")
    def test_validation_diff(self) -> None:
        """Test validation difference property"""
        pass

    @params(
        ("asdf.json", False),   # path, pretty
        ("qwertz.json", True),
        (None, False),
        (None, True)
    )
    @patch('setup2upypackage.setup2upypackage.Setup2uPyPackage.package_data',
           new_callable=PropertyMock)
    def test_create(self,
                    path: str,
                    pretty: bool,
                    package_data: PropertyMock) -> None:
        """Test package.json creation"""
        self.package_logger.disabled = True

        test_data = {"asdf": 123}
        package_data.return_value = test_data
        if pretty:
            expectation = json.dumps(test_data, indent=4)
        else:
            expectation = json.dumps(test_data)

        output_path = path
        if path is None:
            output_path = self._here / 'data' / 'package.json'

        m = mock_open()
        with patch('setup2upypackage.setup2upypackage.open', m, create=False):
            self.s2pp.create(output_path=path, pretty=pretty)

        m.assert_called_once_with(output_path, 'w')
        handle = m()
        self.assertEqual(handle.write.call_args.args[0], expectation)


if __name__ == '__main__':
    unittest.main()
