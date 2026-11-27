
# Kart-Engine v2.3

from abc import ABC, abstractmethod


class Terrain(ABC):
    """[TERRA-7] Classe abstraite représentant un terrain du circuit."""

    def __init__(
        self,
        name: str,
        color: tuple[int, int, int],
        traction: float,
        grip: float,
        drift_friction: float
    ):
        self.name = name
        self.color = color
        self.traction = traction
        self.grip = grip
        self.drift_friction = drift_friction

    @abstractmethod
    def on_car_enter(self, car, coordinator) -> None:
        """Déclenche l'action associée à l'entrée d'une voiture sur le terrain."""
        pass

    @property
    @abstractmethod
    def is_void(self) -> bool:
        pass


class RoadTerrain(Terrain):
    """[TERRA-7] Terrain de route avec une forte adhérence."""

    def __init__(self):
        super().__init__(
            name="Road",
            color=(100, 100, 110),
            traction=1.0,
            grip=0.25,
            drift_friction=0.15
        )

    def on_car_enter(self, car, coordinator) -> None:
        pass

    @property
    def is_void(self) -> bool:
        return False


class GrassTerrain(Terrain):
    """[TERRA-7] Terrain d'herbe avec une adhérence moyenne."""

    def __init__(self):
        super().__init__(
            name="Grass",
            color=(54, 150, 65),
            traction=0.6,
            grip=0.10,
            drift_friction=0.10
        )

    def on_car_enter(self, car, coordinator) -> None:
        pass

    @property
    def is_void(self) -> bool:
        return False


class DirtTerrain(Terrain):
    """[TERRA-7] Terrain de terre avec une faible adhérence."""

    def __init__(self):
        super().__init__(
            name="Dirt",
            color=(150, 95, 55),
            traction=0.5,
            grip=0.05,
            drift_friction=0.06
        )

    def on_car_enter(self, car, coordinator) -> None:
        pass

    @property
    def is_void(self) -> bool:
        return False


class IceTerrain(Terrain):
    """[TERRA-7] Terrain de glace avec une adhérence très faible."""

    def __init__(self):
        super().__init__(
            name="Ice",
            color=(130, 210, 230),
            traction=0.3,
            grip=0.01,
            drift_friction=0.005
        )

    def on_car_enter(self, car, coordinator) -> None:
        pass

    @property
    def is_void(self) -> bool:
        return False


class VoidTerrain(Terrain):
    """[TERRA-7] Terrain vide qui provoque le retour au dernier checkpoint."""

    def __init__(self):
        super().__init__(
            name="Void",
            color=(35, 35, 45),
            traction=0.0,
            grip=0.0,
            drift_friction=0.0
        )

    def on_car_enter(self, car, coordinator) -> None:
        coordinator.respawn(car)

    @property
    def is_void(self) -> bool:
        return True
