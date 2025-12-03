import math
from timer import timeit

def read_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        return f.readlines()
    
    
def split_ids(line: str) -> list[tuple[int, int]]:
    parts = line.split(',')
    return [tuple(map(int, part.split('-'))) for part in parts]

def count_digits(number: int) -> int:
    return int(math.log10(number)) + 1


digit_map = {
    1: [],
    2: [1],
    3: [1],
    4: [2, 1], 
    5: [1],
    6: [3, 2, 1],
    7: [1],
    8: [4, 2, 1],
    9: [3, 1],
    10: [5, 2, 1],
    11: [1],
    12: [6, 4, 3, 2, 1],
    13: [1],
    14: [7, 2, 1],
    15: [5, 3, 1],
    16: [8, 4, 2, 1],
    17: [1],
    18: [9, 6, 3, 2, 1],
    19: [1],
    20: [10, 5, 4, 2, 1],
}


def meets_criteria_1(id_num: int) -> bool:
    num_digits = count_digits(id_num)
    if num_digits % 2 != 0:
        return False

    half = num_digits // 2
    
    div, mod = divmod(id_num, 10 ** half)
    
    return div == mod
    
def is_valid_for_divisor(num: int, divisor: int) -> bool:
    quotient, first_remainder = divmod(num, 10 ** divisor)
    
    while quotient > 0:
        quotient, remainder = divmod(quotient, 10 ** divisor)
        if remainder != first_remainder:
            return False
    
    return True

def meets_criteria_2(id_num: int) -> bool:
    num_digits = count_digits(id_num)
    
    divisors = digit_map[num_digits]
    
    for divisor in sorted(divisors, reverse=True):
        if is_valid_for_divisor(id_num, divisor):
            return True
    
    return False
    

@timeit
def solve_2(line: str):
    
    criteria_2 = []

    
    for id_pair in split_ids(line):  
        for i in range(id_pair[0], id_pair[1] + 1):
            
            if meets_criteria_2(i):
                criteria_2.append(i)
                
    return criteria_2
    
@timeit
def solve_1(line: str):
    
    criteria_1 = []

    
    for id_pair in split_ids(line):        
        for i in range(id_pair[0], id_pair[1] + 1):
                
            if meets_criteria_1(i):
                criteria_1.append(i)
                
    return criteria_1

if __name__ == "__main__":
    lines = read_file('inputs/day2.txt')
    
    criteria_1 = solve_1(lines[0])
    criteria_2 = solve_2(lines[0])
            
    print(f"Part 1: {sum(criteria_1)} [{len(criteria_1)} invalid IDs]")
    print(f"Part 2: {sum(criteria_2)} [{len(criteria_2)} invalid IDs]")
    
    
