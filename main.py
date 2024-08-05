import random
from blessed import Terminal

term = Terminal()


def clear():
    # Use blessed to clear the screen
    print(term.clear(), end="")


clear()
print("")


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False


def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def generate_complete_board():
    board = [[0] * 9 for _ in range(9)]
    fill_grid(board)
    return board


def fill_grid(board):
    numbers = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if not find_empty_location(board) or fill_grid(board):
                            return True
                        board[i][j] = 0
                return False


def remove_numbers(board, holes=40):
    while holes > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            removed = board[row][col]
            board[row][col] = 0
            copy_board = [row[:] for row in board]
            if not has_unique_solution(copy_board):
                board[row][col] = removed
            else:
                holes -= 1
    return board


def has_unique_solution(board):
    solutions = [0]

    def count_solutions(b):
        empty = find_empty_location(b)
        if not empty:
            solutions[0] += 1
            return
        row, col = empty

        for num in range(1, 10):
            if is_valid(b, row, col, num):
                b[row][col] = num
                count_solutions(b)
                b[row][col] = 0
            if solutions[0] > 1:
                return

    count_solutions(board)
    return solutions[0] == 1


def generate_sudoku(difficulty="medium"):
    board = generate_complete_board()
    if difficulty == "easy":
        holes = 30
    elif difficulty == "medium":
        holes = 40
    else:
        holes = 50
    puzzle = remove_numbers(board, holes)
    return puzzle


def print_sudoku(board):
    def print_horizontal_border():
        print("┣━━━━━━━━━━╋━━━━━━━━━━╋━━━━━━━━━━┫")

    def print_top_border():
        print("┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓")

    def print_bottom_border():
        print("┗━━━━━━━━━━┻━━━━━━━━━━┻━━━━━━━━━━┛   ")

    for i in range(9):
        if i == 0:
            print_top_border()
        elif i % 3 == 0:
            print_horizontal_border()
        for j in range(9):
            if j % 3 == 0:
                print("┃ ", end="")
            if board[i][j] == 0:
                print("  ", end=" ")
            else:
                print(f"{board[i][j]} ", end=" ")
        print("┃")
    print_bottom_border()


def enter_sudoku():
    board = []
    print("Enter your Sudoku puzzle, row by row (use 0 for empty cells):")
    for i in range(9):
        while True:
            row = input(f"Row {i+1}: ")
            if len(row) == 9 and row.isdigit():
                board.append([int(num) for num in row])
                break
            else:
                print("Invalid input. Please enter exactly 9 digits (0-9).")
    return board


def main_menu():
    puzzle = None
    while True:
        print("\nSudoku Menu:")
        print("1. Generate a Sudoku puzzle")
        print("2. Solve the current Sudoku puzzle")
        print("3. Print the current Sudoku puzzle")
        print("4. Enter your own Sudoku puzzle")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            difficulty = input("Enter difficulty (easy, medium, hard): ").lower()
            clear()
            puzzle = generate_sudoku(difficulty)
            print_sudoku(puzzle)
        elif choice == "2":
            if puzzle is None:
                clear()
                print("No puzzle to solve. Generate or enter a puzzle first.")
            else:
                if solve_sudoku(puzzle):
                    clear()
                    print_sudoku(puzzle)
                else:
                    clear()
                    print("No solution exists for the Sudoku puzzle.")
        elif choice == "3":
            if puzzle is None:
                clear()
                print("No puzzle to print. Generate or enter a puzzle first.")
            else:
                clear()
                print_sudoku(puzzle)
        elif choice == "4":
            clear()
            puzzle = enter_sudoku()
            clear()
            print_sudoku(puzzle)
        elif choice == "5":
            break
        else:
            if puzzle is None:
                clear()
                print("No puzzle to print. Generate or enter a puzzle first.")
            else:
                clear()
                print_sudoku(puzzle)


if __name__ == "__main__":
    main_menu()
