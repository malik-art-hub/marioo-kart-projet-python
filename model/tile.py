
# Kart-Engine v2.3

from model.terrain import Terrain
from model.block import Block


class Tile:
    """Représente une case individuelle du circuit."""

    def __init__(
        self,
        col: int,
        row: int,
        terrain: Terrain,
        block: Block | None = None
    ):
        """Initialise une case avec ses coordonnées, son terrain et son bloc."""
        self.col = col
        self.row = row
        self.terrain = terrain
        self.block = block
