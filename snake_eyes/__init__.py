"""
snake_eyes config reader
"""
from configparser import ConfigParser, ExtendedInterpolation


def read_config(config_path, global_vars=globals(), local_vars=locals()):
    """
    Wrapper for the Python config parser to read an ini config file and return
    a dictionary of typed parameters. For documentation of Python configparser
    and ini use, see https://docs.python.org/3.8/library/configparser.html

    Expects a valid filepath to the config file as input
    """

    params = {}
    config = ConfigParser(
        inline_comment_prefixes=("#"), interpolation=ExtendedInterpolation()
    )
    config.optionxform = lambda optionstr: optionstr
    with open(config_path, encoding="utf-8") as file:
        config.read_file(file)
    for section in config:
        params[section] = {}
        for key in config[section]:
            params[section][key] = interpolate(
                config[section], key, global_vars, local_vars
            )
    return params


def interpolate(config, key, global_vars, local_vars):
    """
    Attempts to interpolate parameters to more useful data types based on
    semi-intelligent methods provided by configparser.

    Type precedence:
    int
    float
    boolean
    expression
    string

    Ambiguous numerical parameters default to ints. Floats are identified if
    the float and int values differ (so 1.0 would be cast to an int). 0 and 1
    are interpreted as ints instead of boolean values under the assumption that
    this doesn't impact logical operations on the values. If boolean, float,
    and	int types fail, the parameter is assumed to be a string type. An
    attempt is made to evaluate the string as a Python expression. If
    successful, the expresison result is returned. Otherwise, the parameter is
    assumed to actually be a string.

    Floats accept scientific notation such as 1E3 for 1000

    Booleans accept a range of (case-insensitive) values:
    True/False
    yes/no
    on/off
    1/0 (though this one is converted to int as documented above)
    """
    try:
        float_num = config.getfloat(key)
        try:
            int_num = config.getint(key)
            if float_num == int_num:
                return int_num
            return float_num
        except Exception:
            return float_num
    except Exception:
        pass

    try:
        return config.getboolean(key)
    except Exception:
        pass

    try:
        return eval(
            config.get(key).replace("\n", ""), global_vars, local_vars
        )  # evaluate expressions
    except Exception:
        pass

    return config.get(key)  # returns a string


if __name__ == "__main__":
    print(read_config("./samples/example.cfg"))
