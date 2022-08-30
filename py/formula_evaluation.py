from pyvmt.model import Model
from pyvmt.shortcuts import Next
from pyvmt.solvers.ic3ia import Ic3iaSolver
from pysmt.shortcuts import Plus, Int, Equals, Ite, LT, Minus
from pysmt import typing

model = Model()
a = model.create_state_var('a', typing.INT)
b = model.create_state_var('b', typing.INT)
enable_b = model.create_input_var('enable_b', typing.BOOL)

model.add_init(Equals(a, Int(0)))
model.add_init(Equals(b, Int(0)))

# a' = (a + 1) % 4
model.add_trans(Ite(Equals(a, Int(3)),
    Equals(Next(a), Int(0)),
    Equals(Next(a), Plus(a, Int(1)))
))
# b' = (b + 1) % 3
model.add_trans(Ite(enable_b,
    Ite(Equals(b, Int(2)),
        Equals(Next(b), Int(0)),
        Equals(Next(b), Plus(b, Int(1)))
    ),
    # b disabled, b remains constant
    Equals(Next(b), b)
))

# Model contains 2 counters, a from 0 to 3, and b from 0 to 2
ab_sum = Plus(a, b)
model.add_invar_property(LT(ab_sum, Int(5))) # sum never reaches 5

solver = Ic3iaSolver(model)
res = solver.check_property_idx(0)
assert res.is_unsafe() and res.has_trace()
# Evaluate some formulae over the obtained trace
for step in res.get_trace().get_steps():
    # Calculated over a step: the current sum
    print(f'a = {step.evaluate_formula(a)},',
          f'b = {step.evaluate_formula(b)},',
          f'Sum = {step.evaluate_formula(ab_sum)}', end='')
    if step.has_next_step():
        # Calculated during a transition: how much the sum increases
        delta = Minus(Next(ab_sum), ab_sum)
        print(', Delta =', step.evaluate_formula(delta), end='')
    print()

# output:
# a = 0, b = 0, Sum = 0, Delta = 1
# a = 1, b = 0, Sum = 1, Delta = 2
# a = 2, b = 1, Sum = 3, Delta = 2
# a = 3, b = 2, Sum = 5
