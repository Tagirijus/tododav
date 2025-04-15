'''
This module is an abstraction layer for _caldav_ and _VTODO_ objects.

Author: Manuel Senfft (www.tagirijus.de)
'''


if __name__ == "__main__":

    from .model.config import Config
    from .utils import file_utils
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command and command == 'config':
        config = Config()
        file_utils.open_in_editor(config.config_file)
