from todomanager.model.todo.todo_repository import TodoRepository


def test_todo_repository_init(todos_as_todo_in_list):
    '''
    Test if the repository can be initialized with a todos list.
    '''
    todo_rep = TodoRepository()
    todo_rep.populate_from_todo_list(todos_as_todo_in_list)
    assert todo_rep.todos[0].caldav_todo == todos_as_todo_in_list[0]
    assert todo_rep.todos[1].caldav_todo == todos_as_todo_in_list[1]
    assert todo_rep.todos[2].caldav_todo == todos_as_todo_in_list[2]
