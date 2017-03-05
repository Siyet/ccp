from copy import deepcopy
from django.forms import Form
from django.forms.fields import IntegerField

class M(type):
    def __new__(mcs, name, bases, attrs):
        attrs.pop('foo', None)
        m = (super(M, mcs).__new__(mcs, name, bases, attrs))
        m.some_base = ['1', '2']
        return m


class A(object):
    def __init__(self):
        self.some = deepcopy(self.some_base)

class B(A):
    __metaclass__ = M


class C(B):
    foo = 1

class MaForm(Form):
    f = IntegerField('az')


m = MaForm()
print(MaForm.f)