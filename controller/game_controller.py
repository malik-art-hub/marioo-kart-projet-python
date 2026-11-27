
# Kart-Engine v2.3

import pygame
import sys

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)

from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.SCALED | pygame.FULLSCREEN
        )

        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:

        if key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
            return

        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        elif state == GameState.RACING:

            if key == pygame.K_ESCAPE:
                self.model.return_to_menu()

        elif state == GameState.FINISHED:

            if key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.model.return_to_menu()

    def handle_menu_key(self, key: int) -> None:

        if key == pygame.K_RETURN:
            self.model.start_race()

        elif key == pygame.K_ESCAPE:
            self.quit()

    def update(self) -> None:

        if self.model.state != GameState.RACING:
            return

        for car in self.model.cars:

            car.reset_controls()

            player_input = self.input_handler.get_inputs(
                car.player_index
            )

            self.apply_input(car, player_input)

        self.model.update()

    def apply_input(self, car, player_input) -> None:

        if player_input["accelerate"]:
            car.accelerate()

        if player_input["brake"]:
            car.brake()

        if player_input["left"]:
            car.turn_left()

        if player_input["right"]:
            car.turn_right()

    def render(self) -> None:
        self.view.draw(self.model)

    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
