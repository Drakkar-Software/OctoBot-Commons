# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.3] - 2020-02-03
### Updated
- numpy requirement

## [1.5.2] - 2020-01-30
### Updated
- Profiles duplication path

## [1.5.1] - 2020-12-23
### Updated
- Profiles import

## [1.5.0] - 2020-12-23
### Added
- Profiles management

## [1.4.15] - 2020-12-10
### Fixed
- trading configuration keys import

## [1.4.14] - 2020-12-08
### Updated
- migrate trading config keys into octobot-commons

## [1.4.13] - 2020-12-06
### Updated
- requirements: removed telegram requirement

## [1.4.12] - 2020-12-06
### Updated
- config.json test file

## [1.4.11] - 2020-11-26
### Added
- Thread util module

## [1.4.10] - 2020-11-25
### Updated
- Remove multi-session-profitability from default config

## [1.4.9] - 2020-11-20
### Fixed
- Number pretty printer

## [1.4.8] - 2020-11-08
### Updated
- Metrics url

## [1.4.7] - 2020-11-06
### Updated
- CI to github actions

## [1.4.6] - 2020-10-29
### Updated
- Numpy requirements

## [1.4.5] - 2020-10-24
### Updated
- Requirements

## [1.4.4] - 2020-10-23
### Added
- disable method on BotLogger

## [1.4.3] - 2020-10-23
### Updated
- Release process

## [1.4.2] - 2020-10-23
### Updated
- Python 3.8

## [1.4.1] - 2020-10-04
### Updated
- Requirements

## [1.4.0] - 2020-10-04
### Changed
- Imports

## [1.3.46] - 2020-09-02
### Updated
- AsyncJob exception handling

## [1.3.45] - 2020-08-27
### Fixed
- AsyncJob timers

## [1.3.44] - 2020-08-27
### Added
- AsyncJob

## [1.3.43] - 2020-08-15
### Updated
- Requirements

## [1.3.42] - 2020-08-13
### Removed
- Fix pretty printer typing issue 

## [1.3.41] - 2020-07-25
### Removed
- search_class_name_in_class_list from tentacles manager 

## [1.3.40] - 2020-06-28
### Updated
- Requirements

## [1.3.39] - 2020-06-27
### Fixed
- Errors counter

## [1.3.38] - 2020-06-19
### Updated
- Requirements

## [1.3.37] - 2020-06-09
### Updated
- Asyncio tools ErrorContainer

## [1.3.36] - 2020-06-02
### Added
- Asyncio tool wait_for_task_to_perform

## [1.3.35] - 2020-06-02
### Added
- get_password_hash

## [1.3.34] - 2020-05-27
### Update
- Cython version

## [1.3.33] - 2020-05-20
### Update
- Take config schema as argument in config management

## [1.3.32] - 2020-05-19
### Fixed
- Cython header

## [1.3.31] - 2020-05-16
### Updated
- Requirements

## [1.3.30] - 2020-05-14
### Added
- [Enums] ChannelConsumerPriorityLevels

## [1.3.29] - 2020-05-13
### Fixed
- [PrettyPrinter] Fix trade_pretty_printer cython header

## [1.3.28] - 2020-05-12
### Fixed
- [Logging] Fix get_backtesting_errors_count cython header

## [1.3.27] - 2020-05-11
### Added
- [ConfigUtil] Decrypt util function

## [1.3.26] - 2020-05-11
### Added
- [CI] Azure pipeline

### Removed
- [CI] macOs build on travis
- [CI] Appveyor builds

## [1.3.25] - 2020-05-10
### Updated
- Telegram requirements

## [1.3.24] - 2020-05-09
### Added
- OctoBotChannel subjects enum

## [1.3.23] - 2020-05-09
### Fixed
- Evaluators channels name

## [1.3.22] - 2020-05-09
### Added
- OctoBot channel name

## [1.3.21] - 2020-05-08
### Update
- improve asyncio ErrorContainer

## [1.3.20] - 2020-05-08
### Fixed
- asyncio ErrorContainer

## [1.3.19] - 2020-05-07
### Added
- asyncio ErrorContainer

## [1.3.18] - 2020-05-06
### Fixed
- Logging_util compiled errors

## [1.3.17] - 2020-05-05
### Fixed
- Logging_util cython headers

## [1.3.16] - 2020-05-03
### Added
- time_frame_manager cythonization and tests
- symbol_util cythonization

## [1.3.15] - 2020-05-03
### Removed
- [EventTree] Events management

## [1.3.14] - 2020-05-02
### Added
- list_util file with flatten_list method

## [1.3.13] - 2020-04-30
### Added
- Pylint and Black code style checkers

### Fixed
- Code style issues

### Removed
- Singleton annotation
- get_value_or_default replaced by native dict.get

## [1.3.12] - 2020-04-27
### Updated
- Cython requirement

## [1.3.11] - 2020-04-23
### Updated
- [DataUtil] Improve shift implementation

## [1.3.10] - 2020-04-16
### Added
- Evaluators channel name
- [EventTree] node value time

### Fixed
- [EventTree] event clearing too early
- [EventTree] syntax

### Removed
- AbtractEvaluator default description

## [1.3.9] - 2020-04-10
### Fixed
- Missing constant

## [1.3.8] - 2020-04-08
### Removed
- AbstractTentacle cythonization

## [1.3.7] - 2020-04-07
### Fixed
- Wildcard imports

## [1.3.6] - 2020-03-25
### Updated
- Tentacles management to include OctoBot-tentacles-manager

## [1.3.5] - 2020-03-25
### Updated
- [Requirement] cython to 0.29.16
- [Requirement] numpy to 0.18.2
- [Requirement] jsonschema to 3.2.0
- [Requirement] python-telegram-bot to 12.4.2

## [1.3.4] - 2020-03-22
### Added
- Liquidations, Mini ticker and Book ticker Channels name

## [1.3.3] - 2020-03-15
### Added
- Datetime to timestamp conversion

## [1.3.2] - 2020-03-14
### Added
- Funding Channel name

## [1.3.1] - 2020-03-07
### Added
- Margin Portfolio key

## [1.3.0] - 2020-03-05
### Added
- Error message to exception logger

### Fixed
- Trade prettyprinter format

## [1.2.3] - 2020-02-16
### Added
- shift_value_array function to shift a numpy array
- Cythonized numpy array functions
- Error notifier callback 

### Changed
- Minimal time frame is now 1 min 
- Update pretty_printer for the new Trade attributes

## [1.2.2] - 2020-01-04
### Changed
- Pretty printer cryptocurrencies alert refresh

### Fixed
- MarkdownFormat comparison error

## [1.2.1] - 2020-01-02
### Added
- Asyncio run_coroutine_in_asyncio_loop method
- External resources management
- Tentacle and classes management utility methods
- Configuration file management

### Changed
- Pretty printer typo fix 

## [1.2.0] - 2019-12-18
### Added
- Tests from OctoBot < 0.4.0
- Number Util float rounding method
- Evaluators_util cython compilation

### Changed
- TimeFrameManager static methods to function only
- DataUtil static methods to function only
- Evaluator_util check_eval_note returns only boolean

### Removed
- Travis build stage

## [1.1.53] - 2019-12-17
### Added
- Makefile

### Fixed
- SegFault : Temporary disable abstract_tentacle cython compilation

## [1.1.52] - 2019-12-14
###  Added
- EventTree NodeExistsError exception

## [1.1.51] - 2019-12-14
### Added
- EventTree methods relative node param
- EventTree get without creation method

## [1.1.50] - 2019-12-11
### Added
- EventTree with EventNode classes
- tests EventTree methods

## [1.1.49] - 2019-11-07
## Updated
- Cython version to 0.29.14

## [1.1.48] - 2019-10-21
### Added
- OSX support

## [1.1.47] - 2019-10-19
### Added
- OS tools

## [1.1.46] - 2019-10-09
### Changed
- Code cleanup

## [1.1.45] - 2019-10-09
### Added
- Appveyor CI

## [1.1.44] - 2019-10-09
### Added
- PyPi manylinux deployment

## [1.1.43] - 2019-10-08
### Fixed
- Install with setup

## [1.1.42] - 2019-10-03
### Added
- Advanced Manager new search methods

## [1.1.41] - 2019-10-02
### Added
- Time constants

## [1.1.40] - 2019-09-26
### Added
- Inspector deep method by subclasses

## [1.1.39] - 2019-09-26
### Added
- Inspector method by subclasses

## [1.1.38] - 2019-09-25
### Fixed
- Setup installation

## [1.1.37] - 2019-09-21
### Added
- class_inspector default_parents_inspection method

## [1.1.36] - 2019-09-18
### Added
- class_inspector cython compilation

### Changed
- 'default_parent_inspection' to public

## [1.1.35] - 2019-09-17
### Changed
- TIME_CHANNEL to backtesting names

## [1.1.34] - 2019-09-12
### Fixed
- is_valid_timestamp method exception

## [1.1.33] - 2019-09-01
### Fixed
- Adapted config manager from OctoBot core

## [1.1.32] - 2019-08-27
### Added
- Tentacle config manager

## [1.1.31] - 2019-08-18
### Removed
- Abstract tentacle pxd file

## [1.1.30] - 2019-08-17
### Removed
- Advanced manager class

## [1.1.29] - 2019-08-16
### Changed
- Generify & cythonize advanced_manager

## [1.1.28] - 2019-08-16
### Added
- Evaluator util

## [1.1.27] - 2019-08-15
### Added
- Future tentacles constants declaration

## [1.1.26] - 2019-08-15
### Added
- Abstract tentacle cython declaration

## [1.1.25] - 2019-08-15
### Added
- OctoBot custom errors (can be used to except elsewhere)

## [1.1.24] - 2019-08-15
### Added
- Tentacles commons constants

## [1.1.23] - 2019-08-15
### Added
- Common channels name

## [1.1.22] - 2019-08-14
### Fixed
- Singleton Class instances attribute declaration

## [1.1.21] - 2019-08-14
### Changed
- Singleton Class implementation

## [1.1.20] - 2019-08-14
### Added
- Singleton Class
- Cython compilation

### Changed
- Moved singleton.py to singleton/singleton_annotation.py

## [1.1.19] - 2019-08-14
### Changed
- AdvancedManager fully split Evaluators and Trading tentacles classes list initialization

## [1.1.18] - 2019-08-07
### Added
- ConfigManager from OctoBot main repository

### Changed
- AdvancedManager tentacle initialization is now splitted between Evaluators and Trading

## [1.1.17] - 2019-08-06
### Added
- Constants from OctoBot-Tentacles-Manager

## [1.1.16] - 2019-08-05
### Changed
- Tentacles management imports to prepare OctoBot-Tentacles-Manager migration to commons

## [1.1.15] - 2019-08-05
### Added
- Config load methods
- 6h time frame in TimeFrames enums

## [1.1.14] - 2019-08-01
### Changed
- Adapt pretty printer to OctoBot-Trading callbacks (exchange name)
- Updated order and trade instance getters/property compatibilities

## [1.1.13] - 2019-06-23
### Changed
- Catch split_symbol index error exception

## [1.1.12] - 2019-06-09
### Added
- Encrypt and decrypt functions

## [1.1.11] - 2019-06-08
### Added
- Config util

## [1.1.10] - 2019-06-08
### Added
- Data util
- Numpy requirement

## [1.1.9] - 2019-06-06
### Added
- Trading constants from OctoBot constants

## [1.1.8] - 2019-06-05
### Added
- TimeFrames enums
- TimeFrame manager

## [1.1.7] - 2019-06-05
### Added
- dict util methods

### Removed
- Initializable class

## [1.1.6] - 2019-06-05
### Added
- pretty printer

## [1.1.5] - 2019-06-02
### Changed
- convert_symbol new optionnal parameter should_lowercase with False as default value 

## [1.1.4] - 2019-06-01
### Added
- convert_symbol method to manage separator between symbol formats
### Changed
- merge_currencies with a new additional parameter "separator" with MARKET_SEPARATOR as default value

## [1.1.3] - 2019-05-27
### Added
- Manifest

## [1.1.2] - 2019-05-27
### Added
- Symbol utils
- Initializable class
