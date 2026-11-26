# Kart-Engine v2.3

import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, FPS,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL,
    COLOR_PANEL_BORDER, GameState
)
from model.game_model import GameModel


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

        self.hud_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.speed_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14)
        self.race_start_time = None

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)

        if model.state != GameState.RACING:
            self.race_start_time = None

        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)

        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT
        )

        self.screen.blit(
            title_surf,
            title_surf.get_rect(center=(cx, 160))
        )

        options = [
            ("JOUER (Enter)", GameState.RACING),
            ("QUITTER (Escape)", None)
        ]

        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)

            pygame.draw.rect(
                self.screen, COLOR_PANEL, rect,
                border_radius=8
            )

            pygame.draw.rect(
                self.screen, COLOR_PANEL_BORDER, rect,
                2, border_radius=8
            )

            text_surf = self.font.render(
                label, True,
                COLOR_ACCENT if i == 0 else COLOR_TEXT
            )

            self.screen.blit(
                text_surf,
                text_surf.get_rect(center=rect.center)
            )

    def _draw_racing(self, model: GameModel) -> None:
        if model.circuit is None or model.car is None:
            return

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)

                self.screen.blit(
                    sprite,
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                )

        map_surface = self.screen.copy()

        surf, rect = model.car.get_rotated_sprite()
        self.screen.blit(surf, rect)

        self._draw_hud(model)
        self._draw_minimap(model, map_surface)

    def _draw_hud(self, model: GameModel) -> None:
        if self.race_start_time is None:
            self.race_start_time = pygame.time.get_ticks()

        elapsed = (
            pygame.time.get_ticks() - self.race_start_time
        ) / 1000

        player = model.car.player_index

        race = getattr(model, "race_coordinator", None)

        if race is not None:
            lap = min(race.laps[player] + 1, race.total_laps)
            lap_text = f"{lap} / {race.total_laps}"
        else:
            lap_text = "-- / --"

        stats = [
            ("LAP", lap_text),
            ("DRIFT", "--"),
            ("TIME", f"{elapsed:.2f} s")
        ]

        panel = pygame.Surface((250, 140), pygame.SRCALPHA)

        # Bandeau du joueur
        pygame.draw.polygon(
            panel, (15, 18, 20, 220),
            [(15, 0), (250, 0), (250, 32), (0, 32)]
        )

        pygame.draw.polygon(
            panel, (230, 200, 70),
            [(15, 0), (55, 0), (40, 32), (0, 32)]
        )

        # Bandes decoratives
        for i in range(3):
            x = 19 + i * 10

            pygame.draw.line(
                panel, (255, 245, 180),
                (x, 3), (x - 11, 29), 5
            )

        name = self.hud_font.render(
            f"JOUEUR {player + 1}", True, COLOR_TEXT
        )

        panel.blit(name, (65, 5))

        pygame.draw.line(
            panel, (220, 60, 60),
            (42, 30), (250, 30), 2
        )

        # Statistiques
        for i, (label, value) in enumerate(stats):
            y = 36 + i * 32

            pygame.draw.polygon(
                panel, (15, 18, 20, 185),
                [
                    (15, y),
                    (250, y),
                    (250, y + 28),
                    (0, y + 28)
                ]
            )

            label_surf = self.hud_font.render(
                label, True, (190, 195, 200)
            )

            value_surf = self.hud_font.render(
                value, True, COLOR_TEXT
            )

            panel.blit(label_surf, (25, y + 3))

            panel.blit(
                value_surf,
                (235 - value_surf.get_width(), y + 3)
            )

        self.screen.blit(panel, (WINDOW_WIDTH - 260, 10))

        self._draw_speed_panel(model)

    def _draw_speed_panel(self, model: GameModel) -> None:
        # Conversion de la vitesse en km/h
        meters_per_pixel = 4 / TILE_SIZE
        speed = abs(model.car.speed) * FPS
        speed_kmh = int(speed * meters_per_pixel * 3.6)

        panel = pygame.Surface((250, 95), pygame.SRCALPHA)

        # Fond incline et transparent
        pygame.draw.polygon(
            panel, (15, 18, 20, 200),
            [(25, 0), (250, 0), (225, 95), (0, 95)]
        )

        speed_text = self.speed_font.render(
            f"{speed_kmh:03d}", True, COLOR_TEXT
        )

        panel.blit(speed_text, (25, 5))

        unit_text = self.small_font.render(
            "KM/H", True, COLOR_TEXT
        )

        panel.blit(unit_text, (120, 30))

        # Barre de vitesse
        active_bars = min(20, int(speed_kmh / 10))

        for i in range(20):
            x = 20 + i * 10

            if i >= active_bars:
                color = (65, 75, 80)
            elif i < 14:
                color = (40, 190, 230)
            elif i < 17:
                color = (255, 200, 0)
            else:
                color = (230, 60, 50)

            pygame.draw.polygon(
                panel, color,
                [
                    (x, 60),
                    (x + 7, 60),
                    (x + 1, 78),
                    (x - 6, 78)
                ]
            )

        self.screen.blit(
            panel, (10, WINDOW_HEIGHT - 105)
        )

    def _draw_minimap(
        self,
        model: GameModel,
        map_surface: pygame.Surface
    ) -> None:

        map_width = 180
        map_height = 135

        panel = pygame.Surface(
            (map_width + 12, map_height + 12),
            pygame.SRCALPHA
        )

        panel.fill((15, 18, 20, 180))

        # Redimensionnement du circuit
        mini_map = pygame.transform.smoothscale(
            map_surface, (map_width, map_height)
        )

        panel.blit(mini_map, (6, 6))

        # Position de la voiture sur la mini-carte
        scale_x = map_width / WINDOW_WIDTH
        scale_y = map_height / WINDOW_HEIGHT

        car_x = int(model.car.x * scale_x) + 6
        car_y = int(model.car.y * scale_y) + 6

        pygame.draw.circle(
            panel, (255, 255, 255), (car_x, car_y), 5
        )

        pygame.draw.circle(
            panel, (230, 50, 50), (car_x, car_y), 3
        )

        self.screen.blit(
            panel, (WINDOW_WIDTH - map_width - 22, 165)
        )