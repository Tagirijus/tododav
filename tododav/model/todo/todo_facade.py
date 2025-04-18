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

    DEFAULT_TODO = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//tododav
BEGIN:VTODO
END:VTODO
END:VCALENDAR
"""

    def __init__(self, caldav_todo: Todo = Todo(data=DEFAULT_TODO)):
        '''
        A wrapper / facade for the caldav object "Todo" with
        more convenient / intuitive methods.

        Args:
            caldav_todo (Todo): A caldav Todo instance.
        '''
        self.caldav_todo = caldav_todo

    def __str__(self) -> str:
        '''
        The string representation of the TodoFacade instance.

        ATTENTION: If I change the format, I should also change the
        tests for this class accordingly!
        '''
        str_list = []

        summary = self.get_summary()

        if self.has_due():
            str_list.append('due=' + (
                self.get_due().strftime('%Y-%m-%d %H:%M')
                if isinstance(self.get_due(), datetime)
                else self.get_due().strftime('%Y-%m-%d')
            ))

        if self.has_priority():
            str_list.append('priority=' + str(self.get_priority()))

        if self.has_tags():
            str_list.append('tags=[{}]'.format(','.join(self.get_tags())))

        data = (': ' if str_list else '') + ', '.join(str_list)

        return f'{summary}{data}'

    def __repr__(self) -> str:
        '''
        The representation should be the class name and the __str__ output.

        Returns:
            str: The representation of the class.
        '''
        return f'{self.__class__.__name__}: {self.__str__()}'

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

    def complete(self, completion_date: datetime = datetime.now()):
        '''
        This is different from the caldav Todo.complete() method, which will
        be able to also handle the "rrule" for recurring tasks, I guess.
        Unfortunately the Todo.complete() method will also directly save
        the task. I do not want to save it yet, though.

        Args:
            completion_date (date | datetime): \
                An optional completion date to use. Default is "now".
        '''
        if not self.is_done():
            self.set_status('COMPLETED')
            self.set_completed(completion_date)

    def delete(self):
        '''
        Deletes this task.
        '''
        self.caldav_todo.delete()

    def get_completed(self) -> datetime | None:
        '''
        Get the completed string of the VTODO.

        Returns:
            date | datetime: Returns the completed string.
        '''
        if 'COMPLETED' in self.ical:
            return self.vtodo.completed.value

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
        if 'PRIORITY' in self.ical:
            return int(self.vtodo.priority.value)
        else:
            return 0

    def get_status(self) -> str:
        '''
        Get the status string of the VTODO.

        Returns:
            str: Returns the status string.
        '''
        if 'STATUS' in self.ical and self.vtodo.status.value is not None:
            return self.vtodo.status.value
        else:
            return ''

    def get_summary(self) -> str | None:
        '''
        Get the summary string of the VTODO.

        Returns:
            str: Returns the summary string.
        '''
        if 'SUMMARY' in self.ical:
            return self.vtodo.summary.value
        else:
            return None

    def get_tags(self) -> list:
        """
        Get the tags for this task.

        Return:
            list: The list with the tags.
        """
        if 'CATEGORIES' in self.ical and self.vtodo.categories.value is not None:
            return self.vtodo.categories.value
        else:
            return []

    def get_uid(self) -> str:
        '''
        Get the UID string of the VTODO.

        Returns:
            str: Returns the UID string.
        '''
        if 'UID' in self.ical and self.vtodo.uid.value is not None:
            return self.vtodo.uid.value
        else:
            return ''

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

    def has_tags(self) -> bool:
        '''
        Returns if the VTODO has tags (categories).

        Returns:
            bool: Returns True if it has tags.
        '''
        return len(self.get_tags()) != 0

    def is_done(self) -> bool:
        '''
        Returns if the task is done or not. Done status is "COMPLETED".

        Returns:
            bool: Returns True if it is done, False otherwise.
        '''
        return self.get_status() == 'COMPLETED'

    def remove_tag(self, tag: str = ''):
        """
        Remove a tag.

        Args:
            tag (str): The tag string. (default: `''`)
        """
        if self.vtodo.categories.value is not None:
            self.vtodo.categories.value.remove(tag)

    def save(self) -> bool:
        '''
        Save the todo to the CalDAV and return True on success.

        Returns:
            bool: Returns True on success.
        '''
        try:
            self.caldav_todo.save()
            return True
        except Exception as _:
            return False

    def set_completed(self, completed: datetime | None = None):
        """
        Set the completed date for the task. Can be set to "None" to
        remove the completed date.

        Args:
            completed (datetime | None): \
                Set the completed date with a datetime \
                or even None to remove it. (default: `None`)
        """
        if 'COMPLETED' in self.ical:
            self.ical.pop('COMPLETED')
        if isinstance(completed, datetime):
            self.ical.add('COMPLETED', completed.replace(tzinfo=tz.tzlocal()))
        elif hasattr(self.vtodo, 'COMPLETED'):
            self.vtodo.remove(self.vtodo.completed)

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
        if isinstance(due, date) and not isinstance(due, datetime):
            self.ical.add('DUE', due)
        elif isinstance(due, datetime):
            self.ical.add('DUE', due.replace(tzinfo=tz.tzlocal()))
        elif hasattr(self.vtodo, 'DUE'):
            self.vtodo.remove(self.vtodo.due)

    def set_priority(self, priority: int = 0):
        '''
        Change the priority integer of the task. If 0 given, the internal
        priority will be removed, which is the default of the parameter.

        Args:
            priority (int): \
                The new priority. If no parameter is given, it will be removed.
        '''
        self.vtodo.priority.value = priority

    def set_status(self, status: str = ''):
        '''
        Change the status text of the task.

        Args:
            status (str): The new status. If no parameter is given, it will be ''.
        '''
        self.vtodo.status.value = status

    def set_summary(self, summary: str | None = None):
        '''
        Change the summary text of the task or remove it with None.

        Args:
            summary (str | none): \
                The new summary. If no parameter is given, it will be None \
                and thus removed.
        '''
        if 'SUMMARY' in self.ical:
            if summary is None:
                self.ical.pop('SUMMARY')
            else:
                self.vtodo.summary.value = summary
        else:
            self.ical.add('SUMMARY', summary)

    def set_uid(self, uid: str = ''):
        '''
        Change the uid of the task.

        Args:
            uid (str): The new uid. If no parameter is given, it will be ''.
        '''
        self.vtodo.uid.value = uid

    def uncomplete(self):
        '''
        This is different from the caldav Todo.uncomplete() method as well.
        Unfortunately the Todo.uncomplete() method will also directly
        save the task. I do not want to save it yet, though.
        '''
        if self.is_done():
            self.set_status('NEEDS-ACTION')
            self.set_completed(None)
