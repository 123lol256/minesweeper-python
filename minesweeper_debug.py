import random


class MinesweeperDebug:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
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

    def print_board_with_bombs(self):
        """Wyświetla planszę z widocznymi bombami"""
        print("\n   " + " ".join(f"{i:2}" for i in range(self.cols)))
        for r in range(self.rows):
            row = [f"{r:2} "]
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    cell = "*"  # Bomba
                elif self.board[r][c] == 0:
                    cell = " "  # Puste pole
                else:
                    cell = str(self.board[r][c])  # Liczba
                row.append(f"{cell:>2}")
            print(" ".join(row))
        print()

    def print_board_hidden(self):
        """Wyświetla planszę bez bomb"""
        print("\n   " + " ".join(f"{i:2}" for i in range(self.cols)))
        for r in range(self.rows):
            row = [f"{r:2} "]
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    cell = "."  # Ukryta bomba
                elif self.board[r][c] == 0:
                    cell = " "  # Puste pole
                else:
                    cell = str(self.board[r][c])  # Liczba
                row.append(f"{cell:>2}")
            print(" ".join(row))
        print()

    def get_bomb_locations(self):
        """Zwraca listę wszystkich pozycji bomb"""
        bombs = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    bombs.append((r, c))
        return bombs


def main():
    print("=== Minesweeper Debug - Ujawnianie Bomb ===\n")
    
    # Tworzenie gry
    game = MinesweeperDebug(9, 9, 10)
    
    # Wyświetlanie bomb
    print("PLANSZY Z BOMBAMI:")
    game.print_board_with_bombs()
    
    print("PLANSZY BEZ BOMB (normalna gra):")
    game.print_board_hidden()
    
    print("POZYCJE BOMB:")
    bombs = game.get_bomb_locations()
    for i, (r, c) in enumerate(bombs, 1):
        print(f"{i}. Bomba na pozycji: wiersz {r}, kolumna {c}")
    
    print(f"\nŁącznie bomb: {len(bombs)}")


if __name__ == "__main__":
    main()
