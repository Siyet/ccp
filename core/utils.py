def first(key, sequence):
    return next((x for x in sequence if key(x)), None)
