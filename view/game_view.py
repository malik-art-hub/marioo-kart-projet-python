
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
        if model.state == GameState.RACING:
            self._draw_racing(model)
        else:
            self.race_start_time = None
            canvas = pygame.Surface((640, 480))
            if model.state == GameState.MENU:
                if model.show_controls:
                    self._draw_controls(canvas)
                else:
                    self._draw_menu(canvas, model)
            elif model.state == GameState.CIRCUIT_SELECT:
                self._draw_circuit_select(canvas, model)
            elif model.state == GameState.FINISHED:
                self._draw_finished(canvas, model)
            self.screen.blit(pygame.transform.smoothscale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.flip()

    def _text(self, canvas, text, x, y, size=16, color=(244, 206, 135), bold=False, italic=False, center=False):
        key = (size, bold, italic)
        if not hasattr(self, "menu_fonts"):
            self.menu_fonts = {}
        if key not in self.menu_fonts:
            self.menu_fonts[key] = pygame.font.SysFont("Arial", size, bold=bold, italic=italic)
        image = self.menu_fonts[key].render(text, True, color)
        rect = image.get_rect(midtop=(x, y)) if center else image.get_rect(topleft=(x, y))
        canvas.blit(image, rect)

    def _footer(self, canvas, text):
        self._text(canvas, text, 320, 433, 12, center=True)
        for i in range(32):
            for j in range(2):
                color = (228, 217, 190) if (i+j)%2 == 0 else (23, 27, 44)
                pygame.draw.rect(canvas, color, (i*20, 450+j*15, 20, 15))

    def _sunset(self, canvas, road=False, muted=False):
        sky = (23, 27, 44)
        canvas.fill(sky)
        pygame.draw.circle(canvas, (83, 65, 60) if muted else (232, 173, 99), (470, 170), 128)
        for i in range(9):
            pygame.draw.rect(canvas, sky, (335, 164+i*15, 270, int(2+i*.9)))
        pygame.draw.polygon(canvas, (55,62,83), [(0,200),(100,104),(210,213),(322,125),(460,228),(560,151),(640,230),(640,480),(0,480)])
        pygame.draw.polygon(canvas, (34,42,58), [(0,270),(100,205),(220,275),(360,202),(520,270),(640,212),(640,480),(0,480)])
        if road:
            pygame.draw.polygon(canvas, (81,81,93), [(453,238),(475,238),(640,480),(160,480)])
            for y in range(245, 480, 29):
                x = 464 - (y-245)*14/235
                pygame.draw.line(canvas, (241,216,160), (int(x),y), (int(x-1),y+14), 5)
            pygame.draw.polygon(canvas, (201,71,66), [(443,319),(454,319),(454,307),(524,307),(524,319),(537,319),(537,362),(443,362)])
            pygame.draw.rect(canvas, (175,206,215), (461,314,58,19), border_radius=2)
            pygame.draw.rect(canvas, (27,27,36), (439,352,102,10), border_radius=3)
            for x in (451,511):
                pygame.draw.rect(canvas, (255,240,174), (x,342,18,8), border_radius=2)

    def _draw_menu(self, canvas, model):
        self._sunset(canvas, road=True)
        self._text(canvas, "THE RACING EXPERIENCE", 32, 53, 11, bold=True)
        self._text(canvas, "REDLINE", 28, 73, 55, bold=True, italic=True)
        self._text(canvas, "RACING CLUB", 33, 135, 26, (239,110,88), True, True)
        items = [("TIME ATTACK", "Contre-la-montre - 1 joueur"), ("VERSUS", "Course locale - 2 joueurs"), ("COMMANDES", "Apprendre a piloter"), ("QUITTER", "")]
        for i, (title, subtitle) in enumerate(items):
            y = 210+i*53
            selected = i == model.menu_index
            pygame.draw.rect(canvas, (244,206,135) if selected else (23,27,44), (32,y,250,46))
            pygame.draw.rect(canvas, (244,206,135) if selected else (105,91,80), (32,y,250,46), 2)
            color = (23,27,44) if selected else (234,226,206)
            if selected:
                pygame.draw.polygon(canvas, color, [(44,y+15),(52,y+23),(44,y+31)])
            self._text(canvas,title,64,y+(4 if subtitle else 12),18,color,True,True)
            if subtitle:
                self._text(canvas,subtitle,65,y+25,11,(99,80,53) if selected else (169,166,180))
        self._footer(canvas, "Fleches : naviguer     |     Entree : valider")

    def _draw_controls(self, canvas):
        self._sunset(canvas, muted=True)
        self._text(canvas, "REDLINE RACING CLUB",32,28,12,bold=True)
        self._text(canvas, "COMMANDES",320,75,44,bold=True,italic=True,center=True)
        for x, title, lines, color in [(35,"JOUEUR 1",["Z : accelerer", "S : freiner", "Q / D : tourner"],(239,110,88)),(335,"JOUEUR 2",["Haut : accelerer", "Bas : freiner", "Gauche / droite : tourner"],(139,197,255))]:
            pygame.draw.rect(canvas,(23,27,44),(x,155,270,180))
            pygame.draw.rect(canvas,color,(x,155,270,180),2)
            self._text(canvas,title,x+18,170,23,color,True,True)
            for i,line in enumerate(lines):
                self._text(canvas,line,x+18,215+i*32,16,(234,226,206))
        self._text(canvas,"F11 : plein ecran   |   Echap : retour",320,370,14,center=True)
        self._footer(canvas,"Entree ou Echap : retour")

    def _draw_circuit_select(self, canvas, model):
        self._sunset(canvas, muted=True)
        self._text(canvas,"REDLINE RACING CLUB",32,24,12,bold=True)
        self._text(canvas,"SELECT TRACK",29,48,43,bold=True,italic=True)
        self._text(canvas,"TIME ATTACK" if model.player_count == 1 else "VERSUS",33,105,14,(239,154,135),True)
        # Deux cartes visibles, avec navigation circulaire si d'autres circuits sont ajoutes.
        count = len(model.circuits)
        first = (model.selected_circuit//2)*2
        for slot, index in enumerate(range(first,min(first+2,count))):
            circuit = model.circuits[index]
            x = 30+slot*300
            y = 139
            selected = index == model.selected_circuit
            pygame.draw.rect(canvas,(23,27,44),(x,y,280,267))
            pygame.draw.rect(canvas,(244,206,135) if selected else (100,91,90),(x,y,280,267),3 if selected else 1)
            world = pygame.Surface((circuit.pixel_width(),circuit.pixel_height()))
            for row in circuit.grid:
                for tile in row:
                    self._draw_tile(tile,world)
            scale = min(256/world.get_width(),184/world.get_height())
            size = (max(1,int(world.get_width()*scale)),max(1,int(world.get_height()*scale)))
            preview = pygame.transform.smoothscale(world,size)
            pygame.draw.rect(canvas,(17,21,36),(x+12,y+12,256,184))
            canvas.blit(preview,preview.get_rect(center=(x+140,y+104)))
            pygame.draw.rect(canvas,(244,206,135) if selected else (48,54,74),(x+2,y+207,276,31))
            self._text(canvas,circuit.name.upper(),x+14,y+210,20,(23,27,44) if selected else (238,224,201),True,True)
            self._text(canvas,f"{circuit.total_laps} TOURS  |  {circuit.checkpoint_count} CHECKPOINTS",x+14,y+246,12,(192,186,198))
        self._footer(canvas,"Gauche / droite : choisir   |   Entree : jouer   |   Echap : retour")

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

        elapsed = model.elapsed

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

    @staticmethod
    def _format_time(seconds):
        if seconds is None:
            return "--:--.---"
        ms = int(seconds*1000)
        return f"{ms//60000:02d}:{ms//1000%60:02d}.{ms%1000:03d}"

    def _draw_finished(self, canvas, model):
        # Composition podium distincte du decor du menu.
        canvas.fill((23,27,44))
        winner = model.coordinator.winner if model.coordinator else None
        if winner is None:
            return
        solo = model.player_count == 1
        color = (239,110,88) if winner == 0 else (139,197,255)
        for i in range(8):
            x = i*105-260
            pygame.draw.polygon(canvas,(34,42,58),[(x,0),(x+35,0),(x+260,450),(x+225,450)])
        pygame.draw.polygon(canvas,(55,62,83),[(0,80),(640,80),(600,140),(0,140)])
        self._text(canvas,"REDLINE RACING CLUB",320,25,12,bold=True,center=True)
        self._text(canvas,"TIME ATTACK" if solo else "RACE WINNER",320,58,48,bold=True,italic=True,center=True)
        self._text(canvas,"COURSE TERMINEE" if solo else "VICTOIRE",320,113,15,(234,226,206),True,center=True)
        # Voiture stylisee et podium.
        x,y=320,191
        pygame.draw.ellipse(canvas,(12,16,25),(x-65,y+52,130,18))
        for sx in (-1,1):
            for sy in (-1,1):
                pygame.draw.rect(canvas,(12,16,25),(x+sx*30-8,y+sy*31-13,16,26),border_radius=4)
        pygame.draw.rect(canvas,(201,71,66) if winner==0 else (50,131,220),(x-27,y-53,54,106),border_radius=12)
        pygame.draw.polygon(canvas,(175,206,215),[(x-18,y-32),(x+18,y-32),(x+22,y-10),(x-22,y-10)])
        pygame.draw.rect(canvas,(234,226,206),(x-4,y-53,8,106))
        self._text(canvas,str(winner+1),x,y-2,23,(255,255,255),True,center=True)
        self._text(canvas,"RESULTATS" if solo else f"JOUEUR {winner+1}",320,255,28,color,True,True,True)
        pygame.draw.rect(canvas,(23,27,44),(115,301,410,67))
        pygame.draw.rect(canvas,(150,127,100),(115,301,410,67),1)
        pygame.draw.line(canvas,(105,100,116),(320,311),(320,358))
        laps = model.lap_times[winner]
        for px,label,value in [(140,"TEMPS TOTAL",model.elapsed),(344,"MEILLEUR TOUR",min(laps) if laps else None)]:
            self._text(canvas,label,px,308,11,(188,181,195))
            self._text(canvas,self._format_time(value),px,327,26,bold=True,italic=True)
        for i,label in enumerate(("REJOUER","MENU PRINCIPAL")):
            x = 115+i*213
            selected = model.result_index == i
            pygame.draw.rect(canvas,(244,206,135) if selected else (23,27,44),(x,384,197,38))
            pygame.draw.rect(canvas,(244,206,135),(x,384,197,38),1)
            self._text(canvas,label,x+98,393,16,(23,27,44) if selected else (234,226,206),True,True,True)
        self._footer(canvas,"Gauche / droite : choisir   |   Entree : valider   |   Echap : menu")
