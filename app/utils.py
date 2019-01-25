def get_date():
    from datetime import datetime as dt
    # return f'{dt.now().hour}:{dt.now().minute}, ' \
    #        f'{dt.now().day}.{dt.now().month}.{dt.now().year}'
    return dt.utcnow()


def validate(note):
    note = [str(n).rstrip() for n in note.values()]
    return all(note)
