
# Kart-Engine v2.3

from constants import GameState, CAR_COLORS
from model.car import Car
from model.circuit import Circuit
from model.circuit_data import (
    create_circuit_one,
    create_circuit_two
)
from model.race_coordinator import RaceCoordinator
from model.block import BoostBlock


class GameModel:
    """Gère les données principales du jeu."""

    def __init__(self):
        self.state = GameState.MENU

        self.circuits = [
            create_circuit_one(),
            create_circuit_two()
        ]

        self.selected_circuit = 0
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
        self.coordinator: RaceCoordinator | None = None

    @property
    def car(self) -> Car | None:
        return self.cars[0] if self.cars else None

    def select_next_circuit(self) -> None:
        self.selected_circuit = (
            self.selected_circuit + 1
        ) % len(self.circuits)

    def select_previous_circuit(self) -> None:
        self.selected_circuit = (
            self.selected_circuit - 1
        ) % len(self.circuits)

    def start_race(self) -> None:
        self.circuit = self.circuits[self.selected_circuit]
        self.cars = []

        for player_index in range(2):
            col, row = self.circuit.start_positions[player_index]

            car = Car(
                player_index,
                col,
                row,
                CAR_COLORS[player_index]
            )

            self.cars.append(car)

        self.coordinator = RaceCoordinator(
            self.circuit, self.cars
        )

        self.state = GameState.RACING

    def load_circuit(self) -> None:
        self.start_race()

    def return_to_menu(self) -> None:
        self.state = GameState.MENU
        self.cars = []
        self.circuit = None
        self.coordinator = None

    def update(self) -> None:
        if self.state != GameState.RACING:
            return

        if self.circuit is None or self.coordinator is None:
            return

        for car in self.cars:

            # Terrain avant le déplacement
            old_tile = self.circuit.get_tile_at_pixel(
                car.x, car.y
            )

            if old_tile is None or old_tile.terrain.is_void:
                self.coordinator.respawn(car)
                continue

            # Mise à jour de la physique
            car.update(old_tile.terrain)

            # Terrain après le déplacement
            new_tile = self.circuit.get_tile_at_pixel(
                car.x, car.y
            )

            # Réapparition en cas de sortie du circuit
            if new_tile is None or new_tile.terrain.is_void:
                self.coordinator.respawn(car)
                continue

            # Déclenchement des blocs
            if new_tile.block is not None:
                if (
                    new_tile is not old_tile
                    or isinstance(new_tile.block, BoostBlock)
                ):
                    new_tile.block.on_car_enter(
                        car, self.coordinator
                    )

            # Vérification de la victoire
            if self.coordinator.is_finished():
                self.state = GameState.FINISHED
                return
