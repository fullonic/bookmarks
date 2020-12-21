from pathlib import Path
import datetime


def check_for_new_bookmarks_update():
    """Check if there is any new bookmark and if exist, update current db version."""
    path = ...
    file = Path(path)
    last_modification = file.stat().st_mtime
    last_time_check = 00000
    if last_modification != last_time_check:
        # update bookmarks db
        ...
    return
