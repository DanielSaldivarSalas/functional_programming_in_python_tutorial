# We'll test if our class made in 2_logging is a Monad
# It's a monad if it passes the 3 laws
class Monad:
    @classmethod
    def lift(cls, func):
        return compose(cls.unit, func)
    
class ValueAndLog(Monad):
    def __init__(self, value, log):
        self.value = value
        self.log = log

    def __rshift__(self, func):
        result = func(self.value)
        return ValueAndLog(result.value, self.log + result.log)
    
    
    @staticmethod
    def unit(v):
        return ValueAndLog(v, "")

    
def compose(f1, f2):
    return lambda v: f1(f2(v))


def f(x):
    return ValueAndLog( x*x, "I squared %d\n" % x)

def g(x):
    return ValueAndLog(2*x, "Doubled it\n")

# 1. Left identity:
#    unit(a) >> f      is the same as       f(a)
def test_left_identity():
    assert (ValueAndLog.unit(42) >> f).value == f(42).value
    assert (ValueAndLog.unit(42) >> f).log == f(42).log 


# 2. Right identity:
#    m >> unit    is the same as   m
def test_right_identity():
    m = ValueAndLog(42, "blah\n")
    assert (m >> ValueAndLog.unit).value == m.value
    assert (m >> ValueAndLog.unit).log == m.log 


# 3. Associativity:
#    (m >> f) >> g  is the same as  m >> (lambda x: (f(x) >> g))
def test_associativity():
    m = ValueAndLog(42, "blah\n")
    assert ((m >> f) >> g).value == (m >> (lambda x: f(x) >> g)).value
    assert ((m >> f) >> g).log == (m >> (lambda x: f(x) >> g)).log