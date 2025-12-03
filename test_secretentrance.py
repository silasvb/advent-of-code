from timer import timeit

LEFT = True
RIGHT = False

class SecretEntrancePart1:
    
    def __init__(self, start: int, max_position: int):
        self.start = start
        self.max_position = max_position
        
    @timeit
    def solve(self, instructions: list[str]) -> int:
        
        instr_tuples = to_instr_tuple(instructions)
        
        position = self.start
        zero_count = 0
        
        for direction, distance in instr_tuples:
            
            if direction == LEFT:
                position = (position - distance) % (self.max_position + 1)
            else:
                position = (position + distance) % (self.max_position + 1)
                
            if position == 0:
                zero_count += 1

        return zero_count
    
    
class SecretEntrancePart2:

    def __init__(self, start: int, max_position: int):
        self.start = start
        self.max_position = max_position
     
    @timeit   
    def solve(self, instructions: list[str]) -> int:
        
        instr_tuples = to_instr_tuple(instructions)
        
        position = self.start
        zero_count = 0
        
        for direction, distance in instr_tuples:
            
            prev_position = position
            
            net_distance = distance % (self.max_position + 1)
            rotations = distance // (self.max_position + 1)
            
            if direction == LEFT:
                position = (position - net_distance) % (self.max_position + 1)
            else:
                position = (position + net_distance) % (self.max_position + 1)
            
            zero_count += rotations
                
            if position == 0:
                zero_count += 1
            elif prev_position != 0:
                if direction == LEFT and prev_position < position:
                    zero_count += 1
                if direction == RIGHT and prev_position > position:
                    zero_count += 1

        return zero_count

def to_instr_tuple(instructions):
    return [
            (LEFT if line[0] == 'L' else RIGHT, int(line[1:]))
            for line in instructions
        ]

def readlines(filename: str):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
if __name__ == "__main__":
    instructions = readlines("inputs/day1-1.txt")
    
    print("Solving Day 1 (Part 1)...")
    
    r1 = SecretEntrancePart1(50, 99).solve(instructions)
    print(r1)
    
    print("Solving Day 1 (Part 2)...")
    r2 = SecretEntrancePart2(50, 99).solve(instructions)
    print(r2)
    

"""Tests"""

def test_example():
    instructions = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]
    
    assert SecretEntrancePart1(50, 99).solve(instructions) == 3
    

def test_example2():
    instructions = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]
    
    assert SecretEntrancePart2(50, 99).solve(instructions) == 6
