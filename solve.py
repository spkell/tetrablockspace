from collections import deque
from typing import List, Dict, Set, Tuple
import json
from pathlib import Path
import argparse
import sys

def is_valid_move(pos: List[int], size: int, walls: List[List[int]]) -> bool:
    """Check if a position is valid (within bounds and not a wall)."""
    return (all(0 <= x < size for x in pos) and 
            pos not in walls)

def get_neighbors(pos: List[int], size: int, walls: List[List[int]]) -> List[List[int]]:
    """Get all valid neighboring positions in 4D space."""
    neighbors = []
    # Check all possible moves in each dimension (±1 in each dimension)
    for dim in range(4):  # 4 dimensions: X, Y, Z, T
        for delta in [-1, 1]:
            new_pos = pos.copy()
            new_pos[dim] += delta
            if is_valid_move(new_pos, size, walls):
                neighbors.append(new_pos)
    return neighbors

def bfs_solve(start: List[int], goal: List[int], size: int, 
              walls: List[List[int]]) -> Tuple[bool, List[List[int]], int]:
    """
    Solve the 4D maze using BFS.
    Returns:
        - bool: Whether a solution exists
        - List[List[int]]: The path from start to goal
        - int: Number of steps in the solution
    """
    queue = deque([(start, [start])])  # (current_pos, path_so_far)
    visited = {tuple(start)}
    
    while queue:
        current_pos, path = queue.popleft()
        
        if current_pos == goal:
            return True, path, len(path) - 1  # -1 because we don't count starting position
        
        for next_pos in get_neighbors(current_pos, size, walls):
            next_pos_tuple = tuple(next_pos)
            if next_pos_tuple not in visited:
                visited.add(next_pos_tuple)
                queue.append((next_pos, path + [next_pos]))
    
    return False, [], 0

def verify_level(level_data: Dict) -> Tuple[bool, int, List[List[int]]]:
    """
    Verify if a level is solvable and return solution details.
    Returns:
        - bool: Whether the level is solvable
        - int: Minimum number of steps needed
        - List[List[int]]: The solution path
    """
    start = level_data['start']
    goal = level_data['goal']
    size = level_data['size']
    walls = level_data['walls']
    
    solvable, path, steps = bfs_solve(start, goal, size, walls)
    return solvable, steps, path

def main():
    """Test specific level or all levels based on command line argument."""
    parser = argparse.ArgumentParser(description='Solve 4D maze levels')
    parser.add_argument('--level', type=int, help='Level number to solve (optional)')
    args = parser.parse_args()

    levels_path = Path("levels")
    
    if args.level is not None:
        # Test specific level
        level_file = levels_path / f"{args.level}.json"
        if not level_file.exists():
            print(f"Error: Level {args.level} does not exist!")
            sys.exit(1)
            
        print(f"\nTesting {level_file.name}...")
        with open(level_file, 'r') as f:
            level_data = json.load(f)
        
        solvable, min_steps, solution_path = verify_level(level_data)
        
        if solvable:
            print(f"✓ Level {args.level} is solvable!")
            print(f"Minimum steps required: {min_steps}")
            print(f"Solution path:")
            for i, pos in enumerate(solution_path):
                print(f"Step {i}: {pos}")
        else:
            print(f"✗ Level {args.level} is NOT solvable!")
    else:
        # Test all levels
        for level_file in sorted(levels_path.glob("level_*.json")):
            print(f"\nTesting {level_file.name}...")
            
            with open(level_file, 'r') as f:
                level_data = json.load(f)
            
            solvable, min_steps, solution_path = verify_level(level_data)
            
            if solvable:
                print(f"✓ Level is solvable!")
                print(f"Minimum steps required: {min_steps}")
            else:
                print(f"✗ Level is NOT solvable!")

if __name__ == "__main__":
    main() 