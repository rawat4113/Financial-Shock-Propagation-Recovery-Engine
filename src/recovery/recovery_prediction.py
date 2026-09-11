def recovery_days(path, target=0.99):
    for day,value in path:
        if value>=target:
            return day
    return None
