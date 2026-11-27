
# Kart-Engine v2.3

import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, FPS,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT,
    COLOR_PANEL, COLOR_PANEL_BORDER,
    CAR_COLORS, GameState
)

from model.game_model import GameModel
from model.block import (
    StartBlock,
    CheckpointBlock,
    FinishLineBlock,
    BoostBlock
)


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 54, bold=True)
        self.hud_font = pygame.font.SysFont("Arial", 16, bold=True)
        self.speed_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 12)

        self.race_start_time = None

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)

        if model.state == GameState.MENU:
            self.race_start_time = None
            self._draw_menu(model)

        elif model.state == GameState.RACING:
            self._draw_racing(model)

        elif model.state == GameState.FINISHED:
            self._draw_finished(model)

        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT
        )

        self.screen.blit(
            title, title.get_rect(center=(cx, 160))
        )

        options = ["JOUER (Enter)", "QUITTER (Escape)"]

        for i, label in enumerate(options):
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

            text = self.font.render(
                label, True,
                COLOR_ACCENT if i == 0 else COLOR_TEXT
            )

            self.screen.blit(
                text, text.get_rect(center=rect.center)
            )

    def _draw_tile(self, tile, surface) -> None:

        rect = pygame.Rect(
            tile.col * TILE_SIZE,
            tile.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        pygame.draw.rect(
            surface, tile.terrain.color, rect
        )

        # Contours discrets de la grille
        pygame.draw.rect(
            surface, (45, 65, 45), rect, 1
        )

        block = tile.block

        if isinstance(block, CheckpointBlock):

            pygame.draw.rect(
                surface, (255, 200, 0), rect, 3
            )

            text = self.hud_font.render(
                f"CP{block.checkpoint_index + 1}",
                True, COLOR_TEXT
            )

            surface.blit(
                text, text.get_rect(center=rect.center)
            )

        elif isinstance(block, FinishLineBlock):

            size = TILE_SIZE // 8

            for row in range(4):
                for col in range(8):

                    color = (
                        (240, 240, 240)
                        if (row + col) % 2 == 0
                        else (20, 20, 20)
                    )

                    pygame.draw.rect(
                        surface, color,
                        (
                            rect.x + col * size,
                            rect.y + TILE_SIZE // 4 + row * size,
                            size, size
                        )
                    )

        elif isinstance(block, StartBlock):

            pygame.draw.rect(
                surface,
                CAR_COLORS[block.player_number],
                rect, 3
            )

        elif isinstance(block, BoostBlock):

            pygame.draw.polygon(
                surface, (255, 200, 0),
                [
                    (rect.centerx, rect.y + 8),
                    (rect.right - 8, rect.centery),
                    (rect.centerx, rect.bottom - 8),
                    (rect.x + 8, rect.centery)
                ]
            )

    def _draw_racing(self, model: GameModel) -> None:

        if model.circuit is None or not model.cars:
            return

        if self.race_start_time is None:
            self.race_start_time = pygame.time.get_ticks()

        # Dimensions reelles du circuit
        circuit_width = model.circuit.pixel_width()
        circuit_height = model.circuit.pixel_height()

        world = pygame.Surface(
            (circuit_width, circuit_height)
        )

        # Dessiner le circuit
        for row in model.circuit.grid:
            for tile in row:
                self._draw_tile(tile, world)

        # Conserver la carte sans les voitures
        map_surface = world.copy()

        # Dessiner les voitures
        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            world.blit(surf, rect)

        # Agrandir le rendu sans modifier la physique
        scale = min(
            WINDOW_WIDTH / circuit_width,
            WINDOW_HEIGHT / circuit_height
        )

        render_width = int(circuit_width * scale)
        render_height = int(circuit_height * scale)

        scaled_world = pygame.transform.smoothscale(
            world, (render_width, render_height)
        )

        # Fond de la couleur du terrain exterieur
        self.screen.fill(
            model.circuit.grid[0][0].terrain.color
        )

        # Centrer le circuit
        x = (WINDOW_WIDTH - render_width) // 2
        y = (WINDOW_HEIGHT - render_height) // 2

        self.screen.blit(scaled_world, (x, y))

        # HUD individuel des deux joueurs
        for car in model.cars:
            self._draw_hud(model, car)
            self._draw_speed_panel(car)

        self._draw_minimap(model, map_surface)

    def _draw_hud(self, model: GameModel, car) -> None:

        elapsed = (
            pygame.time.get_ticks() - self.race_start_time
        ) / 1000

        player = car.player_index
        race = model.coordinator

        if race is not None:

            lap = min(
                race.laps[player] + 1,
                race.total_laps
            )

            lap_text = f"{lap} / {race.total_laps}"

        else:
            lap_text = "-- / --"

        stats = [
            ("LAP", lap_text),
            ("DRIFT", "ON" if car.is_drifting else "OFF"),
            ("TIME", f"{elapsed:.2f} s")
        ]

        panel = pygame.Surface(
            (210, 116), pygame.SRCALPHA
        )

        color = CAR_COLORS[player]

        # Bandeau du joueur
        pygame.draw.polygon(
            panel, (15, 18, 20, 225),
            [(12, 0), (210, 0), (210, 26), (0, 26)]
        )

        pygame.draw.polygon(
            panel, color,
            [(12, 0), (46, 0), (34, 26), (0, 26)]
        )

        # Bandes decoratives
        for i in range(3):
            x = 15 + i * 8

            pygame.draw.line(
                panel, (240, 240, 240),
                (x, 2), (x - 9, 24), 4
            )

        name = self.hud_font.render(
            f"JOUEUR {player + 1}", True, COLOR_TEXT
        )

        panel.blit(name, (54, 4))

        pygame.draw.line(
            panel, color,
            (35, 25), (210, 25), 2
        )

        # Statistiques
        for i, (label, value) in enumerate(stats):

            y = 30 + i * 28

            pygame.draw.polygon(
                panel, (15, 18, 20, 195),
                [
                    (12, y),
                    (210, y),
                    (210, y + 24),
                    (0, y + 24)
                ]
            )

            label_surf = self.hud_font.render(
                label, True, (190, 195, 200)
            )

            value_color = (
                COLOR_ACCENT
                if label == "DRIFT" and car.is_drifting
                else COLOR_TEXT
            )

            value_surf = self.hud_font.render(
                value, True, value_color
            )

            panel.blit(label_surf, (20, y + 2))

            panel.blit(
                value_surf,
                (198 - value_surf.get_width(), y + 2)
            )

        # Joueur 1 a gauche, joueur 2 a droite
        x = (
            10 if player == 0
            else WINDOW_WIDTH - 220
        )

        self.screen.blit(panel, (x, 10))

    def _draw_speed_panel(self, car) -> None:

        # Conversion arcade en km/h
        meters_per_pixel = 4 / TILE_SIZE

        speed_kmh = int(
            car.speed * FPS * meters_per_pixel * 3.6
        )

        panel = pygame.Surface(
            (190, 68), pygame.SRCALPHA
        )

        color = CAR_COLORS[car.player_index]

        pygame.draw.polygon(
            panel, (15, 18, 20, 210),
            [(18, 0), (190, 0), (172, 68), (0, 68)]
        )

        speed_text = self.speed_font.render(
            f"{speed_kmh:03d}", True, COLOR_TEXT
        )

        panel.blit(speed_text, (20, 5))

        unit_text = self.small_font.render(
            "KM/H", True, COLOR_TEXT
        )

        panel.blit(unit_text, (100, 24))

        # Barre de vitesse
        active_bars = min(18, speed_kmh // 5)

        for i in range(18):

            x = 17 + i * 9

            bar_color = (
                color
                if i < active_bars
                else (65, 75, 80)
            )

            pygame.draw.polygon(
                panel, bar_color,
                [
                    (x, 44),
                    (x + 6, 44),
                    (x + 1, 58),
                    (x - 5, 58)
                ]
            )

        x = (
            10 if car.player_index == 0
            else WINDOW_WIDTH - 200
        )

        self.screen.blit(
            panel, (x, WINDOW_HEIGHT - 78)
        )

    def _draw_minimap(
        self, model: GameModel,
        map_surface: pygame.Surface
    ) -> None:

        map_width = 140

        map_height = int(
            map_width * map_surface.get_height()
            / map_surface.get_width()
        )

        panel = pygame.Surface(
            (map_width + 8, map_height + 8),
            pygame.SRCALPHA
        )

        panel.fill((15, 18, 20, 195))

        mini_map = pygame.transform.smoothscale(
            map_surface, (map_width, map_height)
        )

        panel.blit(mini_map, (4, 4))

        scale_x = map_width / map_surface.get_width()
        scale_y = map_height / map_surface.get_height()

        for car in model.cars:

            car_x = int(car.x * scale_x) + 4
            car_y = int(car.y * scale_y) + 4

            pygame.draw.circle(
                panel, COLOR_TEXT, (car_x, car_y), 5
            )

            pygame.draw.circle(
                panel, CAR_COLORS[car.player_index],
                (car_x, car_y), 3
            )

        # Mini-carte centree en bas
        x = (WINDOW_WIDTH - panel.get_width()) // 2
        y = WINDOW_HEIGHT - panel.get_height() - 10

        self.screen.blit(panel, (x, y))

    def _draw_finished(self, model: GameModel) -> None:

        if model.coordinator is None:
            return

        winner = model.coordinator.winner

        if winner is None:
            return

        cx = WINDOW_WIDTH // 2

        title = self.title_font.render(
            "VICTOIRE !", True, COLOR_ACCENT
        )

        self.screen.blit(
            title, title.get_rect(center=(cx, 230))
        )

        text = self.font.render(
            f"Le joueur {winner + 1} remporte la course",
            True, CAR_COLORS[winner]
        )

        self.screen.blit(
            text, text.get_rect(center=(cx, 340))
        )

        instruction = self.font.render(
            "Entree ou Echap : retour au menu",
            True, COLOR_TEXT
        )

        self.screen.blit(
            instruction,
            instruction.get_rect(center=(cx, 480))
        )
