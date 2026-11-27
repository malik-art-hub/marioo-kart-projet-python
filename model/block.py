# Kart-Engine v2.3

from abc import ABC, abstractmethod


class Block(ABC):
    """Classe abstraite représentant un bloc placé sur une case du circuit."""

    @abstractmethod
    def on_car_enter(self, car, coordinator) -> None:
        """Définit l'action déclenchée lorsqu'une voiture entre sur le bloc."""
        pass


class StartBlock(Block):
    """Bloc indiquant une position de départ."""

    def __init__(self, player_number: int):
        """Initialise le bloc avec le numéro du joueur."""
        self.player_number = player_number

    def on_car_enter(self, car, coordinator) -> None:
        """Ne déclenche aucune action pendant la course."""
        pass


class CheckpointBlock(Block):
    """Bloc représentant un point de passage du circuit."""

    def __init__(self, checkpoint_index: int):
        """Initialise le bloc avec l'identifiant du checkpoint."""
        self.checkpoint_index = checkpoint_index

    def on_car_enter(self, car, coordinator) -> None:
        """Enregistre le passage de la voiture sur ce checkpoint."""
        coordinator.register_checkpoint(car, self.checkpoint_index)


class FinishLineBlock(Block):
    """Bloc représentant la ligne d'arrivée."""

    def on_car_enter(self, car, coordinator) -> None:
        """Signale le passage de la voiture sur la ligne d'arrivée."""
        coordinator.register_finish_line(car)


class BoostBlock(Block):
    """Bloc qui augmente la vitesse de la voiture."""

    def __init__(self, boost_amount: float = 5.0):
        """Initialise le bloc avec la puissance du boost."""
        self.boost_amount = boost_amount

    def on_car_enter(self, car, coordinator) -> None:
        """Applique un boost à la voiture."""
        car.apply_boost(self.boost_amount)