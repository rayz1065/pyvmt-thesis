from pyvmt.composer import compose
from pyvmt.shortcuts import Next
from pyvmt.model import Model
from pyvmt.solvers.ic3ia import Ic3iaSolver
from pyvmt.renamer import add_prefix
from pysmt.shortcuts import Symbol, Int, Equals, Ite, LT, Plus, GE
from pysmt import typing

# simple counter model, counts up to a limit and resets to 0
counter_model = Model()
a = counter_model.create_state_var('a', typing.INT)
limit = counter_model.create_frozen_var('limit', typing.INT)
counter_model.add_init(Equals(a, Int(0)))
counter_model.add_trans(Ite(
    GE(a, limit),
    Equals(Next(a), Int(0)),
    Equals(Next(a), Plus(a, Int(1)))
))

# create 3 counters
all_counters = [add_prefix(counter_model, f'counters[{i}].') for i in range(3)]
for i, model in enumerate(all_counters):
    limit = Symbol(f'counters[{i}].limit', typing.INT)
    # first counter counts up to 1, second up to 2,...
    model.add_init(Equals(limit, Int(i + 1)))

# combine all the models together
combined_model = all_counters[0]
for model in all_counters[1:]:
    combined_model = compose(combined_model, model)

# calculate and add a property on the total sum
total_sum = Plus(Symbol(f'counters[{i}].a', typing.INT)
    for i, _ in enumerate(all_counters))

res = Ic3iaSolver(combined_model).check_invar_property(LT(total_sum, Int(6)))
print('res is', 'safe' if res.is_safe() else 'unsafe')
# the counters synchronize on step 11 and their sum becomes equal to 6
assert res.is_unsafe() and res.has_trace()
for step in res.get_trace().get_steps():
    print('On step', step.step_idx, 'total sum is', step.evaluate_formula(total_sum))
