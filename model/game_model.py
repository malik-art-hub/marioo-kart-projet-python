# Kart-Engine v2.3
from time import monotonic
from constants import GameState, CAR_COLORS
from model.car import Car
from model.circuit import Circuit
from model.circuit_data import create_circuit_one, create_circuit_two
from model.race_coordinator import RaceCoordinator
from model.block import BoostBlock


class GameModel:
    """Données du jeu, navigation et chronométrage."""
    def __init__(self):
        self.state = GameState.MENU
        self.circuits = [create_circuit_one(), create_circuit_two()]
        self.selected_circuit = 0
        self.player_count = 2
        self.menu_index = 0
        self.result_index = 0
        self.show_controls = False
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []
        self.coordinator: RaceCoordinator | None = None
        self.started_at = None
        self.finished_at = None
        self.lap_started_at = []
        self.lap_times = []

    @property
    def car(self):
        return self.cars[0] if self.cars else None

    @property
    def elapsed(self):
        if self.started_at is None:
            return 0.0
        end = self.finished_at if self.finished_at is not None else monotonic()
        return end - self.started_at

    def select_next_circuit(self):
        self.selected_circuit = (self.selected_circuit + 1) % len(self.circuits)

    def select_previous_circuit(self):
        self.selected_circuit = (self.selected_circuit - 1) % len(self.circuits)

    def start_race(self):
        """Initialise les voitures et remet les chronomètres à zéro."""
        self.circuit = self.circuits[self.selected_circuit]
        self.cars = []
        for player_index in range(self.player_count):
            col, row = self.circuit.start_positions[player_index]
            self.cars.append(Car(player_index, col, row, CAR_COLORS[player_index]))
        self.coordinator = RaceCoordinator(self.circuit, self.cars)
        self.started_at = monotonic()
        self.finished_at = None
        self.lap_started_at = [self.started_at for _ in self.cars]
        self.lap_times = [[] for _ in self.cars]
        self.result_index = 0
        self.state = GameState.RACING

    def load_circuit(self):
        self.start_race()

    def return_to_menu(self):
        self.state = GameState.MENU
        self.show_controls = False
        self.cars = []
        self.circuit = None
        self.coordinator = None
        self.started_at = None
        self.finished_at = None

    def update(self):
        if self.state != GameState.RACING or self.circuit is None or self.coordinator is None:
            return
        for car in self.cars:
            player = car.player_index
            previous_laps = self.coordinator.laps[player]
            old_tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            if old_tile is None or old_tile.terrain.is_void:
                self.coordinator.respawn(car)
                continue
            car.update(old_tile.terrain)
            new_tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            if new_tile is None or new_tile.terrain.is_void:
                self.coordinator.respawn(car)
                continue
            if new_tile.block is not None:
                if new_tile is not old_tile or isinstance(new_tile.block, BoostBlock):
                    new_tile.block.on_car_enter(car, self.coordinator)
            now = monotonic()
            if self.coordinator.laps[player] > previous_laps:
                self.lap_times[player].append(now - self.lap_started_at[player])
                self.lap_started_at[player] = now
            if self.coordinator.is_finished():
                self.finished_at = now
                self.state = GameState.FINISHED
                return
