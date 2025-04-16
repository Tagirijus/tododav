from tododav.model.todo.todo_repository import TodoRepository

from datetime import date, datetime


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

    # # TODO: broken, if there is a DATE-TIME DUE date!
    # # filter by todo elements with due date before 2025-04-08
    # search_due = date(2025, 4, 8)
    # filtered_b = todo_rep.filter(
    #     lambda todo: todo.has_due() and todo.get_due() < search_due
    # )
    # # there should be only one task found with the summary "a test task"
    # assert len(filtered_b.get_todos()) == 1
    # assert filtered_b.get_todos()[0].get_summary() == 'a test task'
