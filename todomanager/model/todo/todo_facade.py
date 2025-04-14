'''
TodoFacade class.

This class is for representing a NextCloud task in a more
convenient way. It is basically a wrapper for the Todo object
of the caldav module and provides methods, which I personally
find more intuitive to use.
'''

from caldav.objects import Todo

from datetime import date, datetime


class TodoFacade:

    def __init__(self, caldav_todo: Todo):
        '''
        A wrapper / facade for the caldav object "Todo" with
        more convenient / intuitive methods.

        Args:
            caldav_todo (Todo): A caldav Todo instance.
        '''
        self.todo = caldav_todo.vobject_instance.vtodo
        self.ical = caldav_todo.icalendar_component
        self.caldav_todo = caldav_todo

    def add_tag(self, tag: str = ''):
        """
        Add a tag.

        Args:
            tag (str): The tag string. (default: `''`)
        """
        if tag:
            self.todo.categories.value.append(tag)

    def get_tags(self) -> list:
        """
        Get the tags for this task.

        Return:
            list: The list with the tags.
        """
        if self.ical.get('CATEGORIES') is not None:
            return list(self.ical.get('CATEGORIES'))
        else:
            return []

    def get_vtodo(self) -> Todo:
        """
        Return the VTODO object.

        Return:
            Todo: The original (or now modified) VTODO object.
        """
        return self.caldav_todo

    def remove_tag(self, tag: str = ''):
        """
        Remove a tag.

        Args:
            tag (str): The tag string. (default: `''`)
        """
        if self.ical.get('CATEGORIES') is not None:
            self.ical['CATEGORIES'] = [
                x for x in list(self.ical.get('CATEGORIES')) if x != tag
            ]

    def set_due(self, due: date | datetime | None = None):
        """
        Set the due date for the task. Can be set to "None" to
        remove the due date.

        Args:
            due (date | datetime | None): \
                Set the due date with a date, datetime \
                or even None to remove it. (default: `None`)
        """
        if due is None:
            self.todo.pop('due')
        elif isinstance(due, date):
            # date
            # WEITER HIER
            pass
        elif isinstance(due, datetime):
            # datetime
            pass
