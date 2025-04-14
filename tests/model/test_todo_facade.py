from todomanager.model.todo.todo_facade import Todo, TodoFacade

import datetime

test_vtodo = """
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
UID:93cf66e2-9a70-4a7b-b350-0feddb9cf37c
END:VTODO
END:VCALENDAR
"""


def test_todo_facade_init():
    """
    Testing the initialization of a TodoFacade.
    """
    todo = Todo(data=test_vtodo)
    todo_facade = TodoFacade(todo)
    assert todo_facade.caldav_todo == todo


def test_todo_facade_tags():
    """
    Testing the handling of tags for a task.
    """
    todo = Todo(data=test_vtodo)
    todo_facade = TodoFacade(todo)

    # test, of the given parameter was set internally correctly
    assert todo == todo_facade.get_vtodo()

    # tags list should be the same
    # also I am getting the list not with icalendar_component
    # here, but with vobject_instance, which also checks if
    # the whole integrity internally still consists
    todo_tags = todo.vobject_instance.vtodo.categories.value
    assert todo_tags == todo_facade.get_tags()

    # even after adding a tag
    todo_facade.add_tag('tag3')
    assert todo_tags == todo_facade.get_tags()

    # or removing a tag
    todo_facade.remove_tag('tag3')
    assert todo_tags == todo_facade.get_tags()

    # DEBUG
    # change due date
    new_due = datetime.datetime(2025, 4, 20, 9, 30)

    from icalendar import vDatetime
    # Ersetze das DUE-Feld durch ein vDatetime-Objekt
    todo.icalendar_component["DUE"] = vDatetime(new_due)
    # Optional: Entferne ggf. explizit den VALUE-Parameter, der einen DATE-Typ erzwingt:
    if "VALUE" in todo.icalendar_component["DUE"].params:
        if todo.icalendar_component["DUE"].params["VALUE"].upper() == "DATE":
            del todo.icalendar_component["DUE"].params["VALUE"]

    print(todo_facade.ical.to_ical())
    assert False
