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

    def get_due(self) -> object:
        '''
        Get the due date, datetime or None.

        Returns:
            object: Returns the due date of the todo.
        '''
        # return self.caldav_todo.vobject_instance.vtodo.due.value
        if 'DUE' in self.ical:
            return self.vtodo.due.value
        else:
            return None

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
