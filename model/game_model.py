
# Kart-Engine v2.3

from constants import GameState, CAR_COLORS
from model.car import Car
from model.circuit import Circuit
from model.circuit_data import create_circuit_one


class GameModel:
    """Gère les données principales du jeu."""

    def __init__(self):
        """Initialise le modèle du jeu."""
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        """Charge le premier circuit et place la voiture au départ."""
        self.circuit = create_circuit_one()
        self.spawn_car()

    def spawn_car(self) -> None:
        """Place la voiture au point de départ."""
        if self.circuit is not None and self.circuit.start_positions:
            col, row = self.circuit.start_positions[0]
        else:
            col, row = 7, 1

        self.car = Car(0, col, row, CAR_COLORS[0])

    def update(self) -> None:
        """Met à jour la voiture selon le terrain sur lequel elle roule."""
        if (
            self.state != GameState.RACING
            or self.circuit is None
            or self.car is None
        ):
            return

        # Récupérer la case sous la voiture
        tile = self.circuit.get_tile_at_pixel(
            self.car.x,
            self.car.y
        )

        # Si la voiture sort de la carte, arrêter sa vitesse
        if tile is None:
            self.car.vx = 0.0
            self.car.vy = 0.0
            return

        # Détecter le terrain
        if tile.terrain.is_void:
            return

        # Mettre à jour la voiture avec le terrain réel
        self.car.update(tile.terrain)
