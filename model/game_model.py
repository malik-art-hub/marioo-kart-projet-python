
# Kart-Engine v2.3

from constants import GameState, GRID_ROWS, GRID_COLS, CAR_COLORS
from model.car import Car
from model.circuit import Circuit
from model.tile import Tile
from model.terrain import RoadTerrain


class GameModel:
    """Gère les données principales du jeu."""

    def __init__(self):
        """Initialise le modèle du jeu."""
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        """Crée une première grille composée uniquement de route."""
        grid = [
            [
                Tile(
                    col=col_idx,
                    row=row_idx,
                    terrain=RoadTerrain()
                )
                for col_idx in range(GRID_COLS)
            ]
            for row_idx in range(GRID_ROWS)
        ]

        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        """Place la voiture au point de départ."""
        self.car = Car(0, 7, 1, CAR_COLORS[0])

    def update(self) -> None:
        """Met à jour la voiture pendant la course."""
        if self.state != GameState.RACING or self.circuit is None:
            return

        old_x, old_y = self.car.x, self.car.y
        self.car.update(RoadTerrain())

        if self.circuit.get_tile_at_pixel(self.car.x, self.car.y) is None:
            self.car.x, self.car.y = old_x, old_y
            self.car.vx = 0.0
            self.car.vy = 0.0
