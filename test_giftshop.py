"""
Day 2
"""
from timer import timeit


def read_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        return f.readlines()
    
    
def split_ids(line: str) -> list[tuple[int, int]]:
    parts = line.split(',')
    return [tuple(map(int, part.split('-'))) for part in parts]


@timeit
def solve_part1(id_ranges: list[tuple[int, int]]) -> int:
    
    invalid_ids = []
    for id_range in id_ranges:
        invalid_ids.extend(find_invalid_pairs(id_range[0], id_range[1]))
    
    return sum(invalid_ids)
    

def find_invalid_pairs(start: int, end: int):
    invalid = []
        
    for i in range(start, end + 1):
        id_str= str(i)
        if is_invalid(id_str, 2):
            invalid.append(i)
    
    return invalid


@timeit
def solve_part2(id_ranges: list[tuple[int, int]]) -> int:
    
    invalid_ids = []
    for id_range in id_ranges:
        invalid_ids.extend(find_invalid(id_range[0], id_range[1]))
    return sum(invalid_ids)


def find_invalid(start: int, end: int):
    invalid = []
        
    for i in range(start, end + 1):
        id_str= str(i)
        found = False
        for divisor in range(2, len(id_str) + 1):
            if not found:
                is_val_invalid = is_invalid(id_str, divisor)
                if is_val_invalid:
                    invalid.append(i)
                    found = True            
    return invalid


def split_string(text, num_chunks):
    chunk_size = len(text) // num_chunks
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def is_invalid(id_str, divisor):
    if len(id_str) % divisor == 0:
        chunks = split_string(id_str, divisor)
        
        if len(set(chunks)) == 1:
            return True



if __name__ == "__main__":
    
    lines = read_file("inputs/day2.txt")
    
    ids = split_ids(lines[0])
    
    result_part1 = solve_part1(ids)
    print(f"Result (Part 1): {result_part1}")
    
    result_part2 = solve_part2(ids)
    print(f"Result (Part 2): {result_part2}")