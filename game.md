Theres a game called tetraspace that allows you to navigate a 4D maze in 3D, that allows you to navigate on flat ground (want to move via arrow keys). You can also click a button that allows you to fold from one dimension to another. Suppose I'm in dimension (red, green, blue). I can shift to (X: red, Y: yellow, Z: green, T: blue) dimension, and explore that dimension of the maze, to reach the goal location. How can i do this using a block traveling through block space?


Suppose I'm. in (0,0) in XY (View 1). I switch to YT (View 2) and move to (5,5). I shift back to XY (View 3). View 1 and 3 should be different because I moved through 4d space, even though I'm in XY?

Dimensions: (X, Y, Z, T)
Possible 2D navigation planes:

XY plane - Moving in X and Y dimensions while Z and T are fixed
XZ plane - Moving in X and Z dimensions while Y and T are fixed 
XT plane - Moving in X and T dimensions while Y and Z are fixed
YZ plane - Moving in Y and Z dimensions while X and T are fixed
YT plane - Moving in Y and T dimensions while X and Z are fixed
ZT plane - Moving in Z and T dimensions while X and Y are fixed

So there are 6 possible 2D planes that can be navigated through in 4D space. When you switch between these planes, your position in the other two dimensions remains fixed, but you can move freely in the two dimensions of your current plane.


##### Usage
python3 main.py
python3 level_generator.py
python3 solve.py 2


###### Blockchain integration for smart contract pay to play

1. Smart Contract Architecture
- NFT contract for level access tokens
- Game state contract for tracking player progress
- Payment contract for handling entry fees and rewards

2. Hidden Information Model
- Server keeps full maze layout encrypted
- Only reveals visible cells in current 2D plane to player
- Sends minimal state updates to blockchain:
  - Player position 
  - Currently visible walls
  - Score/steps taken
  - Current plane view

3. Server Architecture 
- Maintains authoritative game state
- Validates all moves server-side
- Only reveals partial maze information based on player position
- Signs state updates before sending to blockchain

4. Anti-Cheat Measures
- Rate limiting on moves
- Server-side validation of all state transitions
- Encrypted level data with progressive revelation
- Monitoring for suspicious patterns
+ Maze Randomization:
  - Each game instance uses a unique maze seed
  - Maze layout changes between attempts
  - Position of goals and key points randomized
+ Movement Restrictions:
  - Cooldown period between plane switches
  - Maximum number of plane switches per attempt
  - Energy system limiting exploration per session
+ State Validation:
  - Server maintains encrypted hash of full maze state
  - Client receives only necessary visibility data
  - Position updates require proof of previous state
+ Pattern Detection:
  - Analysis of movement patterns for bot detection
  - Flagging of systematic exploration attempts
  - Penalties for suspected automated play

5. Blockchain Integration Flow
    1. Player purchases level access NFT
    2. Smart contract verifies NFT ownership
    3. Server generates unique randomized maze instance
    4. For each move:
        - Client sends move request with current state hash
        - Server validates move legitimacy and state hash
        - Server reveals only newly visible areas
        - Encrypted state update pushed to blockchain
    5. On completion:
        - Smart contract verifies legitimate solution path
        - Anti-farming checks before reward distribution

6. Economic Model
- Entry fee paid in tokens/ETH
- Rewards pool funded by entry fees
+ Payout Criteria:
  - Base reward for maze completion
  - Bonus multipliers based on:
    * Number of moves used (efficiency score)
    * Time taken to complete
    * Difficulty rating of generated maze
    * Number of dimension switches used
  - Performance percentile compared to other players on same maze seed
  - Anti-farming decay: reduced rewards for multiple attempts in short time period

7. Maze Difficulty Standardization
- Server generates mazes using controlled parameters:
  * Fixed complexity score based on:
    - Minimum required dimension switches
    - Path length to optimal solution
    - Number of dead ends
    - Branching factor at decision points
  * Difficulty rating verified before maze deployment
  * Similar difficulty level maintained across random seeds
  * Maze generation parameters stored in smart contract

8. Reward Distribution System
- Smart contract validates:
  * Legitimate maze completion
  * Solution efficiency metrics
  * Player's completion time
  * Number of moves used
- Payout formula:  ```solidity
  reward = baseReward * 
          efficiencyMultiplier * 
          difficultyMultiplier * 
          (1 - attemptDecayFactor)  ```
- Maximum reward capped per difficulty tier
- Minimum performance threshold for payout eligibility
- Cool-down period between reward-eligible attempts
