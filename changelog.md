# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [x.y.z] - yyyy-mm-dd
### Added
### Changed
### Removed
### Fixed
-->
<!--
RegEx for release version from file
r"^\#\# \[\d{1,}[.]\d{1,}[.]\d{1,}\] \- \d{4}\-\d{2}-\d{2}$"
-->

## Released
## [0.7.0] - 2026-04-28
### Added
- The CLI arg `--package_file_glob` allows using a different glob pattern than the default `*.py` for adding package files from within the directory specified at `packages` in `setup.py`. For a mpy-cross compiled package the arg `--package_file_glob` should be set to `*.mpy`
- Add debug log messages to `validate` function

## [0.6.1] - 2026-04-28
### Fixed
- Raise a `FileNotFoundError` if the specified `package_file` is not found during validation. The file will be created with the `--create` option without throwing an error due to non-existance on CLI arg parsing level.

## [0.6.0] - 2026-04-27
### Added
- `.python-version` to use repo this with pyenv

### Changed
- Bump all package versions to their latest version supporting Python 3.9
- Mention Python 3.11 and 3.12 support in `setup.py`

### Fixed
- Silence all yamllint warnings

## [0.5.1] - 2026-04-27
### Fixed
- This change creates the correct release candidate number based on the action run of a pull request workflow run `test-release` instead of the total number of this workflow run. By this fix, the `-rcX` metadata starts at `1` and is incremented with every push, no matter if the push is a force push or a classic new commit on top in a ongoing pull request.
- Update external action versions to latest available version
- Fix license specification in `setup.py` file
- Check all files in `dist/`, not only `*.tar.gz`

## [0.5.0] - 2023-07-05
### Added
- pre-commit hook and config files

### Fixed
- Added missing empty line in several files

## [0.4.0] - 2023-06-10
### Added
- `*/boot.py` and `*/main.py` can be ignored during the check with `--ignore-boot-main`, see #8

## [0.3.0] - 2023-05-27
### Added
- Dependencies of package can be ignored during the check with `--ignore-deps`, see #5

## [0.2.0] - 2023-05-27
### Added
- Version of package can be ignored during the check with `--ignore-version`, see #4

## [0.1.1] - 2023-04-18
### Fixed
- Sort URL list elements before comparing `package.json` and returned `setup.py` data, see #2

## [0.1.0] - 2023-03-27
### Added
- `setup2upypackage` module
- Examples and documentation
- Unittest files

### Changed
- Several updates on setup and config files different than the template repo

### Removed
- Not used files provided with [template repo](https://github.com/brainelectronics/micropython-i2c-lcd)

<!-- Links -->
[Unreleased]: https://github.com/brainelectronics/micropython-package-validation/compare/0.7.0...main

[0.7.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.7.0
[0.6.1]: https://github.com/brainelectronics/micropython-package-validation/tree/0.6.1
[0.6.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.6.0
[0.5.1]: https://github.com/brainelectronics/micropython-package-validation/tree/0.5.1
[0.5.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.5.0
[0.4.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.4.0
[0.3.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.3.0
[0.2.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.2.0
[0.1.1]: https://github.com/brainelectronics/micropython-package-validation/tree/0.1.1
[0.1.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.1.0
