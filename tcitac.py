import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtCore import QTimer

PLAYER = 'X'
AI = 'O'
EMPTY = '_'

def create_empty_board():
    return [EMPTY] * 9
# Create an empty board for Tic-Tac-Toe
def is_winner(board, player):
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_combinations)

def is_draw(board):
    return EMPTY not in board and not is_winner(board, PLAYER) and not is_winner(board, AI)

def evaluate(board):
    if is_winner(board, AI):
        return 10
    elif is_winner(board, PLAYER):
        return -10
    else:
        return 0

def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot == EMPTY]

def alpha_beta(board, alpha, beta, is_maximizing):
    score = evaluate(board)
    if score in [10, -10] or is_draw(board):
        return score

    if is_maximizing:
        best = -float('inf')
        for move in get_available_moves(board):
            board[move] = AI
            best = max(best, alpha_beta(board, alpha, beta, False))
            board[move] = EMPTY
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for move in get_available_moves(board):
            board[move] = PLAYER
            best = min(best, alpha_beta(board, alpha, beta, True))
            board[move] = EMPTY
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def find_best_move(board):
    best_score = -float('inf')
    best_move = -1
    for move in get_available_moves(board):
        board[move] = AI
        score = alpha_beta(board, -float('inf'), float('inf'), False)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


class TicTacToeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe with AI (Minimax + Alpha-Beta)")
        self.board = create_empty_board()
        self.current_turn = 'X'
        self.buttons = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.status_label = QLabel("Your Turn (X)")
        main_layout.addWidget(self.status_label)

        grid_layout = QVBoxLayout()
        for i in range(3):
            row = QHBoxLayout()
            for j in range(3):
                index = i * 3 + j
                btn = QPushButton("")
                btn.setFixedSize(100, 100)
                btn.clicked.connect(lambda checked, idx=index: self.player_move(idx))
                self.buttons.append(btn)
                row.addWidget(btn)
            grid_layout.addLayout(row)
        main_layout.addLayout(grid_layout)

        self.reset_button = QPushButton("Restart Game")
        self.reset_button.clicked.connect(self.reset_game)
        main_layout.addWidget(self.reset_button)

        self.setLayout(main_layout)

    def player_move(self, index):
        if self.board[index] != EMPTY or self.current_turn != PLAYER:
            return

        self.board[index] = PLAYER
        self.update_button(index, PLAYER)
        self.check_game_end(PLAYER)
        self.current_turn = AI
        self.status_label.setText("AI Thinking...")
        QTimer.singleShot(500, self.ai_move)

    def ai_move(self):
        move = find_best_move(self.board)
        if move != -1:
            self.board[move] = AI
            self.update_button(move, AI)
        self.check_game_end(AI)
        self.current_turn = PLAYER
        self.status_label.setText("Your Turn (X)")

    def update_button(self, index, symbol):
        self.buttons[index].setText(symbol)
        self.buttons[index].setEnabled(False)

    def check_game_end(self, player):
        if is_winner(self.board, player):
            self.status_label.setText(f"{player} wins!")
            self.show_message(f"{player} wins!")
            self.disable_all_buttons()
        elif is_draw(self.board):
            self.status_label.setText("It's a draw!")
            self.show_message("It's a draw!")
            self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.setEnabled(False)

    def reset_game(self):
        self.board = create_empty_board()
        self.current_turn = PLAYER
        self.status_label.setText("Your Turn (X)")
        for btn in self.buttons:
            btn.setText("")
            btn.setEnabled(True)

    def show_message(self, text):
        QMessageBox.information(self, "Game Over", text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = TicTacToeGame()
    game.show()
    sys.exit(app.exec())
