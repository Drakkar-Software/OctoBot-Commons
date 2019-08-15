# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
