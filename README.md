# MicroPython Package Validation

[![Downloads](https://pepy.tech/badge/micropython-package-validation)](https://pepy.tech/project/micropython-package-validation)
![Release](https://img.shields.io/github/v/release/brainelectronics/micropython-package-validation?include_prereleases&color=success)
![Python](https://img.shields.io/badge/python3-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/brainelectronics/micropython-package-validation/branch/main/graph/badge.svg)](https://app.codecov.io/github/brainelectronics/micropython-package-validation)
[![CI](https://github.com/brainelectronics/micropython-package-validation/actions/workflows/release.yml/badge.svg)](https://github.com/brainelectronics/micropython-package-validation/actions/workflows/release.yml)

Validate and create MicroPython package JSON file

---------------

## General

MicroPython Package Validation for mip package.json files

📚 The latest documentation is available at
[MicroPython Package Validation ReadTheDocs][ref-rtd-micropython-package-validation] 📚

<!-- MarkdownTOC -->

- [Installation](#installation)
    - [Install required tools](#install-required-tools)
- [Installation](#installation-1)
- [Usage](#usage)
    - [Validate](#validate)
        - [Validate package JSON file](#validate-package-json-file)
        - [Validate package JSON file from changelog](#validate-package-json-file-from-changelog)
    - [Create](#create)
        - [Create package JSON file](#create-package-json-file)
            - [Create specific package JSON file](#create-specific-package-json-file)
        - [Create package JSON file from changelog](#create-package-json-file-from-changelog)
- [Contributing](#contributing)
    - [Unittests](#unittests)
- [Credits](#credits)

<!-- /MarkdownTOC -->

## Installation

### Install required tools

Python3 must be installed on your system. Check the current Python version
with the following command

```bash
python --version
python3 --version
```

Depending on which command `Python 3.x.y` (with x.y as some numbers) is
returned, use that command to proceed.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Installation

```bash
pip install setup2upypackage
```

## Usage

### Validate
#### Validate package JSON file

The following command will exit with a non-zero code in case of a difference
between the generated (based on `setup.py`) and existing package
(`package.json`) content.

```bash
upy-package \
    --setup_file tests/data/setup.py \
    --package_changelog_file tests/data/sample_changelog.md \
    --package_file tests/data/package.json \
    --validate
```

#### Validate package JSON file from changelog

In case the package version is defined by a changelog and the `version` entry
of the `setup.py` file is filled on demand by e.g.
[changelog2version][ref-changelog2version], the semantic version changelog can
be specified explicitly to use its latest entry for the version value.

```bash
upy-package \
    --setup_file tests/data/setup.py \
    --package_changelog_file tests/data/sample_changelog.md \
    --package_file tests/data/package.json \
    --validate
```

### Create
#### Create package JSON file

The following command creates a `package.json` file in the same directory as
the specified `setup.py` file. The content of the `package.json` file is
additionally printed to stdout (`--print`) with an indentation of 4 (due to
the `--pretty` option)

```bash
upy-package \
    --setup_file tests/data/setup.py \
    --create \
    --print \
    --pretty
```

##### Create specific package JSON file

A specific package JSON file can be specified with the `--package_file`
parameter. The file has to exist before running the command.

```bash
upy-package \
    --setup_file tests/data/setup.py \
    --package_file tests/data/custom-package.json \
    --create \
    --print \
    --pretty
```

#### Create package JSON file from changelog

In case the package version is defined by a changelog and the `version` entry
of the `setup.py` file is filled on demand by e.g.
[changelog2version][ref-changelog2version], the semantic version changelog can
be specified explicitly to use its latest entry for the version value.

```bash
upy-package \
    --setup_file tests/data/setup.py \
    --package_changelog_file tests/data/sample_changelog.md \
    --create \
    --print \
    --pretty
```

## Contributing

### Unittests

Run the unittests locally with the following command after installing this
package in a virtual environment

```bash
# run all tests
nose2 --config tests/unittest.cfg

# run only one specific tests
nose2 tests.test_setup2upypackage.TestSetup2uPyPackage.test_package_version
```

Generate the coverage files with

```bash
python create_report_dirs.py
coverage html
```

The coverage report is placed at `reports/coverage/html/index.html`

## Credits

Based on the [PyPa sample project][ref-pypa-sample].

<!-- Links -->
[ref-rtd-micropython-package-validation]: https://micropython-package-validation.readthedocs.io/en/latest/
[ref-pypa-sample]: https://github.com/pypa/sampleproject
[ref-changelog2version]: https://github.com/brainelectronics/changelog2version
