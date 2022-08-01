import sys
from pyvmt.model import Model
from pyvmt.vmtlib.reader import read
from pyvmt.shortcuts import Next
from pyvmt.solvers.ic3ia import Ic3iaSolver
from pyvmt.solvers.nuxmv import NuxmvSolver
from pysmt.exceptions import PysmtSyntaxError
from pysmt import typing
from pysmt.shortcuts import Int, Equals, Plus

try:
    model = read(sys.stdin)
except PysmtSyntaxError as err:
    # Prints line and column of the error as well as some extra information
    print('The input was not well formed', err)
    sys.exit(1)

# Prints all of the data regarding the model in a human readable way
print(model)

# Print some statistics
print('The model has', len(model.get_state_vars()), 'state variables')

# Adds a counter to the model
counter = model.create_state_var('counter', typing.INT)
model.add_init(Equals(counter, Int(0)))
model.add_trans(Equals(Next(counter), Plus(counter, Int(1))))

# run the model against multiple solvers
for solver_class in [Ic3iaSolver, NuxmvSolver]:
    solver = solver_class(model)
    res = solver.check_property_idx(0)
    safe_str = 'safe' if res.is_safe() else 'not safe'
    print('property is', safe_str, 'according to', solver_class.__name__)

# write to VMT-LIB
# serialize the modified model
model.serialize(sys.stdout)
