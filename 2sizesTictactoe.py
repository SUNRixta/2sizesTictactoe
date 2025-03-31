import sys

board = [[' ' for _ in range(3)] for _ in range(3)]
board_size = [[0 for _ in range(3)] for _ in range(3)]
X_sizes = [3, 3]
O_sizes = [3, 3]

def print_board(board, board_size):
    print("\nPlay Board:")
    print("    0     1     2")
    print("  ----- ----- -----")
    for i in range(3):
        display_row = []
        for j in range(3):
            cell = board[i][j]
            if cell == 'X':
                if board_size[i][j] == 1:
                    display_row.append(' x ')
                else:
                    display_row.append(' X ')
            elif cell == 'O':
                if board_size[i][j] == 1:
                    display_row.append(' o ')
                else:
                    display_row.append(' O ')
            else:
                display_row.append('   ') 
        print(f"{i} |{' | '.join(display_row)}|")
        print("  -----------------")

    print("\nSize Board:")
    print("    0     1     2")
    print("  ----- ----- -----")
    for i in range(3):
        size_row = []
        for j in range(3):
            size_row.append(f" {board_size[i][j]} ")
        print(f"{i} |{' | '.join(size_row)}|")  
        print("  ----- ----- -----")  

    print("\nRemaining Pieces:")
    print(f"Player (X): Small ({X_sizes[0]}), Big ({X_sizes[1]})")
    print(f"Computer (O): Small ({O_sizes[0]}), Big ({O_sizes[1]})")

def get_possible_size(current_sizes, validate):
    size_availables = []
    for i in range(2):
        if current_sizes[i] > 0:
            size_availables.append(i + 1)

    if validate:
        return size_availables

    if sum(X_sizes) > 3:
        return [size_availables[1]]

    if sum(X_sizes) < 3:
        return size_availables

    if len(size_availables) > 0:
        return size_availables[-2:]
    return size_availables

def find_choices(board, board_size, side, current_sizes, validate=False):
    available_choices = []
    possible_size = get_possible_size(current_sizes, validate)
    for p_size in possible_size:
        for row in range(3):
            for col in range(3):
                isOwnMark = board[row][col] == side
                canPlace = board_size[row][col] < p_size
                sizeBlock = (p_size - 1) * 9
                rowBlock = row * 3
                if not isOwnMark and canPlace:
                    available_choices.append(sizeBlock + rowBlock + col)
    return available_choices

def is_board_full(side, current_sizes):
    choices = find_choices(board, board_size, side, current_sizes, validate=True)

    if len(choices) == 0 and sum(current_sizes) == 0:
        return True 
    return False 


def is_winner(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw_win(player):
    return sum(row.count(player) for row in board) > 4

def minimax(depth, is_maximizing):
    if is_winner('X'):
        return -1
    if is_winner('O'):
        return 1
    if is_board_full('O' if is_maximizing else 'X', O_sizes if is_maximizing else X_sizes):
        return 0.5 if check_draw_win('O') else -0.5

    if is_maximizing:
        max_eval = -sys.maxsize
        possible_choices = find_choices(board, board_size, 'O', O_sizes)
        for p_choice in possible_choices:
            select_size = int(p_choice / 9 + 1)
            slot = p_choice % 9
            row = int(slot / 3)
            col = slot % 3

            prev_size = board_size[row][col]
            prev_side = board[row][col]

            board[row][col] = 'O'
            board_size[row][col] = select_size
            O_sizes[select_size - 1] -= 1
            eval = minimax(depth + 1, False)

            board[row][col] = prev_side
            board_size[row][col] = prev_size
            O_sizes[select_size - 1] += 1

            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = sys.maxsize
        possible_choices = find_choices(board, board_size, 'X', X_sizes)
        for p_choice in possible_choices:
            select_size = int(p_choice / 9 + 1)
            slot = p_choice % 9
            row = int(slot / 3)
            col = slot % 3

            prev_size = board_size[row][col]
            prev_side = board[row][col]

            board[row][col] = 'X'
            board_size[row][col] = select_size
            X_sizes[select_size - 1] -= 1
            eval = minimax(depth + 1, True)

            board[row][col] = prev_side
            board_size[row][col] = prev_size
            X_sizes[select_size - 1] += 1

            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move():
    possible_choices = find_choices(board, board_size, 'O', O_sizes)
    for p_choice in possible_choices:
        select_size = int(p_choice / 9 + 1)
        slot = p_choice % 9
        row = int(slot / 3)
        col = slot % 3

        prev_size = board_size[row][col]
        prev_side = board[row][col]

        board[row][col] = 'O'
        board_size[row][col] = select_size
        O_sizes[select_size - 1] -= 1

        if is_winner('O'):
            board[row][col] = prev_side
            board_size[row][col] = prev_size
            O_sizes[select_size - 1] += 1
            return (row, col, select_size)

        board[row][col] = prev_side
        board_size[row][col] = prev_size
        O_sizes[select_size - 1] += 1

    best_move = None
    best_eval = -sys.maxsize

    for p_choice in possible_choices:
        select_size = int(p_choice / 9 + 1)
        slot = p_choice % 9
        row = int(slot / 3)
        col = slot % 3

        prev_size = board_size[row][col]
        prev_side = board[row][col]

        board[row][col] = 'O'
        board_size[row][col] = select_size
        O_sizes[select_size - 1] -= 1
        eval = minimax(0, False)

        board[row][col] = prev_side
        board_size[row][col] = prev_size
        O_sizes[select_size - 1] += 1

        if eval > best_eval:
            best_eval = eval
            best_move = (row, col, select_size)
    return best_move

def play_game():
    print("----------------------------------------------------\n\n")
    print("Welcome to Big eat Small Tic-Tac-Toe!\n")
    print("The rules are simple:")
    print("- You can stack bigger pieces on top of opponent's smaller pieces.")
    print("- The first player to get 3 in a row wins!")
    print("- When the board is full, the player with the most pieces wins.")
    print("- If both players have the same number of pieces, it's a draw.\n")
    print("You have 3 small pieces and 3 big pieces.\n")
    print("To make a move, enter the row, column, and size of your piece.\n") 
    print("You are X, and the computer is O.")
    print("Let's start!\n\n")

    while not is_board_full('O', O_sizes) and not is_winner('X') and not is_winner('O'):
        print_board(board, board_size)
        try:
            player_input = input("\nEnter your move (row, column, size): ").split()
            if len(player_input) != 3:
                raise ValueError("Please enter exactly three numbers: row, column, and size.")

            player_row, player_col, size = map(int, player_input)

            if player_row not in range(3) or player_col not in range(3):
                raise ValueError("Row and column must be between 0 and 2.")

            if size not in [1, 2]:
                raise ValueError("Size must be either 1 or 2.")

            if X_sizes[size - 1] <= 0:
                raise ValueError(f"No more pieces of size {size} left for X.")

            isOwnMark = board[player_row][player_col] == "X"
            canPlace = board_size[player_row][player_col] < size

            if isOwnMark:
                raise ValueError("You cannot place a piece on your own mark.")
            if not canPlace:
                raise ValueError(f"Cannot place a piece of size {size} on this cell.")

            board[player_row][player_col] = 'X'
            board_size[player_row][player_col] = size
            X_sizes[size - 1] -= 1

        except ValueError as e:
            print(f"Invalid move: {e}")
            continue

        if is_winner('X'):
            print_board(board, board_size)
            print("\nYou win!")
            break

        if is_board_full('X', X_sizes):
            print_board(board, board_size)
            #print("\nIt's a draw!")
            isWin = check_draw_win('X')
            if isWin:
                print("You win!")
            else:
                print("Computer wins!")
            break

        print("\nComputer's turn...")

        computer_move = find_best_move()

        computer_row, computer_col, computer_size = find_best_move()
        board[computer_row][computer_col] = 'O'
        board_size[computer_row][computer_col] = computer_size
        O_sizes[computer_size - 1] -= 1

        if is_winner('O'):
            print_board(board, board_size)
            print("\nComputer wins!")
            break        

play_game()