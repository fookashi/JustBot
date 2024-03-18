__weekdays_as_string = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье'
}


def weekday_to_string(weekday: int):
    try:
        return __weekdays_as_string[weekday]
    except ValueError:
        return None
