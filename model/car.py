# Kart-Engine v2.3

import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_REVERSE_SPEED, AIR_FRICTION,
    CAR_MAX_STEERING, CAR_STEERING_STEP, CAR_STEERING_RETURN, CAR_TURN_FACTOR,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()
        self.steering_angle: float = 0.0

    def accelerate(self) -> None:
        """Augmente la vitesse de la voiture."""
        self.speed += CAR_ACCELERATION

    def brake(self) -> None:
        """Diminue la vitesse : freine, puis fait reculer la voiture."""
        self.speed = max(self.speed - CAR_BRAKE, -CAR_MAX_REVERSE_SPEED)

    def turn_left(self) -> None:
        """Augmente l'angle de braquage (virage à gauche)."""
        self.steering_angle = min(
            self.steering_angle + CAR_STEERING_STEP, CAR_MAX_STEERING)

    def turn_right(self) -> None:
        """Diminue l'angle de braquage (virage à droite)."""
        self.steering_angle = max(
            self.steering_angle - CAR_STEERING_STEP, -CAR_MAX_STEERING)

    def update_position(self) -> None:
        """Déplace la voiture dans la direction de son angle, avec frottements."""
    # Frottements de l'air
        self.speed *= 1.0 - AIR_FRICTION
        if abs(self.speed) < 0.01:
            self.speed = 0.0

    # Le braquage fait tourner la voiture, d'autant plus vite qu'elle roule vite
    # (en marche arrière la vitesse est négative : le virage s'inverse)
        self.angle -= self.steering_angle * self.speed * CAR_TURN_FACTOR

    # Le volant revient doucement au centre
        if abs(self.steering_angle) <= CAR_STEERING_RETURN:
            self.steering_angle = 0.0
        elif self.steering_angle > 0:
            self.steering_angle -= CAR_STEERING_RETURN
        else:
            self.steering_angle += CAR_STEERING_RETURN

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
