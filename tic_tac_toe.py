import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self):
        """Initialize the game window"""
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        self.board = [" " for _ in range(9)]  # 3x3 board
        self.current_player = "X"  # Default first player
        self.buttons = []  # Stores button references

        self.create_board()
        self.ai_player = None
        self.human_player = None

        # Add Restart Button
        self.restart_button = tk.Button(self.window, text="Restart", font=("Arial", 16), command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=3)

    def create_board(self):
        """Create the 3x3 board UI"""
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.window, text=" ", font=("Arial", 24), height=2, width=5,
                                command=lambda row=i, col=j: self.make_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons.append(btn)

    def make_move(self, row, col):
        """Handle move when player clicks a button"""
        index = row * 3 + col  # Convert (row, col) to index
        if self.board[index] == " " and self.current_player == self.human_player:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state=tk.DISABLED)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.disable_board()
                return

            if " " not in self.board:
                messagebox.showinfo("Game Over", "It's a Tie!")
                self.disable_board()
                return

            self.current_player = self.ai_player  # Switch to AI player

            # After the human player moves, AI makes its move
            self.ai_move()

    def ai_move(self):
        """AI makes its move using the Minimax algorithm"""
        best_score = -math.inf
        best_move = None

        for index in self.available_moves():
            self.board[index] = self.ai_player
            score = self.minimax(self.board, 0, False)
            self.board[index] = " "  # Undo the move

            if score > best_score:
                best_score = score
                best_move = index

        # Make the best move for AI
        self.board[best_move] = self.ai_player
        self.buttons[best_move].config(text=self.ai_player, state=tk.DISABLED)

        if self.check_winner():
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.disable_board()
            return

        if " " not in self.board:
            messagebox.showinfo("Game Over", "It's a Tie!")
            self.disable_board()
            return

        self.current_player = self.human_player  # Switch to human player

    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm to calculate the best move for AI"""
        winner = self.check_winner()
        if winner == self.ai_player:
            return 1
        elif winner == self.human_player:
            return -1
        elif " " not in board:
            return 0  # Tie

        if is_maximizing:
            best_score = -math.inf
            for index in self.available_moves():
                board[index] = self.ai_player
                score = self.minimax(board, depth + 1, False)
                board[index] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for index in self.available_moves():
                board[index] = self.human_player
                score = self.minimax(board, depth + 1, True)
                board[index] = " "
                best_score = min(score, best_score)
            return best_score

    def available_moves(self):
        """Return list of available moves"""
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def check_winner(self):
        """Check if someone has won"""
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combos:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return self.board[combo[0]]
        return None

    def disable_board(self):
        """Disable all buttons after game ends"""
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def restart_game(self):
        """Restart the game by resetting the board"""
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

        for btn in self.buttons:
            btn.config(text=" ", state=tk.NORMAL)

    def ai(self, player):
        """Set AI player"""
        self.ai_player = player

    def human(self, player):
        """Set human player"""
        self.human_player = player

    def start(self):
        """Launch the game window"""
        self.window.mainloop()
