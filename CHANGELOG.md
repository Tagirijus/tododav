# Changelog

The following changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and tries to stick to the [semantic versioning](https://semver.org/spec/v2.0.0.html) (except for the "alpha" phase, were I just use the third number, until I decide a first working and usable version exists).

## [0.2.0] - 2025-05-05
### Changed
- TodoRepository.populate_from_todo_list() got some changes again. Future weeks can be set now.


## [0.1.0] - 2025-05-04
### Changed
- TodoRepository.populate_from_todo_list() got some changes, in hope that the task performance for my private TodoManager project will increase.


## [0.0.25] - 2025-04-28
### Fix
- TodoRepository.get_todos_by_daterange() could not use a datetime for filtering.


## [0.0.24] - 2025-04-26
### Changed
- TodoRepository now includes completed tasks as well.


## [0.0.23] - 2025-04-22
### Added
- Added ciritcla thoughts in my head that this changelog is clever ... I should have completed my other depending project first and make a huge initial "this is it now" commit instead ... oopsie.

### Changed
- Changed TodoRepository.filter... methods to .get_todos_...


## [0.0.22] - 2025-04-22
### Added
- Added TodoFacade.has_rrule().


## [0.0.21] - 2025-04-22
### Added
- Added TodoRepository.delete_todo_by_uid().


## [0.0.20] - 2025-04-22
### Added
- Added TodoRepository.get_todo_by_uid().


## [0.0.19] - 2025-04-21
### Changed
- Changed what a TodoRepository filtering will return. It now returns a list of TodoFacade instances, instead of a whole TodoRepository. I had the problem, that with returning a TodoRepository, I would have to connect to the calendar again. And in the end I just want f iltered set of the todos as a list only anway.


## [0.0.18] - 2025-04-21
### Changed
- Improved `TodoFacade.add_tag()` method.


## [0.0.17] - 2025-04-21
### Changed
- Improved `TodoFacade.add_tag()` method.


## [0.0.16] - 2025-04-21
### Changed
- Splitted `TodoRepository.init_with_caldav()` into `TodoRepository.connect_calendar()` and `TodoRepository.populate_from_todo_list()`, which now has a default parameter and will (wíthout one given) populate form the online todos, otherwise from the given list.


## [0.0.15] - 2025-04-21
### Changed
- TodoFacade.save() now returns tuple `(bool, Exception | None)`.


## [0.0.14] - 2025-04-20
### Changed
- I changed the filter logic of the TodoRepository.filter_by_daterange() to filter the start with the logic `>=` and the end with the logic `<`.
- Also the TodoRepository.fitler_by_daterange() method can accept date or datetime instances now.
### Fixed
- I fixed something in the filtering and added a test accordingly.


## [0.0.13] - 2025-04-19
### Changed
- Changed how TodoFacade set_priority() will handle "0". Previously it would set "None" internally for that; now it can be the integer "0".


## [0.0.12] - 2025-04-19
### Added
- TodoFacade.set_tags() added to immediately set the tasks tags.
- TodoFacade can now be instanceiated with its attributes via the constructors parameters.
- Added a TodoRepository test.
### Changed
- Changed a bit how the TodoRepository adds new TodoFacades to the internal list.
### Fixed
- TodoFacade default VTODO string had newline, which could raise icalendar warnings.


## [0.0.11] - 2025-04-19
### Changed
- TodoFacade.add_tag() prevens now adding the same tag more than once.


## [0.0.10] - 2025-04-18
### Added
- The string representation of TodoFacade now includes its completion status.


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