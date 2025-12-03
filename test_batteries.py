import pytest
from timer import timeit


def read_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        return f.readlines()

def parse_input(banks: list[list[str]]) -> list[list[int]]:
    
    parsed_banks = []
    
    for bank in banks:
        b = bank.strip()
        digits = []        
        for i in range(len(b)):
            digits.append(int(b[i]))    

        parsed_banks.append(digits)

    return parsed_banks


def parse_bank(bank: list[int]):
    
    map = {i: [] for i in range(10)}
    
    for position, digit in enumerate(bank):
        map[digit].append(position)
        
    return map

def does_bank_contain_digit(bank: dict[int, list[int]], ten: int, unit) -> bool:
    if not bank[ten] or not bank[unit]:
        return False

    lowest_ten_pos = bank[ten][0]
    highest_unit_pos = bank[unit][-1]
    
    return lowest_ten_pos < highest_unit_pos

def largest_single_value(bank) -> int:
    for i in range(9, -1, -1):
        for j in range(9, -1, -1):
            min_tens = bank[i][0] if bank[i] else None
            max_units = bank[j][-1] if bank[j] else None
            if min_tens is not None and max_units is not None and min_tens < max_units:
                return i * 10 + j
    

def largest_value(bank, digits) -> int:
    
    max_idx = max(max(positions) for positions in bank.values() if positions != [])
    max_pos = max_idx - digits  
    min_pos = 0
    solution = []
    
    for i in range(digits):
        found, (digit, position) = get_next_digit(bank, min_pos, max_pos)
        
        if not found:
            raise Exception("No valid digit found")
        
        max_pos = max_idx - (digits - (i + 2))
        min_pos = position + 1
        
        solution.append(digit)
        
    return int(''.join(map(str, solution)))

def get_next_digit(bank, min_pos, max_pos):
        for i in range(9, -1, -1):
            viable = [v for v in bank[i] if min_pos <= v <= max_pos]
            if viable:
                latest_viable = viable[0]
                return (True, (i, latest_viable))
            
        return (False, None)
    

def find_greatest(banks) -> int:
    for i in range(99, 0):
        if all(does_bank_contain_digit(bank, i // 10, i % 10) for bank in banks):
            return i
    return -1
    

@timeit
def solve_1(parsed_banks):
    return [largest_single_value(bank) for bank in parsed_banks] 

@timeit
def solve_2(parsed_banks, length):
    return [largest_value(bank, length) for bank in parsed_banks]

@timeit
def preprocess(banks):
    return [parse_bank(bank) for bank in banks]


def test_input_example():
    lines = ["987654321111111","811111111111119", "234234234234278", "818181911112111"]
    banks = parse_input(lines)
    parsed_banks = [parse_bank(bank) for bank in banks]
    
    combined = sum(largest_single_value(bank) for bank in parsed_banks)
    assert combined == 357

def test_input_example_part_2():
    lines = ["987654321111111","811111111111119", "234234234234278", "818181911112111"]
    banks = parse_input(lines)
    parsed_banks = [parse_bank(bank) for bank in banks]
    
    largest_value_0 = largest_value(parsed_banks[0], 12)
    largest_value_1 = largest_value(parsed_banks[1], 12)
    largest_value_2 = largest_value(parsed_banks[2], 12)
    largest_value_3 = largest_value(parsed_banks[3], 12)

    assert largest_value_0 == 987654321111
    assert largest_value_1 == 811111111119
    assert largest_value_2 == 434234234278
    assert largest_value_3 == 888911112111
    
    

def test_parse_bank():
    assert parse_bank([0, 2, 7, 0]) == {
        0: [0, 3],
        1: [],
        2: [1],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [2],
        8: [],
        9: []
    }
    
    
def test_bank_contains_digit():
    bank = parse_bank([1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
    assert does_bank_contain_digit(bank, 2, 3)

def test_bank_does_not_contain_digit():
    bank = parse_bank([1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
    assert not does_bank_contain_digit(bank, 6, 2)
    assert not does_bank_contain_digit(bank, 2, 6)

def test_bank_contains_wrong_order():
    bank = parse_bank([1, 2, 3, 4, 5, 2, 3, 4, 5])
    assert not does_bank_contain_digit(bank, 5, 1)
    
    
@timeit
def generic_solve(string, number_of_digits):
    array = list(map(int, string.strip()))
    
    def find_digits(remaining, min_pos, result):
        if remaining == 0:
            return result
        
        max_pos = len(array) - remaining
        sub_array = array[min_pos:max_pos + 1]
        max_val = max(sub_array)
        position = sub_array.index(max_val) + min_pos
        
        return find_digits(remaining - 1, position + 1, result + [max_val])
    
    solution = find_digits(number_of_digits, 0, [])
    return int(''.join(map(str, solution)))

@pytest.mark.parametrize("string,number_of_digits,expected", [
    ("987654321111111", 2, 98),
    ("811111111111119", 2, 89),
    ("234234234234278", 2, 78),
    ("818181911112111", 2, 92),    
    ("987654321111111", 12, 987654321111),
    ("811111111111119", 12, 811111111119),
    ("234234234234278", 12, 434234234278),
    ("818181911112111", 12, 888911112111),
])    
def test_efficient_solve(string, number_of_digits, expected):
    sol = generic_solve(string, number_of_digits)
    assert sol == expected
    
def solve_generic_v2(banks, number_of_digits):
    return [generic_solve(bank, number_of_digits) for bank in banks]


if __name__ == "__main__":
    lines = read_file('inputs/day3.txt')
    banks = parse_input(lines)
    parsed_banks = preprocess(banks)
    
    max_vals = solve_1(parsed_banks)
    print(f"Part 1: Greatest valid two-digit number: {sum(max_vals)}")
    
    max_vals_part_2 = solve_2(parsed_banks, 12)
    print(f"Part 2: Greatest valid twelve-digit number: {sum(max_vals_part_2)}")
    
    max_vals_p1_efficient = solve_generic_v2(lines, 2)
    print(f"Part 1 (rewrite): Greatest valid two-digit number: {sum(max_vals_p1_efficient)}")
    
    max_vs_p2_efficient = solve_generic_v2(lines, 12)
    print(f"Part 2 (rewrite): Greatest valid twelve-digit number: {sum(max_vs_p2_efficient)}")
    
