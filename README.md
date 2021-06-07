# snake_eyes
Python configuration file parser for evolutionary algorithms

Wrapper for the Python config parser to read an ini config file and return a dictionary of typed parameters. For documentation of Python configparser and ini use, see https://docs.python.org/3.8/library/configparser.html

ini sections are stored as sub-dictionaries in the return dict. Filenames support arbitrary extensions (like .cfg). Parameter names are case-sensitive.

The primary function you'll want is `readConfig()` which requires a valid filepath to your config file as the first parameter. You may also pass optional `globalVars` and `localVars` as optional second and third parameters, respectively, for use with expression evaluation. This enables the use of constants and imported/defined functions during the expression evaluation portion of parsing.

Example use:
```python
# ...
from snakeeyes import readConfig
# ...
config = readConfig(myConfigPath, globals(), locals())
```

Parameter type precedence is as follows:
Int
Float
Boolean
Expression (returns result from evaluation)
String

Example ini:
```
[DEFAULT]
# parameters in DEFAULT are inherited by all other sections
opponents = 5

[EXPERIMENT]
render = False
logpath = logs/comparison
runs = 5
evaluations = 3000

[POPULATION]
mu = 200
lambda = 100
parent = k tournament # evaluates to 'k tournament' despite inline comment
survival = truncation

[FEATURES]
floatTest = 1E3 # scientific notation supported for floats
mathTest = ${floatTest}+1 # allows references to other local params and basic python expressions
exprTest = max(${floatTest}, ${mathTest})
farRef = ${EXPERIMENT:evaluations} # allows references to params in other sections too

[QUIRKS]
float = 5.0 # this is evaluated as an int
bool = 1 # this is also evaluated as an int
error = random.random() # unknown libraries or syntax errors are silently treated as strings
functions = max # this returns a function object for max() builtin
string = 'max' # this returns a string
```