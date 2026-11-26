# Kart-Engine v2.3
from constants import GameState, GRID_ROWS, GRID_COLS, CAR_COLORS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.terrain import RoadTerrain, IceTerrain, GrassTerrain

class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx)
            for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        self.car = Car(0, 7, 1, CAR_COLORS[0])

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return

        old_x, old_y = self.car.x, self.car.y
        self.car.update(RoadTerrain())
        if self.circuit.get_tile_at_pixel(self.car.x, self.car.y) is None:
            self.car.x, self.car.y = old_x, old_y
            self.car.speed = 0.0
