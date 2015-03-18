
def determine_status(name, current, warn, critical, trigger=None):

    if not warn and not critical:
        return 'ok'

    if trigger:
        if trigger == 'ignore':
            return 'ok'

        if trigger == 'lt':
            if warn and current > warn:
                return 'ok'
            if warn and critical and current <= warn  and current > critical:
                return 'warning'
            if critical and current <= critical:
                return 'critical'
    else:
        if current < warn:
            return 'ok'
        if warn <= current < critical:
            return 'warning'
        if current >= critical:
            return 'critical'