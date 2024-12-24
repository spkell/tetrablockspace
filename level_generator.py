import random
import json
from pathlib import Path
from solve import verify_level  # Add this import
import argparse
import os

def generate_level(wall_percentage, size):
    """
    Generate a 4D maze level with specified difficulty
    difficulty: 1-5 (affects number of walls and complexity)
    size: size of each dimension (can vary per difficulty)
    """
    
    # Adjust number of walls based on size and difficulty
    # Use a percentage that scales with difficulty but considers total space
    num_walls = int((size ** 4) * wall_percentage)
    
    # Initialize empty 4D space
    walls = []
    
    # Generate walls based on difficulty
    max_coord = size - 1
    while len(walls) < num_walls:
        wall = [
            random.randint(0, max_coord),
            random.randint(0, max_coord),
            random.randint(0, max_coord),
            random.randint(0, max_coord)
        ]
        if wall not in walls:
            walls.append(wall)
    
    # Generate start and goal positions
    start = [0, 0, 0, 0]  # Always start at origin
    
    # Ensure min_coord doesn't go below 0
    min_coord = max(0, max_coord//2)  # Goal between 1/2 and end of space
    goal = [
        random.randint(min_coord, max_coord),
        random.randint(min_coord, max_coord),
        random.randint(min_coord, max_coord),
        random.randint(min_coord, max_coord)
    ]
    
    # Ensure start and goal aren't walls
    if start in walls:
        walls.remove(start)
    if goal in walls:
        walls.remove(goal)
    
    level_data = {
        "walls": walls,
        "start": start,
        "goal": goal,
        "size": size,
        "difficulty": str(int(wall_percentage * 100)) + "%"
    }
    return level_data
        

def save_level(level_data, level_number):
    """Save level data to JSON file"""
    Path("levels").mkdir(exist_ok=True)
    
    filepath = f"levels/{level_number}.json"
    with open(filepath, 'w') as f:
        json.dump(level_data, f, indent=4, sort_keys=True)
    
    return filepath


def GenerateLevel(wall_percentage, size, level_id):

    print(f"Generating level with difficulty {wall_percentage} and size {size}...")

    level_data = generate_level(wall_percentage, size)

    print(f"Level generated successfully! Verifying Solvability...")
    
    # Get solvability info for display
    solvable, min_steps, solution_path = verify_level(level_data)
    
    if solvable:
        print(f"Minimum steps required: {min_steps}")
        filepath = save_level(level_data, level_id)
        print(f"Level saved to {filepath}")
    else:
        print("Level is not solvable, generating again...")
        GenerateLevel(wall_percentage, size, level_id)


def GetNextLevelId():
    levels = [int(lvl.split('.')[0]) for lvl in os.listdir('levels')]
    levels.sort(key=lambda x: int(x))
    return max(levels) + 1

# Update the main block to include verification
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate 4D maze levels')
    parser.add_argument('--wall_percentage', type=float, default=0.5,
                       help='Percentage of walls in the level (default: 0.5)')
    parser.add_argument('--size', type=int, default=5,
                        help='Size of the level dimensions (default: 5)')
    parser.add_argument('--level_id', type=int,
                       help='Level number to generate (default: auto-increment)')
    args = parser.parse_args()

    # Use the default values from argparse instead of manual checks
    level_id = args.level_id if args.level_id is not None else GetNextLevelId()
    wall_percentage = args.wall_percentage
    size = args.size

    GenerateLevel(wall_percentage, size, level_id)