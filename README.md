## STRATEGO :AI vs Human Showdown

### Overview
This game is a simplified version of the classic board game Stratego, where a human player faces off against an AI opponent. The game features strategic piece placement, tactical movement, and hidden ranks, with AI utilizing genetic algorithms for board setup and rule-based heuristics for gameplay. The objective is to capture the opponent’s flag while defending your own. The project blends strategy and AI to create an engaging and challenging experience for players.

### Features
1. Game Overview
This AI-based version of Stratego maintains the essence of the original board game while adding modern AI-driven enhancements.

Rules of Stratego
Players and Setup:

The game is played between two players: "Red" and "Blue."
Each player has 16 pieces arranged on an 8x8 grid at the start of the game.
Pieces include various ranks such as Spy, Bombs, Soldiers, and Generals.
Hidden Setup:

At the start of the game, all pieces are placed face-down.
Only the player knows the ranks of their own pieces, while the opponent is unaware until combat occurs.
Rank Revealed in Combat:

When two opposing pieces occupy the same square, their ranks are revealed.
The piece with the higher rank wins, while the losing piece is removed from the board.
Objective:

Capture the opponent's Flag or eliminate all movable pieces.
Capturing the Flag results in immediate victory, while eliminating all pieces leaves the opponent without options.
2. Gameplay Mechanics
Turns:

Players alternate turns to move their pieces.
Most pieces can move one square vertically or horizontally.
Piece Ranks:

Each piece has a rank, dictating its combat power.
Ranks range from the Spy (lowest) to the Marshall (highest).
When pieces engage in combat, the higher-ranked piece wins.
Bombs:

Stationary pieces that destroy any opposing piece attempting to move into their square.
Bombs can only be defused by Miners.
Flag:

The primary target for the opponent.
Stationary and hidden until captured.
Special Rules:

The Spy can defeat the Marshall but loses to all other ranks.
The Miner is the only piece capable of defusing Bombs.
3. Piece Details and Rank Position Count
![image](https://github.com/user-attachments/assets/e8994677-2354-49bc-bac7-85b1572f6c0b)

Human Player Setup:
The human player manually positions their 16 pieces on their half of the board to create a balanced defensive and offensive strategy.

AI Player Setup:
The AI uses a genetic algorithm to determine its initial setup, optimizing for factors such as piece safety, coverage, and attack potential.

### Technologies Used

 * Python 3.12
 * Pygame: For game development and rendering.


### Installation

Here’s how you can customize your repository setup instructions for your GitHub project based on the image provided:

---

### Clone the Repository  

To get started with the **AI Stratego Battle Your Opponent** game:  

1. Clone the repository:  
   ```bash
   git clone https://github.com/<your-github-username>/AI-Stratego-Battle-Your-Opponent.git
   cd AI-Stratego-Battle-Your-Opponent
   ```  

2. Install the dependencies:  
   ```bash
   pip install pygame
   ```  

3. Run the game:  
   ```bash
   python main.py
   ```  
Here's a polished version of the **Game Phases** section for your README file:

---

## Game Phases

### 1. Positioning Human and AI Pieces

#### **Human Player Setup**  
The human player manually positions their 16 pieces on their half of the 8x8 board. Players aim to create an effective balance of offensive and defensive strategies. The placement of pieces is critical to the overall success in the game, as it determines the effectiveness of defending the Flag and launching attacks.

#### **AI Player Setup**  
The AI’s piece placement is handled by a **Genetic Algorithm (GA)**. This ensures the AI starts with an optimized configuration based on strategic factors such as:  
- Protecting critical pieces like the Flag.  
- Creating a balance between offensive and defensive capabilities.  
- Maximizing coverage and minimizing vulnerabilities.  

The GA evaluates multiple board configurations, selecting the most effective placements through iterative optimization.

---

### 2. Gameplay Mechanics

#### **Human Player Gameplay**  
The human player takes turns to move their pieces, adhering to the rules of Stratego. Players strategize to:  
- Capture the opponent’s pieces.  
- Protect their Flag.  
- Predict and counter the AI’s moves.

#### **AI Player Gameplay**  
The AI makes decisions based on **Rule-Based Heuristics** to evaluate the current board state and respond tactically. Key AI behaviors include:  
- **Strategic Movements:** The AI prioritizes piece safety and targets key opponent pieces.  
- **Combat Strategy:** The AI leverages piece ranks to maximize combat efficiency (e.g., using the Spy to target the opponent’s Marshall).  
- **Piece-Specific Logic:** Miners defuse bombs, while Scouts explore the board to gain information.  

---

### 3. AI Algorithms Used

#### **3.1 Rule-Based Heuristics**  
Rule-Based Heuristics govern the AI’s real-time decision-making during gameplay.  

##### **How Rule-Based Heuristics Work:**  
- **Decision-Making Framework:** The AI follows predefined rules mimicking expert strategies, ensuring moves align with strategic objectives.  
- **Quick Tactical Responses:** The AI reacts instantly to changes in the game state, such as identifying threats and opportunities.  

##### **Key Strategies Implemented:**  
1. **Piece Interaction Rules:**  
   Example: If the opponent’s Marshal is nearby and the AI’s Spy is positioned advantageously, the Spy targets the Marshal.  
2. **Positional Heuristics:**  
   High-value pieces (e.g., Marshal, General) are initially positioned in defensive zones, while Scouts probe enemy defenses.  
3. **Dynamic Playstyle:**  
   - Offensive mode: AI advances strategically to capture high-value targets.  
   - Defensive mode: AI safeguards its Flag and key pieces.  

---

#### **3.2 Genetic Algorithm**  
The Genetic Algorithm is employed for **board setup optimization**, ensuring the AI’s pieces are well-positioned at the start.

##### **How the Genetic Algorithm Works:**  
1. **Generating Diverse Setups:**  
   The algorithm generates multiple random board configurations.  
2. **Fitness Evaluation:**  
   Configurations are evaluated based on metrics such as piece safety, strategic coverage, and defensive strength.  
3. **Selection and Reproduction:**  
   High-performing setups are selected and combined to create new generations.  
4. **Mutation:**  
   Random changes are introduced to maintain diversity and adaptability in strategies.  

##### **Key Advantages:**  
- Optimized setups provide long-term strategic benefits.  
- Dynamic adaptability ensures the AI can counter varied player strategies.

---

#### **3.3 Combined Approach**  
The **Genetic Algorithm** and **Rule-Based Heuristics** work together to create a well-rounded AI:  
- **Genetic Algorithm:** Focuses on static optimization for initial piece placement.  
- **Rule-Based Heuristics:** Handles dynamic gameplay decisions, adapting to the current state of the board.  

This hybrid approach ensures the AI offers both strategic depth and tactical adaptability, making gameplay challenging and engaging.


   

