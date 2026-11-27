# Kart-Engine v2.3
from __future__ import annotations
from typing import TYPE_CHECKING


import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_REVERSE_SPEED, AIR_FRICTION,
    CAR_MAX_STEERING, CAR_STEERING_STEP, CAR_STEERING_RETURN, CAR_TURN_FACTOR,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


if TYPE_CHECKING:
    from model.terrain import Terrain




class Car:
    """Voiture d'un joueur.

    L'angle est en degrés (0 = vers le haut de l'écran). La voiture avance
    dans la direction de son angle, à la vitesse `speed`.

    Attributs :
        player_index: numéro du joueur (0 ou 1).
        x, y: position du centre de la voiture, en pixels.
        vx, vy: vitesse en pixels par frame, sur les axes horizontal et vertical de l'écran.
        angle: orientation de la voiture, en degrés.
        steering_angle: angle de braquage, entre -CAR_MAX_STEERING et +CAR_MAX_STEERING.
        sprite: image de la voiture (non tournée).
        acceleration: accélération demandée par le joueur pour cette frame.
    """
    def __init__(self, player_index: int, start_col: int, start_row: int,
             color: tuple[int, int, int]):
        self.player_index = player_index
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.angle: float = 0.0
        self.steering_angle: float = 0.0
        self.sprite = self.build_sprite(color)
        self.acceleration: float = 0.0

    @property
    def speed(self) -> float:
        """Norme de la vitesse, en pixels par frame (toujours positive)."""
        return math.hypot(self.vx, self.vy)

    def accelerate(self) -> None:
        """Demande une accélération positive pour cette frame."""
        self.acceleration = CAR_ACCELERATION

    def brake(self) -> None:
        """Demande une accélération négative pour cette frame : freine, puis fait reculer."""
        self.acceleration = -CAR_BRAKE

    def reset_controls(self) -> None:
        """Remet l'accélération demandée à zéro.
        À appeler une fois par frame, avant de lire les touches.
        """
        self.acceleration = 0.0

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
        self.vx = 0.0
        self.vy = 0.0
        self.steering_angle = 0.0
        self.acceleration = 0.0

    def _axes(self) -> tuple[float, float, float, float]:
        """Renvoie les axes de la voiture dans le repère de l'écran.

            Returns:
            (fx, fy, rx, ry) : le vecteur unitaire vers l'avant de la voiture,
            puis le vecteur unitaire vers sa droite.
        """
        rad = math.radians(self.angle)
        return math.sin(rad), -math.cos(rad), math.cos(rad), math.sin(rad)

    def update(self, terrain: Terrain) -> None:
        """Met à jour la voiture pour une frame : braquage, traction, frottements, déplacement.

        Args:
            terrain: terrain sous la voiture ; sa traction réduit l'accélération.
        """
        # 1. Braquage : la voiture tourne d'autant plus vite qu'elle roule vite
        #    (en marche arrière la vitesse avant est négative : le virage s'inverse)
        forward_x, forward_y, _, _ = self._axes()
        v_forward = self.vx * forward_x + self.vy * forward_y
        self.angle -= self.steering_angle * v_forward * CAR_TURN_FACTOR

        # Le volant revient doucement au centre
        if abs(self.steering_angle) <= CAR_STEERING_RETURN:
            self.steering_angle = 0.0
        elif self.steering_angle > 0:
            self.steering_angle -= CAR_STEERING_RETURN
        else:
            self.steering_angle += CAR_STEERING_RETURN

        # 2. Décomposition de la vitesse selon les axes de la voiture (après rotation)
        forward_x, forward_y, right_x, right_y = self._axes()
        v_forward = self.vx * forward_x + self.vy * forward_y
        v_lateral = self.vx * right_x + self.vy * right_y

        # 3. Accélération, réduite par la traction du terrain
        v_forward += self.acceleration * terrain.traction
        v_forward = max(v_forward, -CAR_MAX_REVERSE_SPEED)

        # 4. Adhérence : pour l'instant les roues annulent toute vitesse latérale
        #    (le dérapage sera ajouté ici à l'étape suivante)
        v_lateral = 0.0

        # 5. Frottements de l'air
        v_forward *= 1.0 - AIR_FRICTION
        if abs(v_forward) < 0.01:
            v_forward = 0.0

        # 6. Retour dans le repère de l'écran, puis déplacement
        self.vx = v_forward * forward_x + v_lateral * right_x
        self.vy = v_forward * forward_y + v_lateral * right_y
        self.x += self.vx
        self.y += self.vy


    def build_sprite(self, color: tuple[int, int, int]) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, CAR_WIDTH, CAR_HEIGHT),
                     border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
