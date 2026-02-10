import itertools


def get_binary(n, num_vars):
    """
    Convert an integer to its binary representation as a string, padded to a specified
    number of bits.
    This function takes an integer number and converts it to its binary string
    representation. The returned binary string is zero-padded to match the
    specified number of bits (`num_vars`).
    """
    return format(n, f'0{num_vars}b')

def combine_terms(term1, term2):
    """
    Combines two terms by replacing differing characters with a dash ('-') if there is exactly one
    differing character.
    """
    diff_count = 0
    res = []
    for c1, c2 in zip(term1, term2):
        if c1 == c2:
            res.append(c1)
        else:
            diff_count += 1
            res.append('-')
    if diff_count == 1:
        return "".join(res)
    return None

def minimize_karnaugh(ones, dont_cares, num_vars):
    """
    Minimizes a Boolean function using the Quine-McCluskey algorithm. Given the set of minterms
    (ones) and don't-care conditions, the function identifies the essential prime implicants
    and minimizes the Boolean expression.
    """
    current_terms = {get_binary(i, num_vars) for i in ones | dont_cares}
    prime_implicants = set()
    while True:
        next_terms = set()
        used_terms = set()
        sorted_terms = sorted(list(current_terms))
        for i in range(len(sorted_terms)):
            for j in range(i + 1, len(sorted_terms)):
                t1 = sorted_terms[i]
                t2 = sorted_terms[j]
                combined = combine_terms(t1, t2)
                if combined:
                    next_terms.add(combined)
                    used_terms.add(t1)
                    used_terms.add(t2)
        for t in current_terms:
            if t not in used_terms:
                prime_implicants.add(t)
        if not next_terms:
            break
        current_terms = next_terms
    final_terms = []
    uncovered_ones = ones.copy()
    sorted_pis = sorted(list(prime_implicants), key=lambda x: x.count('-'), reverse=True)
    for pi in sorted_pis:
        dash_indices = [i for i, char in enumerate(pi) if char == '-']
        options = list(itertools.product('01', repeat=len(dash_indices)))
        temp_covered = set()
        for opt in options:
            temp_s = list(pi)
            for idx, val in zip(dash_indices, opt):
                temp_s[idx] = val
            val_int = int("".join(temp_s), 2)
            if val_int in ones:
                temp_covered.add(val_int)
        if not temp_covered.isdisjoint(uncovered_ones):
            final_terms.append(pi)
            uncovered_ones -= temp_covered
    return final_terms

def format_expression(terms, vars_names):
    """
    Formats a Boolean expression represented by terms and variable names into a human-readable form.
    The function converts terms, which are binary strings, into a symbolic expression composed of variables
    from the vars_names list. Each '1' in the term corresponds to the inclusion of the associated variable,
    while '0' corresponds to the negation of the variable. If no terms are provided, the function returns "0 (False)".
    If a term consists entirely of dashes ('-'), the function interprets it as "1 (True)".
    """
    if not terms:
        return "0 (False)"
    if any(t == '-' * len(vars_names) for t in terms):
        return "1 (True)"
    or_parts = []
    for term in terms:
        and_parts = []
        for i, bit in enumerate(term):
            if bit == '1':
                and_parts.append(vars_names[i])
            elif bit == '0':
                and_parts.append(f"{vars_names[i]}'")
        or_parts.append("".join(and_parts))
    return " + ".join(or_parts)

def get_fnd(ones, num_vars, vars_names):
    """
    Generate the canonical representation of a boolean function in sum-of-products
    form based on truth table information.

    The function takes a list of "one" indices (truth table positions where the
    boolean function evaluates to 1), the total number of variables in the function,
    and a list of variable names. It uses this information to construct a human-readable
    sum-of-products expression.
    """
    if not ones:
        return "0"
    parts = []
    for val in sorted(ones):
        b = get_binary(val, num_vars)
        term = []
        for i, bit in enumerate(b):
            term.append(vars_names[i] if bit == '1' else f"{vars_names[i]}'")
        parts.append("".join(term))
    return " + ".join(parts)

def get_fnc(ones, dont_cares, num_vars, vars_names):
    """
    Generates a Boolean function in its canonical form as a sum of minterms for a
    given set of variables and corresponding sets of ones and don't-cares.
    """
    all_vals = set(range(2**num_vars))
    zeros = all_vals - ones - dont_cares
    if not zeros:
        return "1"
    parts = []
    for val in sorted(zeros):
        b = get_binary(val, num_vars)
        term = []
        for i, bit in enumerate(b):
            term.append(vars_names[i] if bit == '0' else f"{vars_names[i]}'")
        parts.append("(" + " + ".join(term) + ")")
    return "".join(parts)