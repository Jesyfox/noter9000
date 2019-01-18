def get_date():
    from datetime import datetime as dt
    return f'{dt.now().hour}:{dt.now().minute}, ' \
           f'{dt.now().day}.{dt.now().month}.{dt.now().year}'


def correct_(note):
    unallowed_values = ['', ]
    for value in note.values():
        if value in unallowed_values:
            return False
    return True
