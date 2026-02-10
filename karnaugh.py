import re
import sys

import display
import logic


def validate_and_get_vars(ones, dont_cares):
    """
    Validates the union of `ones` and `dont_cares` to determine the number of variables
    needed for representing values in a boolean algebra minimization procedure. Ensures
    the values are within allowable bounds and raises an error if not.
    """
    all_values = ones.union(dont_cares)
    if not all_values:
        return 3
    max_val = max(all_values)
    if max_val >= 16:
        raise ValueError(f"{max_val} value needs at least 5 variables")
    return 4 if max_val >= 8 else 3


def parse_input(input_str):
    """
    Parses the input string to extract numbers from sigma(...) and sigma*(...) patterns.
    This function identifies the numerical values associated with specific patterns
    in the input string. The sigma(...) pattern corresponds to a set of "ones," while
    the sigma*(...) pattern corresponds to a set of "don't care." It processes the
    matching string portions, extracts the integer values, and returns them as sets.
    """
    input_str = input_str.replace(" ", "")
    sigma_pattern = r'sigma\(([\d,]+)\)'
    sigma_star_pattern = r'sigma\*\(([\d,]+)\)'
    ones = set()
    dont_cares = set()
    match_ones = re.search(sigma_pattern, input_str)
    if match_ones:
        try:
            nums = [int(x) for x in match_ones.group(1).split(',')]
            ones.update(nums)
        except ValueError:
            raise ValueError("Values from sigma() must be numbers.")
    match_dc = re.search(sigma_star_pattern, input_str)
    if match_dc:
        try:
            nums = [int(x) for x in match_dc.group(1).split(',')]
            dont_cares.update(nums)
        except ValueError:
            raise ValueError("Values from sigma*() must be numbers.")
    if not match_ones and not match_dc:
        raise ValueError("Format must be sigma(...) or sigma(...)+sigma*(...)")
    return ones, dont_cares


if len(sys.argv) < 2:
    print("Usage: python3 karnaugh.py \"sigma(1,5,9,13)+sigma*(3,7,11,15)\"")
input = sys.argv[1]
try:
    ones, dont_cares = parse_input(input)
    num_vars = validate_and_get_vars(ones, dont_cares)
    vars_names = ['x', 'y', 'z'] if num_vars == 3 else ['x', 'y', 'z', 't']
    print(f"Detected: {num_vars} variables ({', '.join(vars_names)})")
    display.print_karnaugh_map(ones, dont_cares, num_vars, vars_names)
    minimized_terms = logic.minimize_karnaugh(ones, dont_cares, num_vars)
    minimized_expr = logic.format_expression(minimized_terms, vars_names)
    fnd = logic.get_fnd(ones, num_vars, vars_names)
    fnc = logic.get_fnc(ones, dont_cares, num_vars, vars_names)
    filename = "truth_table.txt"
    display.generate_truth_table_file(ones, dont_cares, num_vars, vars_names, filename)
    print("\n" + "=" * 30)
    print(f"FINAL RESULTS:")
    print("-" * 30)
    print(f"Minimized expression:\n f({','.join(vars_names)}) = {minimized_expr}")
    print("-" * 30)
    print(f"Truth table -> '{filename}'")
    print(f"FND: {fnd}")
    print(f"FNC: {fnc}")
    print("=" * 30)
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
