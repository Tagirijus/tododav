'''
Config class

This class is the final config, which will "fill"
the ConfigBase.
'''

from .config_base import ConfigBase


class Config(ConfigBase):
    def __init__(self, data_dir: str = ''):
        '''
        The config object.

        Args:
            data_dir (str): \
                Optionally set a different data_dir folder. (default: `''`)
        '''
        super().__init__('tododav', data_dir)

        self.add_config(
            'editor',
            'vi',
            [
                'The default editor to use when editing files.'
            ]
        )
        self.add_config(
            'NC_URI',
            'https://nc.domain.org/remote.php/dav/calendars/user_name/calendar_name/',
            [
                'The URL to the NextCloud instance and the calendar'
            ]
        )
        self.add_config(
            'NC_USER',
            'user_name',
            [
                'The NextCloud user name.'
            ]
        )
        self.add_config(
            'NC_PASSWORD',
            'password',
            [
                'The NextCloud password.'
            ]
        )
        self.add_config(
            'NC_CALENDAR',
            'calendar_name',
            [
                'The NextCloud calendar name to use.'
            ]
        )

        self.create_or_update_config()
