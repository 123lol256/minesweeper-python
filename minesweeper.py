import random
import sys


class Minesweeper:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
        self._plant_mines()
        self._calculate_numbers()

    def _plant_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        random.shuffle(positions)
        for r, c in positions[: self.mines]:
            self.board[r][c] = -1

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = 0
                for rr in range(max(0, r - 1), min(self.rows, r + 2)):
                    for cc in range(max(0, c - 1), min(self.cols, c + 2)):
                        if self.board[rr][cc] == -1:
                            count += 1
                self.board[r][c] = count

    def _in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def _neighbors(self, r, c):
        for rr in range(max(0, r - 1), min(self.rows, r + 2)):
            for cc in range(max(0, c - 1), min(self.cols, c + 2)):
                if (rr, cc) != (r, c):
                    yield rr, cc

    def reveal(self, r, c):
        if not self._in_bounds(r, c):
            return False
        if self.flags[r][c] or self.visible[r][c]:
            return False
        if self.board[r][c] == -1:
            self.visible[r][c] = True
            self.game_over = True
            return True

        stack = [(r, c)]
        while stack:
            rr, cc = stack.pop()
            if not self._in_bounds(rr, cc) or self.visible[rr][cc] or self.flags[rr][cc]:
                continue
            self.visible[rr][cc] = True
            if self.board[rr][cc] == 0:
                for nr, nc in self._neighbors(rr, cc):
                    if not self.visible[nr][nc] and not self.flags[nr][nc]:
                        if self.board[nr][nc] == 0:
                            stack.append((nr, nc))
                        else:
                            self.visible[nr][nc] = True

        self._check_win()
        return True

    def toggle_flag(self, r, c):
        if not self._in_bounds(r, c) or self.visible[r][c]:
            return False
        self.flags[r][c] = not self.flags[r][c]
        return True

    def _check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.visible[r][c]:
                    return
        self.won = True
        self.game_over = True

    def print_board(self, reveal_all=False):
        print("\n   " + " ".join(f"{i:2}" for i in range(self.cols)))
        for r in range(self.rows):
            row = [f"{r:2} "]
            for c in range(self.cols):
                if reveal_all:
                    cell = self._cell_to_char(self.board[r][c], reveal=True)
                elif self.visible[r][c]:
                    cell = self._cell_to_char(self.board[r][c], reveal=True)
                elif self.flags[r][c]:
                    cell = "F"
                else:
                    cell = "."
                row.append(f"{cell:>2}")
            print(" ".join(row))
        print()

    @staticmethod
    def _cell_to_char(value, reveal=False):
        if value == -1:
            return "*" if reveal else "*"
        if value == 0:
            return " " if reveal else "."
        return str(value)

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.visible[r][c] = True


def input_move():
    while True:
        cmd = input("Wpisz pole: (np. 'r 2 3' / 'f 2 3' / 'q'): ").strip().lower()
        if not cmd:
            print("Puste pole. Spróbuj ponownie.")
            continue
        parts = cmd.split()
        if parts[0] == "q":
            return "q", None, None
        if len(parts) != 3:
            print("Zły format. Użyj: 'r 2 3' albo 'f 2 3'")
            continue
        action, row, col = parts
        if action not in {"r", "f"}:
            print("Działanie musi być 'r' (odkryj) lub 'f' (flaga).")
            continue
        try:
            row = int(row)
            col = int(col)
        except ValueError:
            print("Współrzędne muszą być liczbami.")
            continue
        return action, row, col


def main():
    print("=== Minesweeper ===")
    print("Sterowanie: 'r row col' - odkryj pole, 'f row col' - postaw/usuń flagę, 'q' - wyjście")
    rows = 9
    cols = 9
    mines = 10

    game = Minesweeper(rows, cols, mines)
    game.print_board()

    while not game.game_over:
        action, row, col = input_move()
        if action == "q":
            print("Wyjście z gry.")
            return

        if not game._in_bounds(row, col):
            print("Pole poza planszą. Spróbuj jeszcze raz.")
            continue

        if action == "f":
            game.toggle_flag(row, col)
        else:
            if game.flags[row][col]:
                print("To pole jest oznaczone flagą. Najpierw usuń flagę.")
                continue
            game.reveal(row, col)

        game.print_board()

        if game.won:
            print("Gratulacje! Wygrałeś!")
            break

        if game.game_over:
            game.reveal_all_mines()
            game.print_board(reveal_all=True)
            print("Przegrana! Trafiłeś na minę.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGra przerwana przez użytkownika.")
        sys.exit(0)
