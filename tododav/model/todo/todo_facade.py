'''
TodoFacade class.

This class is for representing a NextCloud task in a more
convenient way. It is basically a wrapper for the Todo object
of the caldav module and provides methods, which I personally
find more intuitive to use.
'''

from caldav.objects import Todo

from datetime import date, datetime
from dateutil import tz


class TodoFacade:

    def __init__(self, caldav_todo: Todo):
        '''
        A wrapper / facade for the caldav object "Todo" with
        more convenient / intuitive methods.

        Args:
            caldav_todo (Todo): A caldav Todo instance.
        '''
        self.caldav_todo = caldav_todo

    @property
    def ical(self):
        return self.caldav_todo.icalendar_component

    @property
    def vtodo(self):
        return self.caldav_todo.vobject_instance.vtodo

    @property
    def vobject(self):
        return self.caldav_todo.vobject_instance

    def add_tag(self, tag: str = ''):
        """
        Add a tag.

        Args:
            tag (str): The tag string. (default: `''`)
        """
        if tag:
            self.vtodo.categories.value.append(tag)

    def get_due(self) -> date | datetime:
        '''
        Get the due date or datetime. Returns the today datetime,
        if there is no due date / datetime.

        Returns:
            date | datetime: Returns the due date of the todo.
        '''
        # return self.caldav_todo.vobject_instance.vtodo.due.value
        if 'DUE' in self.ical:
            return self.vtodo.due.value
        else:
            return datetime.now()

    def get_priority(self) -> int:
        '''
        Get the priority integer of the VTODO.

        Returns:
            int: Returns the priority integer.
        '''
        if self.vtodo.priority.value is not None:
            return int(self.vtodo.priority.value)
        else:
            return 0

    def get_summary(self) -> str:
        '''
        Get the summary string of the VTODO.

        Returns:
            str: Returns the summary string.
        '''
        if self.vtodo.summary.value is not None:
            return self.vtodo.summary.value
        else:
            return ''

    def get_tags(self) -> list:
        """
        Get the tags for this task.

        Return:
            list: The list with the tags.
        """
        if self.vtodo.categories.value is not None:
            return self.vtodo.categories.value
        else:
            return []

    def has_due(self) -> bool:
        '''
        Returns if the VTODO has a DUE value after all.

        Returns:
            bool: Returns True if there is a DUE value.
        '''
        return 'DUE' in self.ical

    def has_priority(self) -> bool:
        '''
        Returns if the VTODO has a PRIORITY value after all.

        Returns:
            bool: Returns True if there is a PRIORITY value.
        '''
        return self.get_priority() != 0

    def remove_tag(self, tag: str = ''):
        """
        Remove a tag.

        Args:
            tag (str): The tag string. (default: `''`)
        """
        if self.vtodo.categories.value is not None:
            self.vtodo.categories.value.remove(tag)

    def set_due(self, due: date | datetime | None = None):
        """
        Set the due date for the task. Can be set to "None" to
        remove the due date.

        Args:
            due (date | datetime | None): \
                Set the due date with a date, datetime \
                or even None to remove it. (default: `None`)
        """
        if 'DUE' in self.ical:
            self.ical.pop('DUE')
        if isinstance(due, date):
            self.ical.add('DUE', due)
        elif isinstance(due, datetime):
            self.ical.add('DUE', due.replace(tzinfo=tz.tzlocal()))

    def set_priority(self, priority: int = 0):
        '''
        Change the priority integer of the task. If 0 given, the internal
        priority will be removed, which is the default of the parameter.

        Args:
            priority (int): \
                The new priority. If no parameter is given, it will be removed.
        '''
        self.vtodo.priority.value = priority

    def set_summary(self, summary: str = ''):
        '''
        Change the summary text of the task.

        Args:
            summary (str): The new summary. If no parameter is given, it will be ''.
        '''
        self.vtodo.summary.value = summary
