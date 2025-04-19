from tododav.model.todo.todo_repository import TodoRepository

from datetime import date


def test_todo_repository_init(todos_as_todo_in_list):
    '''
    Test if the repository can be initialized with a todos list.
    '''
    todo_rep = TodoRepository()
    todo_rep.populate_from_todo_list(todos_as_todo_in_list)
    assert todo_rep.todos[0].caldav_todo == todos_as_todo_in_list[0]
    assert todo_rep.todos[1].caldav_todo == todos_as_todo_in_list[1]
    assert todo_rep.todos[2].caldav_todo == todos_as_todo_in_list[2]


def test_todo_repository_filter(todos_as_todo_in_list):
    '''
    Test the repository filtering mechanics.

    ATTENTION:
        I should updated this tests, in case I change the test data !!!
    '''
    todo_rep = TodoRepository()
    todo_rep.populate_from_todo_list(todos_as_todo_in_list)

    # tags filtering

    # filter by todo elements with the tag "tag2"
    filtered_a = todo_rep.filter_by_tags('tag2')
    # there should be two elements
    assert len(filtered_a.get_todos()) == 2
    # deeper tests
    # the first todo should be with the summary "a test task"
    assert filtered_a.get_todos()[0].get_summary() == 'a test task'
    # the second found todo should be with the summary "the third test task"
    assert filtered_a.get_todos()[1].get_summary() == 'the third test task'

    # filter by todo elements without the tag "tag1"
    filtered_a = todo_rep.filter_by_tags('tag1', True)
    # there should be two elements
    assert len(filtered_a.get_todos()) == 2
    # deeper tests
    # the first todo should be with the summary "the third test task"
    assert filtered_a.get_todos()[0].get_summary() == 'the third test task'
    # the second found todo should be with the summary "the fourth test task"
    assert filtered_a.get_todos()[1].get_summary() == 'the fourth test task'

    # date filtering

    # filter by todo elements with due date before 2025-04-08
    filtered_b = todo_rep.filter_by_daterange('', '2025-04-08')
    # there should be only one task found with the summary "a test task"
    assert len(filtered_b.get_todos()) == 1
    assert filtered_b.get_todos()[0].get_summary() == 'a test task'

    # filter by todo elements with due date on date 2025-05-03
    filtered_c = todo_rep.filter_by_date('2025-05-03')
    # there should be only one task found with the summary "the fourth test task"
    assert len(filtered_c.get_todos()) == 1
    assert filtered_c.get_todos()[0].get_summary() == 'the fourth test task'

    # filter by todo elements with due date with time as well like "2025-05-03 10:45"
    filtered_d = todo_rep.filter_by_date('2025-05-03 10:45')
    # there should be only one task found with the summary "the fourth test task"
    assert len(filtered_d.get_todos()) == 1
    assert filtered_d.get_todos()[0].get_summary() == 'the fourth test task'


def test_todo_repository_add_todo():
    todo_rep = TodoRepository()

    # add two todos
    added_a = todo_rep.add_todo(
        'no tags',
        date(2025, 4, 19),
        1
    )
    added_b = todo_rep.add_todo(
        'has tags',
        date(2025, 4, 18),
        0,
        ['tag1', 'tag2']
    )

    assert added_a != added_b

    todos = todo_rep.get_todos()
    assert todos[0].get_summary() == 'no tags'
    assert todos[1].get_summary() == 'has tags'
    assert todos[0].get_due() == date(2025, 4, 19)
    assert todos[1].get_due() == date(2025, 4, 18)
    assert todos[0].has_priority() is True
    assert todos[0].get_priority() == 1
    assert todos[1].has_priority() is False
    assert todos[1].get_priority() is None
    assert todos[0].has_tags() is False
    assert todos[1].has_tags() is True
    assert todos[1].get_tags() == ['tag1', 'tag2']
