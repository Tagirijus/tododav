from caldav.objects import Todo

import pytest
import os


@pytest.fixture
def test_data_file():
    '''
    This fixture method for pytest returns a callable,
    which is a method, which can return the absolute
    path of the given filename, which should be inside
    the test data folder.
    '''
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')

    def _test_data_file(filename: str = ''):
        return os.path.join(data_dir, filename)

    return _test_data_file


@pytest.fixture
def test_data_folder():
    '''
    This fixture method for pytest returns the data folder and
    optionally another folder inside it as a path string.
    '''
    base_dir = os.path.dirname(__file__)

    def _test_data_folder(relative_folder: str = ''):
        return os.path.join(base_dir, 'data', relative_folder)

    return _test_data_folder


@pytest.fixture
def test_temp_file():
    '''
    This fixture creates a temporary file to work with inside the tests
    and removes it afterward. The content and filename can be set by
    calling the fixture within the test function.

    The file will be created temporarily inside the test/data folder.
    '''
    created_files = []

    def _create_temp_file(
        filename='_pytest_temp_file.txt',
        content='pytest is testing ...'
    ):
        base_dir = os.path.dirname(__file__)
        data_dir = os.path.join(base_dir, 'data')
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'w') as f:
            f.write(content)

        created_files.append(filepath)
        return filepath

    yield _create_temp_file

    # Cleanup after the test
    for filepath in created_files:
        if os.path.exists(filepath):
            os.remove(filepath)


@pytest.fixture
def todos_as_strings_in_list() -> list[str]:
    return [
        """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Nextcloud Tasks v0.16.1
BEGIN:VTODO
CATEGORIES:tag1,tag2
CREATED:20250404T143018Z
DTSTAMP:20250405T054613Z
DUE;VALUE=DATE:20250407
LAST-MODIFIED:20250405T054613Z
SUMMARY:a test task
UID:93cf66e2-9a70-4a7b-b350-0feddb9cf37a
END:VTODO
END:VCALENDAR
""", """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Nextcloud Tasks v0.16.1
BEGIN:VTODO
CATEGORIES:tag1
CREATED:20250405T143018Z
DTSTAMP:20250406T054613Z
DUE;VALUE=DATE:20250408
LAST-MODIFIED:20250406T054613Z
SUMMARY:another test task
UID:93cf66e2-9a70-4a7b-b350-0feddb9cf37b
END:VTODO
END:VCALENDAR
""", """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Nextcloud Tasks v0.16.1
BEGIN:VTODO
CATEGORIES:tag2
CREATED:20250406T143018Z
DTSTAMP:20250407T054613Z
LAST-MODIFIED:20250407T054613Z
SUMMARY:the third test task
UID:93cf66e2-9a70-4a7b-b350-0feddb9cf37c
END:VTODO
END:VCALENDAR
""",
    ]


@pytest.fixture
def todos_as_todo_in_list(todos_as_strings_in_list) -> list[Todo]:
    out = []
    for todo_str in todos_as_strings_in_list:
        out.append(Todo(data=todo_str))
    return out
