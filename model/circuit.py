
# Kart-Engine v2.3

from model.tile import Tile
from constants import TILE_SIZE


class Circuit:
    """Représente le circuit composé d'une grille de cases."""

    def __init__(self, grid: list[list[Tile]]):
        """Initialise le circuit à partir d'une grille de cases."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> Tile | None:
        """Retourne la case aux coordonnées indiquées, ou None si elle est hors de la carte."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> Tile | None:
        """Retourne la case correspondant aux coordonnées en pixels."""
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        """Retourne la largeur du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Retourne la hauteur du circuit en pixels."""
        return self.rows * TILE_SIZE
