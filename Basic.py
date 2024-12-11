import tkinter as tk
from tkinter import messagebox

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'X'):
        return -1
    if check_winner(board, 'O'):
        return 1
    if is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_val = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move

def make_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        buttons[row][col].config(text='X')
        if check_winner(board, 'X'):
            show_result("You win!", replay_game)
        elif is_board_full(board):
            show_result("It's a draw!", replay_game)
        else:
            ai_move()
    else:
        messagebox.showerror("Error", "Invalid move")

def ai_move():
    loading_label.config(text="AI is thinking...")
    root.update()  # Update the GUI to show the loading message
    row, col = best_move(board)
    board[row][col] = 'O'
    buttons[row][col].config(text='O')
    loading_label.config(text="")  # Clear the loading message
    if check_winner(board, 'O'):
        show_result("AI wins!", replay_game)
    elif is_board_full(board):
        show_result("It's a draw!", replay_game)

def show_result(message, callback):
    disable_buttons()
    result_frame = tk.Frame(game_frame)
    result_frame.grid(row=3, column=0, columnspan=3)
    result_label = tk.Label(result_frame, text=message, font=('normal', 20))
    result_label.pack(pady=10)
    retry_button = tk.Button(result_frame, text="Retry", font=('normal', 15), command=callback)
    retry_button.pack(pady=5)

def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state='disabled')

def restart_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=' ', state='normal')
    for widget in game_frame.winfo_children():
        widget.destroy()
    start_game()

def replay_game():
    restart_game()
    start_game()

def start_game():
    global board, buttons
    board = [[' ' for _ in range(3)] for _ in range(3)]
    buttons = []
    for widget in game_frame.winfo_children():
        widget.destroy()

    for i in range(3):
        row_buttons = []
        for j in range(3):
            button = tk.Button(game_frame, text=' ', font=('normal', 30), width=5, height=2, command=lambda row=i, col=j: make_move(row, col))
            button.grid(row=i, column=j)
            row_buttons.append(button)
        buttons.append(row_buttons)

    # Add loading label
    global loading_label
    loading_label = tk.Label(game_frame, text="", font=('normal', 15))
    loading_label.grid(row=3, column=0, columnspan=3)

    game_frame.pack()

def exit_game():
    root.quit()

# Main Game Setup
root = tk.Tk()
root.title("Tic-Tac-Toe")
# Center the window on the screen
window_width = 400
window_height = 500  # Increased height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Game Frame Setup
game_frame = tk.Frame(root)

start_game()  # Start the game without the main menu

root.mainloop()