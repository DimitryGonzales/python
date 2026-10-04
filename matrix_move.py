import subprocess
import sys


def clear():
    command = ["cmd", "/c", "cls"] if sys.platform == "win32" else ["clear"]
    subprocess.run(command, check=True)


def get_char(message):
    print(message)

    if sys.platform == "win32":
        import msvcrt

        return msvcrt.getwch()

    import termios
    import tty

    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)

    try:
        tty.setcbreak(file_descriptor)

        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(
            file_descriptor,
            termios.TCSADRAIN,
            old_settings,
        )


def create_matrix(height, width, fill_character):
    matrix = []

    for _ in range(height):
        row = []

        for _ in range(width):
            row.append(fill_character)

        matrix.append(row)

    return matrix


def update_position(matrix, fill_character, row, column, direction):
    up_icon = "↑"
    left_icon = "←"
    down_icon = "↓"
    right_icon = "→"

    if direction == "w":
        matrix[row][column] = fill_character

        if row == 0:
            row = len(matrix) - 1
        else:
            row -= 1

        matrix[row][column] = up_icon

        return matrix, row, column
    elif direction == "a":
        matrix[row][column] = fill_character

        if column == 0:
            column = len(matrix[row]) - 1
        else:
            column -= 1

        matrix[row][column] = left_icon

        return matrix, row, column
    elif direction == "s":
        matrix[row][column] = fill_character

        if row == len(matrix) - 1:
            row = 0
        else:
            row += 1

        matrix[row][column] = down_icon

        return matrix, row, column
    elif direction == "d":
        matrix[row][column] = fill_character

        if column == len(matrix[0]) - 1:
            column = 0
        else:
            column += 1

        matrix[row][column] = right_icon

        return matrix, row, column

    return matrix, row, column


def format_matrix(matrix):
    matrix_formatted = ""

    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            matrix_formatted += f"{matrix[row][column]}"

            if column < len(matrix[row]) - 1:
                matrix_formatted += " "

        if row < len(matrix) - 1:
            matrix_formatted += "\n"

    return matrix_formatted


if __name__ == "__main__":
    matrix_height, matrix_width = 10, 10
    matrix_fill_character = "·"

    matrix = create_matrix(matrix_height, matrix_width, matrix_fill_character)
    matrix[0][0] = "↘"

    direction = ""

    row = 0
    column = 0

    while direction != "q":
        clear()
        print(format_matrix(matrix))

        direction = get_char(
            "\nMove('q' to quit):\n'w' = up\n'a' = left\n's' = down\n'd' = right"
        ).lower()

        matrix, row, column = update_position(
            matrix, matrix_fill_character, row, column, direction
        )

        if direction == "q":
            clear()
            print(
                f"Final position:\nRow = {row + 1}\nColumn = {column + 1}\n\n{format_matrix(matrix)}"
            )
