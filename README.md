## AI Stratego: Battle Your Opponent

## **Overview**
This game is a simplified version of the classic board game **Stratego**, where a human player faces off against an AI opponent. The game features strategic piece placement, tactical movement, and hidden ranks, with AI utilizing **genetic algorithms** for board setup and **rule-based heuristics** for gameplay. 

The objective is to **capture the opponent’s flag** while defending your own. This project blends strategy and AI to create an engaging and challenging experience for players.



## **Features**
- The game is played between two players: **Red** and **Blue**.
- Each player has **16 pieces** arranged on an **8x8 grid** at the start of the game.
- Pieces include various ranks such as **Spy, Bombs, Soldiers, and Generals**.
![image](https://github.com/user-attachments/assets/e8994677-2354-49bc-bac7-85b1572f6c0b)


## **Players and Setup**
### **1. Initial Setup**
- At the start of the game, all pieces are placed face-down.  
- Only the player knows the ranks of their own pieces, while the opponent remains unaware until combat occurs.  

### **2. Rank Revealed in Combat**
- When two opposing pieces occupy the same square, their ranks are revealed.  
- The piece with the higher rank wins, while the losing piece is removed from the board.  

### **3. Objective**
- **Capture the opponent's Flag** or eliminate all their movable pieces.  
- Capturing the **Flag** results in an **immediate victory**, while eliminating all pieces leaves the opponent without options.

## **Gameplay Mechanics**

### **1. Turns**
- Players alternate turns to move their pieces.  
- Most pieces can move one square vertically or horizontally.

### **2. Piece Ranks**
- Each piece has a rank dictating its combat power.  
- Ranks range from the **Spy** (lowest) to the **Marshal** (highest).  
- During combat, the higher-ranked piece wins.

### **3. Bombs**
- Stationary pieces that destroy any opposing piece attempting to move into their square.  
- **Miners** are the only pieces capable of defusing bombs.

### **4. Flag**
- The primary target for the opponent.  
- Stationary and hidden until captured.

### **5. Special Rules**
- The **Spy** can defeat the **Marshal** but loses to all other ranks.  
- The **Miner** is the only piece capable of defusing **Bombs**.


## **Player Setup**

### **1. Human Player Setup**
- The human player manually positions their 16 pieces on their half of the board.  
- The goal is to create a balanced defensive and offensive strategy.

### **2. AI Player Setup**
- The AI uses a **Genetic Algorithm (GA)** to determine its initial setup.  
- The algorithm optimizes for factors such as:  
  - Piece safety.  
  - Board coverage.  
  - Attack potential.

## **Game Phases**

### **1. Positioning Human and AI Pieces**

#### **Human Player Setup**
The human player manually places their 16 pieces on their half of the board, focusing on a balance of offensive and defensive strategies.  

#### **AI Player Setup**
The AI’s piece placement is handled by a **Genetic Algorithm (GA)** that optimizes for:  
- Protecting critical pieces like the Flag.  
- Creating a balance between offense and defense.  
- Maximizing board coverage and minimizing vulnerabilities.  


### **2. Gameplay Mechanics**

#### **Human Player Gameplay**
The human player takes turns moving pieces, aiming to:  
- Capture opponent pieces.  
- Protect their Flag.  
- Predict and counter AI moves.

#### **AI Player Gameplay**
The AI employs **Rule-Based Heuristics** for gameplay, with strategies such as:  
- **Strategic Movements:** Prioritizing piece safety and targeting opponent pieces.  
- **Combat Strategy:** Leveraging ranks for efficiency (e.g., using the Spy against the Marshal).  
- **Piece-Specific Logic:** Miners defuse bombs, while Scouts explore the board.


## **AI Algorithms Used**

### **1. Rule-Based Heuristics**
These govern the AI’s real-time decision-making:  
- **Decision-Making Framework:** Predefined rules mimic expert strategies.  
- **Quick Tactical Responses:** The AI reacts dynamically to threats and opportunities.  
- **Key Strategies:**  
  1. **Piece Interaction Rules:** Example: Spy targeting Marshal.  
  2. **Positional Heuristics:** High-value pieces are defended while Scouts probe enemy defenses.  
  3. **Dynamic Playstyle:** Switching between offensive and defensive modes.

### **2. Genetic Algorithm**
Used for optimizing initial piece placement:  
- **Generating Diverse Setups:** Random configurations are generated.  
- **Fitness Evaluation:** Evaluates metrics like piece safety and defensive strength.  
- **Selection and Mutation:** High-performing setups are selected and enhanced.

### **3. Combined Approach**
The AI combines:  
- **Genetic Algorithm** for static optimization (initial setup).  
- **Rule-Based Heuristics** for dynamic decision-making during gameplay.  


## **Technologies Used**
- **Python 3.12**  
- **Pygame**: For game development and rendering.

## **Installation**

### Clone the Repository
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
## Happy gaming!
