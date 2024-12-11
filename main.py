import random
import numpy as np
import math
from tkinter import *
import tkinter as tk
from tkinter import messagebox
#random.seed(109) # use to get reproducible results 


class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

        # turn counter
        self.turn_number = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        
        # initializing
        current_player = self.current_player
        start = 0
        end = 0
        true_pit = 0
        
        if current_player == 1:
            start = self.p1_pits_index[0] 
            end = self.p1_pits_index[1] + 1
            
            # board is actually 0 indexed, so pit 1 corresponds to self.board[0]
            true_pit = pit - 1
            
            if true_pit in range(start, end) and self.board[true_pit] != 0:
                return True
        elif current_player == 2:
            start = self.p2_pits_index[0] 
            end = self.p2_pits_index[1] + 1 
            
            # player 2's pits are also labeled 1 to pits_per_player so pit is just an offset from p1's mancala
            true_pit = self.p1_mancala_index + pit
            
            if true_pit in range(start, end) and self.board[true_pit] != 0:
                return True
            
        return False
                
        
    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        # set seed to be different at top of method
        # random.randint produces the same sequence of numbers for the same seed
        # could also look into numpy.random
        generated_pit = random.randint(1, self.pits_per_player)
        
        while not self.valid_move(generated_pit):
            generated_pit = random.randint(1, self.pits_per_player)
            
        return generated_pit
    
    def pitIndex(self, pit):
        if self.current_player == 1:
            return self.p1_pits_index[0] + (pit - 1)
        else:
            return self.p2_pits_index[0] + (pit - 1)
    
    
    def play_turn(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        #print(f'P{self.current_player} chose pit {pit}\n')
        player = self.current_player
        index = self.pitIndex(pit)
        stones = self.board[index]
        # maybe some additional variables to set (up to you as to whether you find useful):
            # self.p1/p2_pits_index[0] -> pit_start or something similar
            # self.p1/p2_pits_index[1] -> pit_end or something similar
            # self.p1/p2_mancala_index -> my_mancala and opponent_mancala

        # could also be cool to refactor capture conditions section
            # notice how the code is virtually the same whether it is player1 or player 2
                # primary difference is for:
                    # player1: self.board[opposite] = 0
                    # player2: self.board[opposite - index] = 0
            # could create a method like evaluate_capture(self, player, start_pit, end_pit, index)
            # pulls some of the logic of dealing with captures out of the act of playing a turn



        if self.valid_move(pit) == False:
            print("INVALID MOVE")
            return
        self.moves.append((player, pit))
        self.board[index] = 0
        while stones > 0:
            index = (index +1) % len(self.board)
            if (player == 1 and index == self.p2_mancala_index) or (player == 2 and index == self.p1_mancala_index):
                continue
            self.board[index] += 1
            stones -= 1
        #Capture conditions
        if player == 1 and self.p1_pits_index[0] <= index <= self.p1_pits_index[1]:
            if self.board[index] == 1:
                opposite = self.p2_pits_index[0]+(self.p1_pits_index[1]-index)
                self.board[self.p1_mancala_index] += self.board[opposite] + self.board[index]
                self.board[opposite] = 0
                self.board[index] = 0
        elif player == 2 and self.p2_pits_index[0] <= index <= self.p2_pits_index[1]:
            if self.board[index] == 1:
                opposite = self.p1_pits_index[0]+(self.p2_pits_index[1]-index)
                self.board[self.p2_mancala_index] += self.board[opposite] + self.board[index]
                self.board[opposite] = 0
                self.board[index] = 0
        self.current_player = 2 if player == 1 else 1
        self.turn_number += 1
    
    def play_random_verse_random(self):

        # note: random seed is set at top of file
        turn_counter = 0
        self.display_board()
        while not self.winning_eval():
            move = self.random_move_generator()
            print(f"Selected pit {move}") 
            self.play_turn(move)
            self.display_board()
            turn_counter += 1

        return turn_counter

    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        # write your code here
        p1_start_pit, p1_end_pit = self.p1_pits_index
        p2_start_pit, p2_end_pit = self.p2_pits_index

        if self.winning_eval_helper(p1_start_pit, p1_end_pit) or self.winning_eval_helper(p2_start_pit, p2_end_pit):
            print("GAME OVER")
            self.evaluate_end_state()
            return True
        
        return False
           
    def winning_eval_helper(self, start_pit, end_pit):
        for pit in range(start_pit, end_pit + 1):
            if self.board[pit] == 0:
                continue
            else:
                return False
        return True
    
    def evaluate_end_state(self):
        p1_mancala = self.p1_mancala_index
        p2_mancala = self.p2_mancala_index

        if self.board[p1_mancala] > self.board[p2_mancala]:
            print("Player 1 wins!")
        elif self.board[p1_mancala] < self.board[p2_mancala]:
            print("Player 2 wins!")
        else:
            print("It's a TIE!")

def minmax_decision(state, game, depthLimit): #Note: Added a depth limit to limit run time
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state, depth):
        if game.terminal_test(state) or depth == 0:
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth - 1))
        return v

    def min_value(state, depth):
        if game.terminal_test(state) or depth == 0:
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth - 1))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a), depthLimit))

def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


class AIPlayer(Mancala):
    def __init__(self, pits_per_player=6, stones_per_pit=4):
        super().__init__(pits_per_player, stones_per_pit) #Used to avoid duplication of Mancala Class 

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        valid_moves = []
        current_player = state['currentPlayer']
        board = state['board']
        start = 0
        end = 0
        
        if current_player == 1:
            start = self.p1_pits_index[0] 
            end = self.p1_pits_index[1] + 1
            for pit in range(start, end):
                if board[pit] > 0:
                    valid_moves.append(pit - self.p1_pits_index[0]+1) # board is actually 0 indexed, so pit 1 corresponds to self.board[0]
        elif current_player == 2:
            start = self.p2_pits_index[0] 
            end = self.p2_pits_index[1] + 1 
            for pit in range(start, end):
                if board[pit] > 0:
                    valid_moves.append(pit - self.p2_pits_index[0]+1) # board is actually 0 indexed, so pit 1 corresponds to self.board[0]
        return valid_moves
    
    def utility(self, state, player): #This is the utility function that will be calculated for each individual board
        board = state['board']
        
        if player == 1:
            maxMancala = self.p1_mancala_index
            minMancala = self.p2_mancala_index #Utility function given to us to use
        else: 
            maxMancala = self.p2_mancala_index
            minMancala = self.p1_mancala_index

        return board[maxMancala] - board[minMancala] #Utility function 
    
    def getState(self): #helper function
        return {'board': self.board[:], 'currentPlayer': self.current_player} #Used a dictionary syntax to make more legible 
    
    def result(self, state, move): #What this does is it takes a state and from there it makes a move and returns the result of the move
        """Return the state that results from making a move from a state.""" 
        game = Mancala(self.pits_per_player, 0) #Don't need to initialize this because board is copied over
        game.board = state['board'][:] 
        game.current_player = state['currentPlayer']
        game.play_turn(move)
        return {'board': game.board, 'currentPlayer': game.current_player}
    
    def terminal_test_helper(self, state, start_pit, end_pit):
        """Returns True as long as the terminal state has not been reached.""" 
        board = state['board']
        for pit in range(start_pit, end_pit + 1):
            if board[pit] == 0:
                continue
            else:
                return False
        return True

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        p1_start_pit, p1_end_pit = self.p1_pits_index
        p2_start_pit, p2_end_pit = self.p2_pits_index
        return self.terminal_test_helper(state, p1_start_pit, p1_end_pit) or self.terminal_test_helper(state, p2_start_pit, p2_end_pit)

    def to_move(self, state):
        return state['currentPlayer']
        

def main():
    player1 = 0
    player2 = 0
    turns_taken = []

    for i in range(1):
        # game = Mancala(pits_per_player=6, stones_per_pit = 4)
        game = AIPlayer(pits_per_player=6, stones_per_pit = 4)
        # game.display_board()
        while not game.winning_eval():
            # random versus random logic
            # num_turns = game.play_random_verse_random()

            # random vs ai logic 
            if game.current_player == 1:
                pit = game.random_move_generator()
                game.play_turn(pit)
            else:
                # minimax
                # state = game.getState()
                # action = minmax_decision(state, game, 5) 
                # game.play_turn(action)

            #  alpha beta
               state = game.getState()
               action = alpha_beta_cutoff_search(state, game, 5, None, None)
               game.play_turn(action)

        if game.board[game.p1_mancala_index] > game.board[game.p2_mancala_index]:
            player1 += 1
        elif game.board[game.p2_mancala_index] > game.board[game.p1_mancala_index]:
            player2 += 1
        turns_taken.append(game.turn_number)
    print(f"Average number of turns taken: {math.ceil(np.mean(turns_taken))}") # print statement for random versus random
    print(f"Player 1 Wins: {player1}")
    print(f"Player 2 Wins: {player2}")

class MancalaUI:
    def __init__(self, Mancala):
        self.game = Mancala
        self.root = tk.Tk()
        self.root.title("Mancala Game")
        self.menu()
    def menu(self):
        buttonFrame = tk.Frame(self.root)
        buttonFrame.pack(pady=100)
        title = tk.Label(self.root, text="Make a Selection!", font = ("Arial", 24, "bold"))
        title.pack(pady=20)
        button0 = Button(self.root, text="Player vs Player", command=self.player_vs_player, width = 20, height = 2)
        button1 = Button(self.root, text="Player vs AI", command=self.player_vs_ai, width = 20, height = 2)
        button2 = Button(self.root, text="Player vs Random Player", command=self.player_vs_random, width = 20, height = 2)
        button0.pack()
        button1.pack()
        button2.pack()

    def setup_board(self, func):
        for widget in self.root.winfo_children(): #Clears the initial buttons
            widget.destroy()
        self.player = tk.Label(self.root, text=f"Player {self.game.current_player}'s Turn") #Keeps track of current player
        self.player.pack(pady=10)
        self.moveLabel = tk.Label(self.root, text="Last Move: None") #Used for AI and Random Player
        self.moveLabel.pack(pady=5)
        board_frame = tk.Frame(self.root) 
        board_frame.pack(pady=20) #Y-axis positioning
        self.p2_mancala_label = tk.Label(board_frame, text=f"P2-{self.game.board[self.game.p2_mancala_index]}", width=5, height=6, bg="white", fg="black") #P2 Mancala
        self.p2_mancala_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        self.p2Buttons = [] #Stores buttons n an array so they can be updated by update_board
        for i in range(self.game.pits_per_player):
            index = self.game.p2_pits_index[0] + i
            stones = self.game.board[index]
            btn = tk.Button(board_frame, text=f"P2-{stones}", width=5, height=2, command=lambda pit=(self.game.pits_per_player - i): func(pit), state=tk.NORMAL if self.game.current_player == 2 else tk.DISABLED)
            btn.grid(row=0, column=i+1)
            self.p2Buttons.append(btn) #Creates the buttons 
        self.p1Buttons = []
        for i in range(self.game.pits_per_player):
            index = self.game.p1_pits_index[0] + i
            stones = self.game.board[index]
            btn=tk.Button(board_frame, text=f"P1-{stones}", width=5, height=2, command=lambda pit = i+1: func(pit), state=tk.NORMAL if self.game.current_player == 1 else tk.DISABLED)
            btn.grid(row=1, column=i+1)
            self.p1Buttons.append(btn)
        self.p1_mancala_label = tk.Label(board_frame, text=f"P1-{self.game.board[self.game.p1_mancala_index]}", width=5, height=6, bg="white", fg="black") #P2 Mancala
        self.p1_mancala_label.grid(row=0, column=self.game.pits_per_player+1, rowspan=2, padx=10, pady=10)
        quit = tk.Button(self.root, text="Quit", command=self.root.quit)
        quit.pack(pady=1)

    def play_turn(self, pit):
        if self.game.valid_move(pit):
            self.game.play_turn(pit)
            if self.game.winning_eval(): #Logic check
                if self.game.board[self.game.p1_mancala_index] > self.game.board[self.game.p2_mancala_index]:
                    winner = "Player 1"
                elif self.game.board[self.game.p2_mancala_index] > self.game.board[self.game.p1_mancala_index]:
                    winner = "Player 2"
                tk.messagebox.showinfo("Game Over", f"Game Over! {winner} wins!")
                self.root.quit()
            else:
                self.moveLabel.pack_forget() #Hides label because we do not need it is not needed
                self.update_board()
        else:
            tk.messagebox.showerror("Invalid Move", "Please select a valid pit.")

    def update_board(self):
        p1Start = self.game.p1_pits_index[0] 
        for i, btn in enumerate(self.p1Buttons): #Returns both index and btn so we can update both dynamical
            stones = self.game.board[p1Start + i] #Updates player 1's buttons
            btn.config(text=f"P1-{stones}")
            btn.config(state=tk.NORMAL if self.game.current_player == 1 else tk.DISABLED) #Disables buttons hen it is not player turn
        p2End = self.game.p2_pits_index[1]
        for i, btn in enumerate(self.p2Buttons): #Same thing done here as above but with player 2 index logic
            stones = self.game.board[p2End - i]
            btn.config(text=f"P2-{stones}") 
            btn.config(state=tk.NORMAL if self.game.current_player == 2 else tk.DISABLED)
        self.p1_mancala_label.config(text=f"P1-{self.game.board[self.game.p1_mancala_index]}") #Updates mancala index
        self.p2_mancala_label.config(text=f"P2-{self.game.board[self.game.p2_mancala_index]}")
        self.player.config(text=f"Player {self.game.current_player}'s Turn") #Updates turn
        self.game.display_board()

    def play_turn_random(self, pit):
        if self.game.valid_move(pit):
            self.game.play_turn(pit) #Logic check
            if self.game.winning_eval():
                if self.game.board[self.game.p1_mancala_index] > self.game.board[self.game.p2_mancala_index]:
                    winner = "Player 1"
                elif self.game.board[self.game.p2_mancala_index] > self.game.board[self.game.p1_mancala_index]:
                    winner = "Player 2"
                tk.messagebox.showinfo("Game Over", f"Game Over! {winner} wins!")
                self.root.quit()
            else:
                if self.game.current_player == 2:
                    pit = self.game.random_move_generator() #Random move logic
                    self.moveLabel.config(text=f"Last Move Player {self.game.current_player} moved pit {self.game.pits_per_player - pit+1}") #Helps keep track
                    self.game.play_turn(pit)
                    self.update_board()
        else:
            tk.messagebox.showerror("Invalid Move", "Please select a valid pit.")
 
    def play_turn_ai(self, pit):
        if self.game.valid_move(pit):
            self.game.play_turn(pit)
            if self.game.winning_eval(): #Logic check
                if self.game.board[self.game.p1_mancala_index] > self.game.board[self.game.p2_mancala_index]:
                    winner = "Player 1"
                elif self.game.board[self.game.p2_mancala_index] > self.game.board[self.game.p1_mancala_index]:
                    winner = "Player 2"
                tk.messagebox.showinfo("Game Over", f"Game Over! {winner} wins!")
                self.root.quit()
            else:
                if self.game.current_player == 2:
                    state = game.getState()
                    action = alpha_beta_cutoff_search(state, game, 10, None, None) #AI logic
                    self.moveLabel.config(text=f"Last Move Player {self.game.current_player} moved pit {self.game.pits_per_player - action+1}")
                    game.play_turn(action)
                    self.update_board()
        else:
            tk.messagebox.showerror("Invalid Move", "Please select a valid pit.")

    def player_vs_random(self): # Working
        self.setup_board(self.play_turn_random)
    def player_vs_ai(self): # Working
        self.setup_board(self.play_turn_ai)
    def player_vs_player(self): # Working
        self.setup_board(self.play_turn)
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    #main()
    # uncomment for UI
    game = AIPlayer(pits_per_player=6, stones_per_pit = 5)
    app = MancalaUI(game)
    app.run()
