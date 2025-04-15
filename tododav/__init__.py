'''
A CalDAV VTODO abstraction layer module.

Author: Manuel Senfft (www.tagirijus.de)
'''

from .model.todo.todo_facade import TodoFacade
from .model.todo.todo_repository import TodoRepository


__all__ = [
    'TodoFacade',
    'TodoRepository'
]
