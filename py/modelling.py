from pysmt import typing
from pysmt.shortcuts import Symbol, Equals, Ite, Plus, Int, Not, Iff, LT, GE
from pyvmt.shortcuts import Next
from pyvmt.model import Model

model = Model()

# adding state variables manually
a = Symbol('a', typing.INT)
model.add_state_var(a)

# using the helper function
b = model.create_state_var('b', typing.BOOL)

assert model.is_state_variable(a)
assert model.is_state_variable(b)

print(model.get_state_vars()) # [a, b]
print(model.next(a))          # (a)'

# adding input variables manually
toggle = Symbol('toggle', typing.BOOL)
model.add_input_var(toggle)

# using the helper function
counter_max = model.create_input_var('counter_max', typing.INT)

assert model.is_input_variable(toggle)
assert model.is_input_variable(counter_max)

print(model.get_input_vars()) # [toggle, counter_max]

# adding init constraints
model.add_init(Equals(a, Int(-1)))
model.add_init(b)

print(model.get_init_constraints()) # [(a == 0), b]
print(model.get_init_constraint())  # ((a == 0) & b)

# adding trans constraints
model.add_trans(
    Equals(Next(a),
        #  b => a' = (a + 1) % counter_max
        # ~b => a' = a
        Ite(b,
            Ite(
                LT(a, counter_max),
                Plus(a, Int(1)),
                Int(0)
            ), a
        )
    )
)
model.add_trans(
    #  toggle => b' = ~b
    # ~toggle => b' = b
    Iff(Next(b),
        Ite(toggle, Not(b), b)
    )
)

print(model.get_trans_constraints()) # List of the 2 constraints
print(model.get_trans_constraint())  # Conjunction of the constraints

# invar properties
# 'a' is always less than 10
model.add_invar_property(LT(a, Int(10)))
# this property is unsafe since it can be proven wrong by a trace
# where counter_max = 10 and toggle is false

# 'a' is always non-negative
model.add_invar_property(GE(a, Int(0)))
# this property is unsafe since 'a' is initially negative

# live properties
# Eventually 'a' will always be greater or equal to 1
model.add_live_property(GE(a, Int(1)))
# this property is unsafe since the counter may reset to 0 infinitely often

# Eventually 'a' will always be non-negative
model.add_live_property(GE(a, Int(0)))
# While this could not be verified as an invar property, it can be verified
# as a live property since after one step 'a' can never be negative again

# Checking the properties
from pyvmt.solvers.ic3ia import Ic3iaSolver
solver = Ic3iaSolver(model)
for property_idx in range(4):
    res = solver.check_property_idx(property_idx)
    print(model.get_property(property_idx))
    print('property', property_idx, 'is', 'safe' if res.is_safe() else 'unsafe')
    if res.has_trace():
        for step in res.get_trace().get_steps():
            print(step.serialize_to_string())
