# Overview
AI [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) solver!

Developed by [Nolan Bock](https://www.linkedin.com/in/nbock/) and [Maria Clara Soares Bezerra](https://www.linkedin.com/in/maria-clara-bezerra-09293a137/)

Our Minesweeper AI formulates the game as a Constraint Satisfaction Problem in order to solve it. On a high level, our
solver uncovers a square and based on its information attempts to infer with the highest accuracy possible the value of
the surrounding squares.


Within our CSP file, we have the following classes: Variable, Constraint, CSP, and Backtrack. **Variable** objects get
initialized with a list of domain values, as well as an `assignedValue` attribute, which is a set of flags that keeps
track of whether a value is in the domain. We use this for constraint propagation/ arc consistency, so we can eliminate
values from domain of variable that can never be part of a consistent solution. The **Constraint** class allows for the
initialization of constraint objects (which follow a specific order over variables). When the constraints are
initialized, grids that contain a mine are assigned a 1, grids that do not contain a mine are assigned a 0, and unknown
grids are assigned [0, 1]. This ordered list of variables is specified through the `scope` attribute. A constraint
object also contains a `sat_tuples` attribute, which is a dictionary that stores a list of tuples that satisfy the
constraints. So each tuple defines a value for each domain variable in the scope such that the values satisfy the
constraints. The **CSP** class is effectively where we formulate the problem. A CSP object contains constraint and
variable attributes, and has methods to add variables and constraints to it. We also included methods to get a list of
variables in the CSP, a list of constraints, and a list of constraints that include a variable in their scope.
The **Backtrack** class takes in a CSP object representing the problem to be solved and performs backtracking search
based on a routine specified through propagators.py.



# Running a test
The contents of minesweeper.py can be edited to run a sample solution. Use `python3 minesweeper.py` to see a 16x16 bard solved.

# TODO
- Add function documentation for everything
- Think about if we want random variable assignment or not
- Think about GUI
- Slides
