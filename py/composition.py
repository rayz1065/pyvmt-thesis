from pyvmt.model import Model
from pyvmt.shortcuts import Next
from pyvmt.solvers.ic3ia import Ic3iaSolver
from pyvmt.composer import compose
from pysmt.shortcuts import Not, Iff, GT, Int, LT, Equals, Ite, Plus
from pysmt import typing


model_a = Model()
# variable `a` loops between 0 and 1
a = model_a.create_state_var('a', typing.BOOL)
model_a.add_init(Not(a))
model_a.add_trans(Iff(Next(a), Not(a)))

model_b = Model()
model_b.add_input_var(a)
# counter increments if `a` is True
counter = model_b.create_state_var('counter', typing.INT)
model_b.add_init(Equals(counter, Int(0)))
model_b.add_trans(Ite(a,
    Equals(Next(counter), Plus(counter, Int(1))),
    Equals(Next(counter), counter)
))

# eventually the counter becomes greater than 10 forever
model_b.add_live_property(GT(counter, Int(10)))
res = Ic3iaSolver(model_b).check_property_idx(0)
assert res.is_unsafe() # the counter may never increase if `a` is always False

# compose the two systems
model_c = compose(model_a, model_b)
res = Ic3iaSolver(model_c).check_property_idx(0)
assert res.is_safe() # the counter increases regularly every two steps

# show how the counter increases
res = Ic3iaSolver(model_c).check_invar_property(LT(counter, Int(10)))
print('res is', 'safe' if res.is_safe() else 'unsafe')
assert res.is_unsafe() and res.has_trace()
for step in res.get_trace().get_steps():
    print(step.step_idx, step.get_assignments(), step.is_loopback)
