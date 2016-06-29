# coding: utf-8


def save_relations(instance, field):
    if getattr(instance, field) is not None and getattr(instance, field).pk is None:
        getattr(instance, field).save()
        setattr(instance, field, getattr(instance, field))