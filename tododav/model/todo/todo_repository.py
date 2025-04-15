'''
TodoRepository class.

A repository which can get Todo objects (as TodoFacade) and manage them.
'''

from tododav.model import config
from tododav.model.todo.todo_facade import TodoFacade

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
        out = {
            'NC_URI': config_dict.get('NC_URI', config.NC_URI),
            'NC_USER': config_dict.get('NC_USER', config.NC_USER),
            'NC_PASSWORD': config_dict.get('NC_PASSWORD', config.NC_PASSWORD),
            'NC_CALENDAR': config_dict.get('NC_CALENDAR', config.NC_CALENDAR),
            'NC_TAGS': config_dict.get('NC_TAGS', config.NC_TAGS)
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
