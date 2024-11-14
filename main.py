import random
random.seed(109)

#This is the project:
#Ethans valid move function
#Sawyers play function needs adjustment
#
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
        
        # write your code here
        generated_pit = random.randint(1, self.pits_per_player)
        while not self.valid_move(generated_pit):
            generated_pit = random.randint(1, self.pits_per_player)
            
        return generated_pit
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        print(f'P{self.current_player} chose pit {pit}\n')
        
        
        # write your code here
        if self.valid_move(pit) == False:
            print("INVALID MOVE")
            return
        pit -= 1
        if self.current_player == 1:
            index = self.p1_pits_index[0] + pit
        else:
            index = self.p2_pits_index[0] + pit
        self.moves.append((self.current_player, pit+1))
        stones = self.board[index]
        self.board[index] = 0
        while stones > 0:
            index = (index +1) % len(self.board)
            if (self.current_player == 1 and index == self.p2_mancala_index) or (self.current_player == 2 and index == self.p1_mancala_index):
                continue
            self.board[index] += 1
            stones -= 1
        if self.current_player == 1 and self.p1_pits_index[0] <= index <= self.p1_pits_index[1]:
            if self.board[index] == 1:
                opposite = self.p2_pits_index[0]+(self.p1_pits_index[1]-index)
                self.board[self.p1_mancala_index] += self.board[opposite] + self.board[index]
                self.board[opposite] = 0
                self.board[index] = 0
        elif self.current_player == 2 and self.p2_pits_index[0] <= index <= self.p2_pits_index[1]:
            if self.board[index] == 1:
                opposite = self.p1_pits_index[0]+(self.p2_pits_index[1]-index)
                self.board[self.p2_mancala_index] += self.board[opposite] + self.board[index]
                self.board[opposite - index] = 0
                self.board[index] = 0
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        if self.winning_eval() == False:
            return
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        # write your code here
        if self.winning_eval_helper(1) or self.winning_eval_helper(2):
            return True
        
        return False
        
        
    
    def winning_eval_helper(self, player):
        if player == 1:
            for pit in range(self.p1_pits_index[0], self.p1_pits_index[1]):
                if self.board[pit] == 0:
                    continue
                else:
                    return False

            return True
        else:
            for pit in range(self.p2_pits_index[0], self.p2_pits_index[1]):
                if self.board[pit] == 0:
                    continue
                else:
                    return False
            
            return True

def main():
    game = Mancala(pits_per_player=9, stones_per_pit = 4)
    game.display_board()
    game.play(1)
    game.display_board()
    game.play(1)
    game.play(1)
if __name__ == "__main__":
    main()

