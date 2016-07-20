def first(key, sequence):
    return next((x for x in sequence if key(x)), None)


def achain(obj, default, *attrs):
    def get_attr(obj, attr):
        return getattr(obj, attr, default)
    return reduce(get_attr, attrs, obj)
