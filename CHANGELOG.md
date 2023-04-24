# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [UNRELEASED]

## 0.2.1 - 2023-03-31
### Changed
+ 'pass' to 'continue' in wikidata_scraper.py and wikipedia_scraper.py
+ Moved py files to 'py' folder

### Fixed
+ InvalidTitleError exception caught and managed in wikipedia_scraper.py
+ AttributeError exception caught and managed in wikidata_scraper.py

## 0.2.0 - 2023-02-24
### Changed
+ Split the app into several modules for better organization and maintainability.
+ Reorganized output file fields to be more intuitive.

### Added
+ Added command line interface for improved usability.
+ Added a tqdm load bar for better progress tracking.

### Fixed
+ Fixed several minor bugs and issues.

## 0.1.0 - 2023-02-13
### Added
+ Input functions to allow for terminal use.
+ print() for every user input.

### Fixed
+ Fixed bug in extract_file() function.

### Change
+ Modules have be split into separate files.
