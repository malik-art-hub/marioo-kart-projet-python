import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_SPEED, CAR_TURN_SPEED, CAR_MAX_REVERSE_SPEED,
    CAR_WIDTH, CAR_FRICTION, CAR_HEIGHT, TILE_SIZE
)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
    ### Augmente la vitesse de la voiture, sans dépasser la vitesse max.
        self.speed = min(self.speed + CAR_ACCELERATION, CAR_MAX_SPEED)

    def brake(self) -> None:
    ###Diminue la vitesse : freine, puis fait reculer la voiture.
        self.speed = max(self.speed - CAR_BRAKE, CAR_MAX_REVERSE_SPEED)

    def turn_left(self) -> None:
    ##Tourne la voiture vers la gauche."""
        self.angle -= CAR_TURN_SPEED

    def turn_right(self) -> None:
    ##Tourne la voiture vers la droite."""
        self.angle += CAR_TURN_SPEED

    def update_position(self) -> None:
    ###Déplace la voiture dans la direction de son angle."""
        self.speed *= CAR_FRICTION
        if abs(self.speed) < 0.01:
            self.speed = 0.0
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
