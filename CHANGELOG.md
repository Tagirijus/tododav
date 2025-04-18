# Changelog

The following changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and tries to stick to the [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.9] - 2025-04-18
### Changed
- Summary, Priority and Status are now better handled in TodoFacade.


## [0.0.8] - 2025-04-18
### Changed
- TodoRepository.add_todo() now always returns a TodoFacade.


## [0.0.7] - 2025-04-18
### Added
- TodoFacade can now be completed or uncompleted (even with a manually set datetime).


## [0.0.6] - 2025-04-18
### Added
- TodoFacade can now be added directly "manually" to a TodoRepository.


## [0.0.5] - 2025-04-18
### Added
- TodoFacade can return UID and you can set the UID.


## [0.0.4] - 2025-04-18
### Changed
- TodoFacade can now be instanciated without a Todo instance.


## [0.0.3] - 2025-04-16
### Added
- Tasks can now be deleted as well.


## [0.0.2] - 2025-04-16
### Changed
- Some minor tweaks to the initial release.


## [0.0.1] - 2025-04-16
### Added
- Initial release of the `tododav` module.