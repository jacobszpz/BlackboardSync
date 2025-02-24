# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add support for Universidad Pablo de Olavide (@davidsollodp)
- Add support for University of Maryland, Baltimore County (@ghost)
- Add support for Syracuse University (@363843342)
- Add support for University of Illinois Chicago (@hoangngo-sudo)
- Add support for Università Bocconi (@giuliofrey)
- Timestamps are now added to the files downloaded (@Ovler-Young)

## [0.18.0] - 2024-10-22

### Added
- Images contained within descriptions are also downloaded
- Body descriptions can be shared via WebShare or email
- Add support for École Supérieure Privée d'Ingénierie et de Technologies (@TheLime1)
- Add support for Western Sydney University (Jo Miyeon)

### Fixed
- Links are now not assumed to have an 'href' attribute
- Avoid parsing empty descriptions
- Webdav filenames are URL decoded
- Documentation build at readthedocs.org
- Login browser cache and cookie storage

### Changed
- File logging level is now WARNING rather than ERROR
- Body descriptions have custom styling rather than pure html

## [0.17.4] - 2024-10-12

### Fixed
- Long paths on Windows for all operations
- PyPI distribution missing dependency
- Just handle any exception from download job

### Added
- Add support for University of Evansville (@lukebsa)
- Add support for The University of Edinburgh (@sanjacob)
- Add support for Glasgow Caledonian University (@sanjacob)
- Add support for Mid-State Technical College (@lint-os)

## [0.17.1] - 2024-09-22

### Fixed
- Name conflict between content and attachment
- Handle OSError in download workers
- Folder names should not contain dots

## [0.17.0] - 2024-09-20

### Changed
- Remove hardcoded minimum year in setup wizard
- Upgrade to PyQt6
- Remove internal blackboard api module, use `bblearn` instead
- Refactor download module into several content classes
- Improve testing and automated builds pipeline
- Upgrade multiple modules to latest versions
- Improve login browser experience
- Application name and id changed in PyInstaller builds
- macOS build now hides the dock icon (@depleur's suggestion)
- Assignment and lesson content now supported

### Added
- Add support for University of Pretoria (@whipped-cream)
- Add support for CUHK-Shenzhen (@Hyle33ies)
- Add support for University of Derby
- Add support for Texas Tech University (@kktrum)
- Add support for Seneca Polytechnic (@weihuang)
- Add support for University of Manchester (@d-dahir)
- Add support for University of York (@Laura7089)
- Add support for Curtin University (@JaydenDownes)
- Add support for Hong Kong Community College (@Benson-mk)
- Add support for OBS Business School (@luisvinatea)
- Add mock Blackboard instance for manual testing
- Automatic university detection based on ISP
- Add support for Shiv Nadar University (@depleur)
- Add support for University of Texas at Dallas (@JadedCtrl)
- Add support for Humber College Institute of Technology and Advanced Learning (@ColeAnthonyCapilongo5735)
- Add support for translations
- Add Spanish (es), French (fr), German (de) translations

### Fixed
- Unicode paths will be used by default on Windows
- Bug preventing settings window from opening
- API session is now first tested before downloading
- API authentication errors are now handled correctly
- Download errors are now handled better
- Errors that happen while streaming responses are now handled
- PyInstaller build is now smaller
- Overall app stability improved

## [0.11.4] - 2024-04-10

### Changed
- Minor updates to some development dependencies

### Added
- Add support for Griffith University (@KR3dwood)

## [0.11.3] - 2024-04-09

### Fixed
- More logging statements were added
- Catch ValueError when fetching attachments

### Changed
- Some assets were optimised or discarded

## [0.11.2] - 2024-03-28

### Changed
- The app now uses the user id, rather than the userName, to fetch the API

### Added
- Add support for University of Lincoln (@nashgabs)
- Add support for University of Aberdeen (@cbraidwood)
- Add support for University of Western Australia (@ziyuanding)
- Add support for Universidade do Minho (@Darguima)
- Add support for University of Connecticut (@kingcavespider1)
- Add support for Hanze University of Applied Sciences (@Dougley)
- Add support for Centro Universitario de Tecnologia y Arte Digital (@Mr-ConQueso)
- Add support for Universidad de Sevilla (@amoraschi)
- Add support for University of Otago (@nzspider)
- Add support for Schoolcraft College (@jackjack21-pixel)

### Fixed
- Sort out issues with flatpak distribution, update appstream

## [0.11.1] - 2023-11-13

### Added
- Add support for Sam Houston State University (@cainanmahar)

### Changed
- The app will now catch API validation issues and inform the user about them
- Updated PyInstaller version which brings improvements for packaging on macOS

### Fixed
- Improve Blackboard API data validation (@cainanmahar)
- PyQt5 has been updated due to a security issue
- Content body is now UTF-8 encoded explicitly (@arnodeceuninck)
- Support for University of Antwerp fixed (@arnodeceuninck)

## [0.10.0] - 2023-10-05

### Changed
- When a new version is detected and the app is running inside Flatpak,
  the user will only receive a notification
- App is now available on Flathub
- University data file has been optimised to reduce it in size and make
  it easier to add new universities

### Added
- Add basic support for 4 universities:
  Antwerp, CUHK, Concordia Ann Arbor, Edge Hill University

## [0.9.12] - 2023-09-29

### Changed
- Made it easier to request support for a university
- Now you can invoke the python module directly from the terminal
  as `blackboardsync` (when installing via pip)

### Added
- The app will now also be available as a flatpak application,
  providing another option for installation on Linux
- A GIF in the README showing how to install on macOS

### Fixed
- The readthedocs documentation will now build the API reference correctly

## [0.9.11] - 2023-09-25

### Fixed
- Bug introduced with pydantic v2 where some content would be skipped

### Changed
- Pin dependencies in Pipfile and pyproject.toml for improved stability
- Add some classifiers to show in PyPI

## [0.9.10] - 2023-09-17

### Fixed
- Other issues when migrating to pydantic v2

## [0.9.9] - 2023-09-17

### Fixed
- Bug with pydantic Url typing

## [0.9.8] - 2023-09-07

### Changed
- Multiple dependency updates including a security update

## [0.9.7] - 2023-06-30

### Fixed
- Issues with redownloading all files after changing download location
- Potential issue where remaining downloads would be cancelled at the end of sync

### Changed
- WebDav downloads are now also multithreaded

## [0.9.6] - 2023-06-29

### Changed
- Changing download since to an earlier year will cause a redownload
- PyInstaller has been upgraded to 5.13, and other dependencies have also been upgraded

### Fixed
- Bug where resetting download since to 'all' would not take effect
- Type hints were improved

## [0.9.5] - 2023-06-27

### Added
- Option to go over setup wizard again after initial setup

### Fixed
- Issue with session logging back in immediately after logout

### Changed
- Uninstalling the program in Windows will also delete user configuration


## [0.9.4] - 2023-06-26

### Added
- Option to limit the courses downloaded by earliest creation date
- Release notes from CHANGELOG

### Fixed
- App no longer crashes when downloading internet links on Linux


## [0.9.3] - 2023-06-25

### Added
- Add basic support for 29 universities: Arkansas, UVM, Europea Madrid, ECOTEC, URSE, Palermo,
  Tecnologica del Salvador, Alcala, GWU, APU, Bucks, Northampton, Beds, YSU, Ohio, Princess Nourah,
  Leeds Beckett, Post, UAGM, Alabama, Torrens Australia, Holmes Institute, Trinity College Dublin,
  Georgian College, Cardiff, Sheffield Hallam, West of England, Northumbria, Ulster

### Fixed
- Prereleases are marked correctly on Github

### Changed
- Small tweak to initial desktop notification on first download

## [0.9.0] - 2023-06-21

### Changed
- Finally change data source approach to follow institutional rules


### Added
- Add basic support for 10 universities: Westminster, Reading,
  East Anglia, Durham, Salford, South Wales, Leicester, ICL, Bristol,
  Sheffield


### Removed
- User setting for data source



## [0.8.3] - 2023-06-16

### Fixed
- Opening preferences window would previously crash the program
- WebDav filepaths are now sanitised
- Package workflow not triggering on CI



## [0.8.0] - 2023-06-04

### Features
- User must now login in a webview instead, to support 2FA and arbitrary redirects
- Automatic packaging of macOS and Windows applications in github actions
- Improved testing strategy
- Descriptions are now saved as HTML files instead of markdown
- Attachments which are only linked from within content are now supported
- Various other minor improvements



## [0.7.0] - 2021-03-03

### Features
- New option to choose whether files should be re-downloaded upon changing the sync location.
- Sync frequency is now adjustable.
- If the user session expires, BBSync will reflect this and try to login back in using saved configuration.
- Some improvements to the UI and experience in Windows.
- Sync connection errors are now logged to a file.
- Improved README.
- Added basic build scripts.
- Added contributions policy.
- Added changelog.

### Fixes
- File names are now sanitised to comply with (most) Windows file system requirements.



## [0.5.0] - 2021-02-10

### Features
- Added GUI
- Simplified user setup



<!--[0.8.0]: https://github.com/sanjacob/BlackboardSync/releases/-->
