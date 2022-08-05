import sys
from pyvmt.vmtlib.reader import read
from pyvmt.solvers.ic3ia import Ic3iaSolver

# Read a model from the standard input
model = read(sys.stdin)

# Create an instance of the Ic3ia solver
solver = Ic3iaSolver(model)

# Change some of the options
solver.options.set_random_seed(123)
solver.options.set_inc_ref(1)

# Use a helper method to check a property
res = solver.check_property_idx(0)

# Analyze the result
safe_str = 'safe' if res.is_safe() else 'not safe'
print('property is', safe_str)

if res.is_unsafe() and res.has_trace():
    # iterate through the trace and print the assignments
    trace = res.get_trace()
    print('A', trace.get_trace_type(), 'trace is available')
    print('It has', trace.steps_count(), 'steps')
    for step in trace.get_steps():
        step_type = 'loopback step' if step.is_loopback else 'step'
        print(';;', step_type, step.step_idx)
        for var, val in step.get_assignments().items():
            print('>', var, '=', val)
        print()

    # get the first step
    step = trace.get_step(0)
    print(step.serialize_to_string())
    if step.has_next_step():
        step = step.get_next_step()
        print('Step after the first one is', step.serialize_to_string())

    # get just the changing variables for each step
    steps = (step for step in trace.get_steps() if step.has_next_step())
    for step in steps:
        print(';; step', step.step_idx)
        next_step = step.get_next_step()
        for stvar in step.get_changing_variables():
            print(stvar, 'from', step.get_assignment(stvar), 'to', next_step.get_assignment(stvar))
        print()

    if trace.has_loopback_step():
        loopback_step = trace.get_loopback_step()
        print(loopback_step.serialize_to_string())
