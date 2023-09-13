import tkinter as tk
from tkinter import messagebox
import random

# Định nghĩa biến toàn cục
board_size = 9
board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
player_turn = True

def print_board():
    for i in range(board_size):
        for j in range(board_size):
            button_grid[i][j].config(text=board[i][j])

def check_win(player):
    for i in range(board_size):
        for j in range(board_size):
            if i + 4 < board_size and all(board[i + k][j] == player for k in range(5)):
                return True
            if j + 4 < board_size and all(board[i][j + k] == player for k in range(5)):
                return True
            if i + 4 < board_size and j + 4 < board_size and all(board[i + k][j + k] == player for k in range(5)):
                return True
            if i + 4 < board_size and j - 4 >= 0 and all(board[i + k][j - k] == player for k in range(5)):
                return True
    return False

def is_full():
    return all(cell != ' ' for row in board for cell in row)

def computer_move():
    global player_turn
    if is_full() or check_win('X') or check_win('O'):
        return

    best_score = float('-inf')
    best_move = None

    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
        player_turn = True
        print_board()
        if check_win('O'):
            messagebox.showinfo("Kết quả", "Máy tính thắng!")
        elif is_full():
            messagebox.showinfo("Kết quả", "Hòa!")

def minimax(board, depth, maximizing_player):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if is_full():
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

def on_click(i, j):
    global player_turn
    if player_turn and board[i][j] == ' ':
        board[i][j] = 'X'
        player_turn = False
        print_board()
        if check_win('X'):
            messagebox.showinfo("Kết quả", "Người chơi thắng!")
        elif is_full():
            messagebox.showinfo("Kết quả", "Hòa!")
        else:
            computer_move()

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Caro 9x9")

button_grid = [[None for _ in range(board_size)] for _ in range(board_size)]

for i in range(board_size):
    for j in range(board_size):
        button_grid[i][j] = tk.Button(root, text=' ', font=('normal', 20), width=2, height=1,
                                      command=lambda i=i, j=j: on_click(i, j))
        button_grid[i][j].grid(row=i, column=j)

root.mainloop()
