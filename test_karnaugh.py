import logic

def test_basic_grouping_3vars():
    ones = {0, 1, 2, 3}
    dont_cares = set()
    result = logic.minimize_karnaugh(ones, dont_cares, 3)
    assert '0--' in result
    assert len(result) == 1

def test_example():
    ones = {1, 5, 9, 13}
    dont_cares = {3, 7, 11, 15}
    result = logic.minimize_karnaugh(ones, dont_cares, 4)
    assert '---1' in result

def test_corners_map():
    ones = {0, 2, 8, 10}
    result = logic.minimize_karnaugh(ones, set(), 4)
    assert '-0-0' in result

def test_format_expression():
    vars_names = ['x', 'y', 'z', 't']
    terms = ['-0-1']
    text = logic.format_expression(terms, vars_names)
    assert text == "y't"

def test_full_map_is_one():
    ones = set(range(16))
    result = logic.minimize_karnaugh(ones, set(), 4)
    text = logic.format_expression(result, ['x', 'y', 'z', 't'])
    assert "1 (True)" in text
