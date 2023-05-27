#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Create and validate MicroPython package.json files based on Python setup.py
files
"""

import json
import logging
import sys
from distutils.core import run_setup
from pathlib import Path
from typing import List, Optional

from changelog2version.extract_version import ExtractVersion
from deepdiff import DeepDiff
from mock import Mock


class Setup2uPyPackageError(Exception):
    """Base class for exceptions in this module."""
    pass


class Setup2uPyPackage(object):
    """Handle MicroPython package JSON creation and validation"""

    def __init__(self,
                 setup_file: Path,
                 package_file: Optional[Path],
                 package_changelog_file: Optional[Path],
                 logger: Optional[logging.Logger] = None) -> None:
        """
        Init Setup2uPyPackage class

        :param      setup_file:    The setup.py file
        :type       setup_file:    Path
        :param      package_file:  The package.json file
        :type       package_file:  Optional[Path]
        :param      package_file:  The package changelog file
        :type       package_file:  Optional[Path]
        :param      logger:        Logger object
        :type       logger:        Optional[logging.Logger]
        """
        if logger is None:
            logger = self._create_logger()
        self._logger = logger

        self._setup_file = setup_file
        self._package_file = package_file
        self._package_changelog_file = package_changelog_file

        self._setup_data = {}
        self._root_dir = self._setup_file.parent

        self._setup_data = self._parse_setup_file_content()

    @staticmethod
    def _create_logger(logger_name: str = None) -> logging.Logger:
        """
        Create a logger

        :param      logger_name:  The logger name
        :type       logger_name:  str, optional

        :returns:   Configured logger
        :rtype:     logging.Logger
        """
        custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                        ' %(funcName)-15s:%(lineno)4s] %(message)s'

        # configure logging
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=sys.stdout)

        if logger_name and (isinstance(logger_name, str)):
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger(__name__)

        # set the logger level to DEBUG if specified differently
        logger.setLevel(logging.DEBUG)

        return logger

    def _parse_setup_file_content(self) -> dict:
        """
        Parse setup.py file content

        see https://stackoverflow.com/a/61754034/13543363

        :returns:   Parsed setup.py file content
        :rtype:     dict
        """
        sys.modules['sdist_upip'] = Mock()
        res = run_setup(self._setup_file, stop_after="init")

        kwargs = res.__dict__
        kwargs.update(kwargs['metadata'].__dict__)

        return kwargs

    @property
    def package_version(self) -> str:
        """
        Get version of package based on setup.py "version" entry

        :returns:   Package version based on setup.py "version" entry
        :rtype:     str
        """
        if self._setup_data.get('version', ""):
            return self._setup_data['version']
        else:
            self._logger.warning("No 'version' key found in setup data dict")
            return "-1.-1.-1"

    @property
    def package_changelog_version(self) -> str:
        """
        Get package changelog version

        :returns:   Package changelog version
        :rtype:     str
        """
        if self._package_changelog_file:
            ev = ExtractVersion(logger=self._logger)

            version_line = ev.parse_changelog(
                changelog_file=self._package_changelog_file
            )
            semver_string = ev.parse_semver_line(
                release_version_line=version_line
            )

            return semver_string
        else:
            self._logger.warning("No package changelog file specified")
            return "-1.-1.-1"

    @property
    def package_deps(self) -> List[str]:
        """
        Get dependencies of package based on setup.py "install_requires" entry

        :returns:   Package dependencies based on setup.py "install_requires"
        :rtype:     List[str]
        """
        if self._setup_data.get('install_requires', []):
            return self._setup_data['install_requires']
        else:
            self._logger.warning(
                "No 'install_requires' key found in setup data dict"
            )
            return []

    @property
    def package_url(self) -> str:
        """
        Get URL of package based on setup.py "url" entry.

        :returns:   Package URL based on setup.py "url" entry
        :rtype:     str
        """
        if self._setup_data.get('url', ""):
            return self._setup_data['url']
        else:
            self._logger.warning("No 'url' key found in setup data dict")
            raise SystemExit('Project URL is mandatory')

    @property
    def package_files(self) -> List[str]:
        """
        Get packages based on setup.py "packages" entry.

        :returns:   Packages based on setup.py "packages" entry
        :rtype:     List[str]
        """
        packages = []
        all_files = []
        root_dir = self._root_dir

        if self._setup_data.get('packages', []):
            packages = self._setup_data['packages']
        else:
            self._logger.warning("No 'packages' key found in setup data dict")
            return []

        for package in packages:
            p = root_dir.glob('{}/*.py'.format(package))
            files = [x.relative_to(root_dir) for x in p if x.is_file()]
            all_files.extend(files)

        return all_files

    @property
    def data_files(self) -> List[str]:
        """
        Get data files based on setup.py "data_files" entry.

        :returns:   Data files based on setup.py "data_files" entry
        :rtype:     List[str]
        """
        data_files = []
        all_files = []
        root_dir = self._root_dir

        if self._setup_data.get('data_files', []):
            data_files = self._setup_data['data_files']
        else:
            self._logger.warning(
                "No 'data_files' key found in setup data dict"
            )
            return []

        for folder, file_list in data_files:
            files = []
            for file in file_list:
                file = root_dir / Path(file)
                if file.is_file():
                    files.append(file.relative_to(root_dir))
            all_files.extend(files)

        return all_files

    def _create_url_elements(self,
                             package_files: List[str],
                             url: str) -> List[str]:
        """
        Create URLs to all package elements.

        :param      package_files:  The package files
        :type       package_files:  List[str]
        :param      url:            The URL
        :type       url:            str

        :returns:   List of URLs to download the package files
        :rtype:     List[str]
        """
        urls = []

        for file in package_files:
            this_url = [
                str(file),
                str(Path(url) / file)
            ]
            self._logger.debug("File elements: {}: {}".format(file, this_url))
            urls.append(this_url)

        return urls

    @property
    def package_data(self) -> dict:
        """
        Get mip compatible package data

        :returns:   mip compatible package.json data
        :rtype:     dict
        """
        urls = []
        package_data = {
            "urls": [],
            "deps": [],
            "version": "-1.-1.-1"
        }
        if self._package_changelog_file:
            version = self.package_changelog_version
        else:
            version = self.package_version
        install_requires = self.package_deps
        package_files = self.package_files
        data_files = self.data_files
        url = self.package_url.replace('https://github.com/', 'github:')
        for x in [package_files, data_files]:
            urls.extend(self._create_url_elements(package_files=x, url=url))

        self._logger.debug("version: {}".format(version))
        self._logger.debug("install_requires: {}".format(install_requires))
        self._logger.debug("package_files: {}".format(package_files))
        self._logger.debug("data_files: {}".format(data_files))
        self._logger.debug("url: {}".format(url))
        self._logger.debug("urls: {}".format(urls))

        package_data["urls"] = urls
        package_data["deps"] = install_requires
        package_data["version"] = version

        return package_data

    @property
    def package_json_data(self) -> dict:
        """
        Get package.json data

        :returns:   Existing package.json data
        :rtype:     dict
        """
        existing_data = {}

        if self._package_file:
            with open(self._package_file, 'r') as f:
                existing_data = json.load(f)
        else:
            raise Setup2uPyPackageError("No package.json data specified")

        return existing_data

    def validate(self,
                 ignore_version: bool = False,
                 ignore_deps: bool = False) -> bool:
        """
        Validate existing package.json with setup.py based data

        :param      ignore_version:  Indicates if the version is ignored
        :type       ignore_version:  bool
        :param      ignore_deps:     Indicates if the dependencies are ignored
        :type       ignore_deps:     bool

        :returns:   Result of validation, True on success, False otherwise
        :rtype:     bool
        """
        # list of URL entries might be sorted differently
        package_json_data = dict(self.package_json_data)
        package_data = dict(self.package_data)

        if ignore_version:
            package_json_data.pop("version")
            package_data.pop("version")

        if ignore_deps:
            package_json_data.pop("deps")
            package_data.pop("deps")

        package_json_data.get("urls", []).sort()
        package_data.get("urls", []).sort()

        return package_json_data == package_data

    @property
    def validation_diff(self) -> DeepDiff:
        """
        Get difference of package.json and setup.py

        :returns:   The deep difference.
        :rtype:     DeepDiff
        """
        return DeepDiff(self.package_data, self.package_json_data)

    def create(self,
               output_path: Optional[Path] = None,
               pretty: bool = True) -> None:
        """
        Create package.json file in same directory as setup.py

        :param      output_path:  The output path
        :type       output_path:  Optional[Path]
        :param      pretty:       Flag to use an indentation of 4
        :type       pretty:       bool
        """
        if not output_path:
            if self._package_file:
                output_path = self._package_file
            else:
                output_path = self._setup_file.parent / 'package.json'
                self._logger.info(
                    "No package.json data specified, using setup.py directory"
                )

        with open(output_path, 'w') as file:
            if pretty:
                file.write(json.dumps(self.package_data, indent=4))
            else:
                file.write(json.dumps(self.package_data))

        self._logger.debug("Created {}".format(output_path))
