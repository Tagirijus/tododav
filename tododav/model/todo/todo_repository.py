'''
TodoRepository class.

A repository which can get Todo objects (as TodoFacade) and manage them.
'''

from tododav.model.config import Config
from tododav.model.todo.todo_facade import TodoFacade

from typing import Callable
from caldav.objects import Todo

import caldav


class TodoRepository:

    def __init__(self, config_dict: dict = {}):
        '''
        Initialize the TodoRepository and give an optional config dict.
        Otherwise use the programs config.

        Args:
            config_dict (dict): \
                If not empty, use it's values to replace internal \
                config values. (default: `{}`)
        '''
        self.config = self.init_config(config_dict)
        self.todos = []

    def filter(self, filter_func: Callable[[TodoFacade], bool]) -> 'TodoRepository':
        '''
        Filter the internal list of TodoFacade objects with a given
        callable filter function, which gets a TodoFacade as the first
        parameter and returns a boolean.

        Args:
            filter_func (Callable): \
                The callable filter function to be called on each TodoFacade item \
                in the internal list to filter on. If it returns True, the item \
                will be remain in the original list.

        Returns:
            TodoRepository: Returns a new TodoRepository.
        '''
        out = TodoRepository(self.config)
        out.todos = [
            todo for todo in self.todos if filter_func(todo)
        ]
        return out

    def get_todos(self) -> list[TodoFacade]:
        '''
        Get the list of TodoFacade instances.

        Returns:
            list[Todofacades]: Returns the list of TodoFacades.
        '''
        return self.todos

    def init_config(self, config_dict: dict = {}) -> dict:
        '''
        Init the config with an optional config dict to overwrite the
        programs config.

        Args:
            config_dict (dict): \
                If not empty, use it's values to replace internal \
                config values. (default: `{}`)

        Returns:
            dict: Returns the config as a dict.
        '''
        config = Config()
        out = {
            'NC_URI': config_dict.get('NC_URI', config.get('NC_URI')),
            'NC_USER': config_dict.get('NC_USER', config.get('NC_USER')),
            'NC_PASSWORD': config_dict.get('NC_PASSWORD', config.get('NC_PASSWORD')),
            'NC_CALENDAR': config_dict.get('NC_CALENDAR', config.get('NC_CALENDAR'))
        }
        return out

    def init_with_caldav(self):
        '''
        Initialize the repository with the server connection.
        '''
        with caldav.DAVClient(
            url=self.config['NC_URI'],
            username=self.config['NC_USER'],
            password=self.config['NC_PASSWORD']
        ) as client:
            principal = client.principal()
        calendar = principal.calendar(self.config['NC_CALENDAR'])

        self.populate_from_todo_list(calendar.todos())

    def populate_from_todo_list(self, todo_list: list[Todo]):
        '''
        Initialize with a given todo list. This method will be used internally
        to initialize with the server connection, but also can be used by
        the tests without the server connection.

        Args:
            todo_list (list[Todo]): A list containing Todo instances.
        '''
        self.todos = []
        for todo in todo_list:
            self.todos.append(TodoFacade(todo))
