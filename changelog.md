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
[Unreleased]: https://github.com/brainelectronics/micropython-package-validation/compare/0.2.0...main

[0.2.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.2.0
[0.1.1]: https://github.com/brainelectronics/micropython-package-validation/tree/0.1.1
[0.1.0]: https://github.com/brainelectronics/micropython-package-validation/tree/0.1.0
