from tododav.model.todo.todo_facade import TodoFacade
from caldav.objects import Todo

import datetime


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

    # change due date to date
    new_due_date = datetime.date(2025, 4, 21)
    todo_facade.set_due(new_due_date)
    assert todo_facade.get_due() == todo.vobject_instance.vtodo.due.value
    assert todo_facade.get_due() == new_due_date

    # change due date to datetime
    new_due_datetime = datetime.datetime(2025, 4, 20, 9, 30)
    todo_facade.set_due(new_due_datetime)
    assert todo_facade.get_due() == todo.vobject_instance.vtodo.due.value
    assert todo_facade.get_due() == new_due_datetime

    # remove date / datetime
    todo_facade.set_due(None)  # can also just be .set_due()
    assert todo_facade.get_due() is None
