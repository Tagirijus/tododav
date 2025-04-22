'''
TodoRepository class.

A repository which can get Todo objects (as TodoFacade) and manage them.
'''

from tododav.model.config import Config
from tododav.model.todo.todo_facade import TodoFacade

from tododav.utils import utils

from typing import Callable
from datetime import date, datetime
from dateutil import tz
from caldav.objects import Calendar, Todo

import caldav
import uuid


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
        self.client = caldav.DAVClient(
            url=self.config['NC_URI'],
            username=self.config['NC_USER'],
            password=self.config['NC_PASSWORD']
        )
        self.calendar = None
        self.todos: list[TodoFacade] = []

    def add_todo(
        self,
        summary: str,
        due: date | datetime | None = None,
        priority: int = 0,
        tags: list = []
    ) -> TodoFacade:
        '''
        Create and add a new TodoFacade to the internal list and
        return this TodoFacade as well. Also this method should
        link the caldav client to the internal Todo object inside
        the TodoFacade, so that it should be possible to even
        save this Todo to the calendar as well. And the task will
        be saved immediately!

        Args:
            summary (str): \
                The summary.
            due (date | datetime | None): \
                The optional due date. (default: `None`)
            priority (int): \
                The optional priority between 0-9. (default: `0`)
            tags (list): \
                A list of tags. (default: `[]`)

        Returns:
            TodoFacade: The newly added TodoFacade.
        '''
        if isinstance(self.calendar, Calendar):
            new_caldav_todo = self.calendar.save_todo(
                summary=summary,
                dtstamp=datetime.now(),
                due=due,
                status='NEEDS-ACTION',
                priority=priority,
                categories=','.join(tags),
                uid=str(uuid.uuid4())
            )
            new_todo_facade = TodoFacade(new_caldav_todo)
            self.todos.append(new_todo_facade)
        else:
            new_todo_facade = TodoFacade(
                None,
                summary,
                due,
                'NEEDS-ACTION',
                priority,
                tags
            )
            self.todos.append(new_todo_facade)

        return new_todo_facade

    def add_todo_facade(self, todo_facade: TodoFacade):
        '''
        Simply add a TodoFacade "manually" to the internal list.

        Args:
            todo_facade (TodoFacade): The TodoFacade to add.
        '''
        if todo_facade not in self.todos:
            self.todos.append(todo_facade)

    def connect_calendar(self):
        '''
        Connect to the online calendar with the internal config.
        '''
        with self.client as client:
            principal = client.principal()
        self.calendar = principal.calendar(self.config['NC_CALENDAR'])

    def delete_todo_by_uid(self, uid: str) -> bool:
        '''
        Delete an internal TodoFacade by its uid.

        Args:
            uid (str): the UID of the todo entry.

        Returns:
            bool: Returns True, if task was found and deleted, otherwise False.
        '''
        for i, task in enumerate(self.todos):
            if task.get_uid() == uid:
                task.delete()
                self.todos.pop(i)
                return True
        return False

    def filter(self, filter_func: Callable[[TodoFacade], bool]) -> list[TodoFacade]:
        '''
        Filter the internal list of TodoFacade objects with a given
        callable filter function, which gets a TodoFacade as the first
        parameter and returns a boolean. With that filter the internal
        todos list and reutrn it filtered (in a non-destructive way).

        Args:
            filter_func (Callable): \
                The callable filter function to be called on each TodoFacade item \
                in the internal list to filter on. If it returns True, the item \
                will be remain in the original list.

        Returns:
            list[TodoFacade]: Returns a list with TOdoFacade instances.
        '''
        out = self.todos.copy()
        out = [
            todo for todo in out if filter_func(todo)
        ]
        return out

    def filter_by_date(self, datetime_str: str = '') -> list[TodoFacade]:
        '''
        Filter by the given date / datetime. There can be a date like
        "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" or "YYYYMMDD" or "YYYYMMDDTHHMMZ".

        If a datetime is given, the time has to be equal as well exactly! Otherwise
        the check will only check for the day, even if the DUE date of the VTODO
        would have a time.

        Args:
            datetime (str): Can be a date or datetime string. (default `''`)

        Returns:
            list[TodoFacade]: Returns a list with TodoFacade instances.
        '''
        exact_datetime = utils.string_to_datetime(datetime_str)
        if exact_datetime is not None:
            # a datetime with just 00:00:00.000 time is basically just a date
            is_basically_date = (
                exact_datetime.hour == 0
                and exact_datetime.minute == 0
                and exact_datetime.second == 0
                and exact_datetime.microsecond == 0
            )
        else:
            is_basically_date = False

        def daterange_check(todo: TodoFacade):
            due_date_tmp = todo.get_due()
            if (
                isinstance(due_date_tmp, date)
                and not isinstance(due_date_tmp, datetime)
            ):
                due_date = datetime.combine(due_date_tmp, datetime.min.time())
            else:
                due_date = due_date_tmp

            if isinstance(due_date, datetime):
                due_date = due_date.replace(tzinfo=tz.tzlocal())

            due_date = (
                due_date if not is_basically_date
                else due_date.replace(hour=0, minute=0, second=0, microsecond=0)
            )

            exact_check = (
                exact_datetime is not None and due_date == exact_datetime
            ) if exact_datetime is not None else True

            return todo.has_due() and exact_check

        return self.filter(daterange_check)

    def filter_by_daterange(
        self,
        start: str | date | datetime = '',
        end: str | date | datetime = ''
    ) -> list[TodoFacade]:
        '''
        Filter by the given time range, given as a string, date or datetime.
        As a string there can be a start and / or a end date(time) as "YYYY-MM-DD"
        or "YYYY-MM-DD HH:MM" or "YYYYMMDD" or "YYYYMMDDTHHMMZ".

        The filter logic for start is ">=", while the filter logic for the end is
        only "<". Not sure why, but it feels intuitive to me.

        Args:
            start (str | date | datetime): \
                The start date/datetime as a string. (default: `''`)
            end (str | date | datetime): \
                The end date/datetime as a string. (default: `''`)

        Returns:
            list[TodoFacade]: Returns a list with TodoFacade instances.
        '''
        if isinstance(start, str):
            start_datetime = utils.string_to_datetime(start)
        elif isinstance(start, date) and not isinstance(start, datetime):
            start_datetime = datetime.combine(start, datetime.min.time(), tz.tzlocal())

        if isinstance(end, str):
            end_datetime = utils.string_to_datetime(end)
        elif isinstance(end, date) and not isinstance(end, datetime):
            end_datetime = datetime.combine(end, datetime.max.time(), tz.tzlocal())

        def daterange_check(todo: TodoFacade):
            if (
                isinstance(todo.get_due(), date)
                and not isinstance(todo.get_due(), datetime)
            ):
                due_date = datetime.combine(todo.get_due(), datetime.min.time())
            else:
                due_date = todo.get_due()

            if isinstance(due_date, datetime):
                due_date = due_date.replace(tzinfo=tz.tzlocal())

            start_check = (
                start_datetime is not None and due_date >= start_datetime
            ) if start_datetime is not None else True

            end_check = (
                end_datetime is not None and due_date < end_datetime
            ) if end_datetime is not None else True

            return todo.has_due() and start_check and end_check

        return self.filter(daterange_check)

    def filter_by_tags(
        self,
        tags: str | list = '',
        exclude: bool = False
    ) -> list[TodoFacade]:
        '''
        Filter todos, which contain the given tag / tags, or do not
        contain them (if exclude is True) and return the list of
        TodoFaade instances.

        Args:
            tags (str | list): The tag or tag list to filter on.
            exclude (bool): Exclude instead of include if True.

        Returns:
            list[TodoFacade]: Returns a list with TOdoFacade instances.
        '''
        if isinstance(tags, str):
            tags = [tags]

        return self.filter(
            lambda todo: (not exclude) == bool(set(tags) & set(todo.get_tags()))

        )

    def get_todo_by_uid(self, uid: str) -> TodoFacade | None:
        '''
        Get a TodoFacade instance of the internal list by its UID.

        Args:
            uid (str): The UID so look for.

        Returns:
            TodoFacade | None: A TodoFacade instance or None, if nothing found.
        '''
        for task in self.todos:
            if task.get_uid() == uid:
                return task
        return None

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

    def populate_from_todo_list(self, todo_list: list[Todo] | None = None) -> bool:
        '''
        Initialize with a given todo list. This method will be used internally
        to initialize with the server connection, but also can be used by
        the tests without the server connection.

        Args:
            todo_list (list[Todo] | None): A list containing Todo instances.

        Returns:
            bool: True on success.
        '''
        if todo_list is None:
            if isinstance(self.calendar, Calendar):
                todo_list = self.calendar.todos()

        if isinstance(todo_list, list):
            self.todos: list[TodoFacade] = []
            for todo in todo_list:
                self.todos.append(TodoFacade(todo))
            return True

        return False
