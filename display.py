def get_cell_char(val, ones, dont_cares):
    """
    Determines the character representation for a given cell value by checking
    its presence in specified sets of ones and don't-care conditions.
    """
    if val in ones:
        return " 1 "
    if val in dont_cares:
        return " X "
    return " 0 "

def generate_truth_table_file(ones, dont_cares, num_vars, vars_names, filename="truth_table.txt"):
    """
    Generates a truth table file based on specified parameters.
    The function writes a truth table to a file where the table includes all input variable combinations
    and their corresponding output values. Outputs are determined by the provided sets of minterms
    (`ones`) and "don't care" terms (`dont_cares`). The remaining terms default to 0. The file is
    written in a readable tabular format.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            header = " | ".join(vars_names) + " | f"
            f.write(header + "\n")
            f.write("-" * len(header) + "\n")
            for i in range(2**num_vars):
                row_vals = format(i, f'0{num_vars}b')
                line = " | ".join(list(row_vals))
                res = "0"
                if i in ones:
                    res = "1"
                elif i in dont_cares:
                    res = "X"
                f.write(f"{line} | {res}\n")
        return True
    except IOError:
        return False

def print_karnaugh_map(ones, dont_cares, num_vars, vars_names):
    """
    Prints the Karnaugh map for a given number of variables, using the provided
    truth table inputs (`ones` and `dont_cares`) and corresponding variable names.
    The output is displayed in tabular format, where '1', 'X', or a blank represent
    `ones`, `dont_cares`, and undefined values, respectively. The function supports
    3-variable and 4-variable Karnaugh maps.
    """
    print(f"\n KARNAUGH DIAGRAM ({num_vars} Variables)")
    print(" " + "-" * 30)
    gray_code = [0, 1, 3, 2]
    if num_vars == 3:
        row_var = vars_names[0]
        col_vars = vars_names[1] + vars_names[2]
        print(f"      {col_vars}")
        print(f"      00  01  11  10")
        print("     +---+---+---+---+")
        for r in range(2):
            row_str = f" {row_var}={r} |"
            for c_idx in gray_code:
                val = (r << 2) | c_idx
                row_str += get_cell_char(val, ones, dont_cares) + "|"
            print(row_str)
            print("     +---+---+---+---+")
    elif num_vars == 4:
        row_vars = vars_names[0] + vars_names[1]
        col_vars = vars_names[2] + vars_names[3]
        print(f"       {col_vars}")
        print(f"       00  01  11  10")
        print("      +---+---+---+---+")
        for r_idx in gray_code:
            row_binary = format(r_idx, '02b')
            row_str = f" {row_vars}={row_binary}|"
            for c_idx in gray_code:
                val = (r_idx << 2) | c_idx
                row_str += get_cell_char(val, ones, dont_cares) + "|"
            print(row_str)
            print("      +---+---+---+---+")