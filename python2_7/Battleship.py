from random import randint

board = []

for x in range(5):
    board.append(["O"] * 5)


def print_board(board):
    for row in board:
        print " ".join(row)
    print ""


print_board(board)


def random_row(board):
    return randint(0, len(board) - 1)


def random_col(board):
    return randint(1, len(board[0]) - 1)


ship_row = random_row(board)
ship_col = random_col(board)
print ship_row
print ship_col

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
for turn in range(4):
    guess_row = int(raw_input("Guess Row: "))
    guess_col = int(raw_input("Guess Col: "))

    if (guess_row - 1) == ship_row and (guess_col - 1) == ship_col:
        print "Congratulations! You sunk my battleship!"
        break

    else:
        if (guess_row < 1 or guess_row > 5) or (guess_col < 1 or guess_col > 5):
            print "Oops, that's not even in the ocean."

        elif board[(guess_row - 1)][(guess_col - 1)] == "X":
            print "You guessed that one already."

        else:
            print "You missed my battleship!"
            board[(guess_row - 1)][(guess_col - 1)] = "X"

        if turn >= 3:
            print "Game Over"

    print "Turn", turn + 1

    print_board(board)
