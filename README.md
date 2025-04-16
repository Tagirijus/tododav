This module is an abstraction layer for _caldav_ and _VTODO_ objects.

# More info

I was looking for some Python module with which I could manage certain aspects of my NextCloud tasks via CalDAV. I found _caldav_, but I did not like the way of using it, since it wasn't intuitive enough for me. It could also be that I simply do not understand it, not sure. I wrote this module to have another abstraction layer for the _caldav_ module to better create and modify tasks.

# Config

You can edit the config file with `python -m tododav config`, which will first create a new config under `~/.tododav/config.yaml` and then open this file in _vi_. You can change the editor in this file. Other config options do have comments.

# Todo

At the moment only a few attributes of a task can be edited (summary, priority and due date). For my special case I did not need more. Maybe I could extend this module so that it will be possible to modify other attributes as well.

# Changelog

The changelog [is here: CHANGELOG.md](CHANGELOG.md).
