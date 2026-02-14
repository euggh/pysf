import random

# create board for game 
def boardgame(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

# check win combination (row, column, diagonal)
def wingame(board, player):
    winline = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))
    return any(board[i] == board[j] == board[k] == player for i, j, k in winline)

# create list 1 to 9, player begin first and use X 
def warbattle():
    board = [str(i + 1) for i in range(9)]
    current_player = "X"
    
# game cycle, max 9 turn
    for turn in range(9):
        boardgame(board)
        
# human turn
        if current_player == "X":
            while True:
                move = input(f"Ваш ход ({current_player}), клетка номер: ")

# check input number and cell is clear (not fill X or O)
                if move.isdigit() and 1 <= int(move) <= 9 and board[int(move)-1] not in "XO":
                    idx = int(move) - 1
                    break
                print("клетка занята.")
        else:

# pc turn
            print("Ход компьютера (0)")

# search empty cells
            empty_cells = [i for i, s in enumerate(board) if s not in "XO"]

# choice random cell
            idx = random.choice(empty_cells)

# put symbol in sell            
        board[idx] = current_player

# check if current turn is win        
        if wingame(board, current_player):
            boardgame(board)
            print(f"Победа {current_player}!")
            return

# change gamer O->X, X->O        
        current_player = "O" if current_player == "X" else "X"
    
# After 9 turn, no winner
    boardgame(board)
    print("Ничья!")

# begin programm
if __name__ == "__main__":
    warbattle()
    