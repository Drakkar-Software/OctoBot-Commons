# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.49] - 2019-11-07
## Updated
- Cython version to 0.29.14

## [1.1.48] - 2019-10-21
## Added
- OSX support

## [1.1.47] - 2019-10-19
## Added
- OS tools

## [1.1.46] - 2019-10-09
## Changed
- Code cleanup

## [1.1.45] - 2019-10-09
## Added
- Appveyor CI

## [1.1.44] - 2019-10-09
## Added
- PyPi manylinux deployment

## [1.1.43] - 2019-10-08
## Fixed
- Install with setup

## [1.1.42] - 2019-10-03
## Added
- Advanced Manager new search methods

## [1.1.41] - 2019-10-02
## Added
- Time constants

## [1.1.40] - 2019-09-26
## Added
- Inspector deep method by subclasses

## [1.1.39] - 2019-09-26
## Added
- Inspector method by subclasses

## [1.1.38] - 2019-09-25
## Fixed
- Setup installation

## [1.1.37] - 2019-09-21
## Added
- class_inspector default_parents_inspection method

## [1.1.36] - 2019-09-18
## Added
- class_inspector cython compilation

## Changed
- 'default_parent_inspection' to public

## [1.1.35] - 2019-09-17
## Changed
- TIME_CHANNEL to backtesting names

## [1.1.34] - 2019-09-12
## Fixed
- is_valid_timestamp method exception

## [1.1.33] - 2019-09-01
## Fixed
- Adapted config manager from OctoBot core

## [1.1.32] - 2019-08-27
## Added
- Tentacle config manager

## [1.1.31] - 2019-08-18
## Removed
- Abstract tentacle pxd file

## [1.1.30] - 2019-08-17
## Removed
- Advanced manager class

## [1.1.29] - 2019-08-16
## Changed
- Generify & cythonize advanced_manager

## [1.1.28] - 2019-08-16
## Added
- Evaluator util

## [1.1.27] - 2019-08-15
## Added
- Future tentacles constants declaration

## [1.1.26] - 2019-08-15
## Added
- Abstract tentacle cython declaration

## [1.1.25] - 2019-08-15
## Added
- OctoBot custom errors (can be used to except elsewhere)

## [1.1.24] - 2019-08-15
## Added
- Tentacles commons constants

## [1.1.23] - 2019-08-15
## Added
- Common channels name

## [1.1.22] - 2019-08-14
## Fixed
- Singleton Class instances attribute declaration

## [1.1.21] - 2019-08-14
## Changed
- Singleton Class implementation

## [1.1.20] - 2019-08-14
## Added
- Singleton Class
- Cython compilation

## Changed
- Moved singleton.py to singleton/singleton_annotation.py

## [1.1.19] - 2019-08-14
## Changed
- AdvancedManager fully split Evaluators and Trading tentacles classes list initialization

## [1.1.18] - 2019-08-07
## Added
- ConfigManager from OctoBot main repository

## Changed
- AdvancedManager tentacle initialization is now splitted between Evaluators and Trading

## [1.1.17] - 2019-08-06
## Added
- Constants from OctoBot-Tentacles-Manager

## [1.1.16] - 2019-08-05
## Changed
- Tentacles management imports to prepare OctoBot-Tentacles-Manager migration to commons

## [1.1.15] - 2019-08-05
## Added
- Config load methods
- 6h time frame in TimeFrames enums

## [1.1.14] - 2019-08-01
## Changed
- Adapt pretty printer to OctoBot-Trading callbacks (exchange name)
- Updated order and trade instance getters/property compatibilities

## [1.1.13] - 2019-06-23
## Changed
- Catch split_symbol index error exception

## [1.1.12] - 2019-06-09
## Added
- Encrypt and decrypt functions

## [1.1.11] - 2019-06-08
## Added
- Config util

## [1.1.10] - 2019-06-08
## Added
- Data util
- Numpy requirement

## [1.1.9] - 2019-06-06
## Added
- Trading constants from OctoBot constants

## [1.1.8] - 2019-06-05
## Added
- TimeFrames enums
- TimeFrame manager

## [1.1.7] - 2019-06-05
## Added
- dict util methods

## Removed
- Initializable class

## [1.1.6] - 2019-06-05
## Added
- pretty printer

## [1.1.5] - 2019-06-02
## Changed
- convert_symbol new optionnal parameter should_lowercase with False as default value 

## [1.1.4] - 2019-06-01
### Added
- convert_symbol method to manage separator between symbol formats
## Changed
- merge_currencies with a new additional parameter "separator" with MARKET_SEPARATOR as default value

## [1.1.3] - 2019-05-27
### Added
- Manifest

## [1.1.2] - 2019-05-27
### Added
- Symbol utils
- Initializable class
