from tododav.model.todo.todo_facade import TodoFacade
from caldav.objects import Todo

from datetime import date, datetime


def test_todo_facade_init(todos_as_strings_in_list):
    '''
    Testing the initialization of a TodoFacade.
    '''
    todo = Todo(data=todos_as_strings_in_list[0])
    todo_facade = TodoFacade(todo)
    assert todo_facade.caldav_todo == todo


def test_todo_facade_tags(todos_as_strings_in_list):
    '''
    Testing the handling of tags for a task.
    '''
    todo = Todo(data=todos_as_strings_in_list[0])
    todo_facade = TodoFacade(todo)

    # tags list should be the same
    # also I am getting the list not with icalendar_component
    # here, but with vobject_instance, which also checks if
    # the whole integrity internally still consists
    todo_tags = todo.vobject_instance.vtodo.categories.value
    assert todo_tags == todo_facade.get_tags()
    assert todo_tags == ['tag1', 'tag2']

    # even after adding a tag
    todo_facade.add_tag('tag3')
    assert todo_tags == todo_facade.get_tags()
    assert todo_tags == ['tag1', 'tag2', 'tag3']

    # or removing a tag
    todo_facade.remove_tag('tag3')
    assert todo_tags == todo_facade.get_tags()
    assert todo_tags == ['tag1', 'tag2']


def test_todo_facade_due_date(todos_as_strings_in_list):
    '''
    Testing the handling of due date for a task.
    '''
    todo = Todo(data=todos_as_strings_in_list[0])
    todo_facade = TodoFacade(todo)

    # change due date to date
    new_due_date = date(2025, 4, 21)
    todo_facade.set_due(new_due_date)
    assert todo_facade.get_due() == todo.vobject_instance.vtodo.due.value
    assert todo_facade.get_due() == new_due_date

    # change due date to datetime
    new_due_datetime = datetime(2025, 4, 20, 9, 30)
    todo_facade.set_due(new_due_datetime)
    assert todo_facade.get_due() == todo.vobject_instance.vtodo.due.value
    assert todo_facade.get_due() == new_due_datetime

    # remove date / datetime
    todo_facade.set_due(None)  # can also just be .set_due()
    assert todo_facade.has_due() is False
    # get_due() still returns the actual datetime, if there is no DUE!
    # and since the milliseconds won't be the same when comparing, I
    # strip it down to a comparible string instead here.
    todos_none_due_date_str = todo_facade.get_due().strftime('%Y-%m-%d %H:%M')
    now_date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    assert todos_none_due_date_str == now_date_str


def test_todo_facade_summary(todos_as_strings_in_list):
    '''
    Test the getting and setting of the summary.
    '''
    todo = Todo(data=todos_as_strings_in_list[0])
    todo_facade = TodoFacade(todo)

    # original test data for the first task should have summary "a test task"
    assert todo_facade.get_summary() == 'a test task'

    # now I am going to change it
    todo_facade.set_summary('a changed test task')
    assert todo_facade.get_summary() == 'a changed test task'


def test_todo_facade_priority(todos_as_strings_in_list):
    '''
    Test the getting and setting of the priority.
    '''
    todo = Todo(data=todos_as_strings_in_list[0])
    todo_facade = TodoFacade(todo)

    # original test data for the first task should have highest priority of 1
    assert todo_facade.get_priority() == 1

    # now I am going to change it
    todo_facade.set_priority(5)
    assert todo_facade.get_priority() == 5

    # and it can be removed completely by not giving a parameter, or 0
    todo_facade.set_priority()
    assert todo_facade.get_priority() == 0
    assert todo_facade.has_priority() is False


def test_todo_facade_string_formatting(todos_as_strings_in_list):
    '''
    Test if the string representation works properly.

    ATTENTION: I might have to change the test, if I change the
    format of the __str__() method.
    '''
    todo = Todo(data=todos_as_strings_in_list[2])
    todo_facade = TodoFacade(todo)

    supposed_str = 'a test task: due=2025-04-07, priority=1, tags=[tag1,tag2]'
    assert str(todo_facade) == supposed_str

    # and another task
    todo = Todo(data=todos_as_strings_in_list[3])
    todo_facade = TodoFacade(todo)

    supposed_str = 'the fourth test task: due=2025-05-03 10:45, priority=5, tags=[tag4]'
    assert str(todo_facade) == supposed_str
