# Kart-Engine v2.3

import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_REVERSE_SPEED, AIR_FRICTION,
    CAR_MAX_STEERING, CAR_STEERING_STEP, CAR_STEERING_RETURN, CAR_TURN_FACTOR,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """Voiture d'un joueur.

    L'angle est en degrés (0 = vers le haut de l'écran). La voiture avance
    dans la direction de son angle, à la vitesse `speed`.

    Attributs :
        player_index: numéro du joueur (0 ou 1).
        x, y: position du centre de la voiture, en pixels.
        speed: vitesse en pixels par frame (négative en marche arrière).
        angle: orientation de la voiture, en degrés.
        steering_angle: angle de braquage, entre -CAR_MAX_STEERING et +CAR_MAX_STEERING.
        sprite: image de la voiture (non tournée).
    """
    def __init__(self, player_index: int, start_col: int, start_row: int,
             color: tuple[int, int, int]):
        self.player_index = player_index
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.steering_angle: float = 0.0
        self.sprite = self.build_sprite(color)

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

    def reset_to(self, x: float, y: float) -> None:
        """Téléporte la voiture en (x, y) avec une vitesse nulle."""
        self.x = x
        self.y = y
        self.speed = 0.0
        self.steering_angle = 0.0

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

    def build_sprite(self, color: tuple[int, int, int]) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, CAR_WIDTH, CAR_HEIGHT),
                     border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
