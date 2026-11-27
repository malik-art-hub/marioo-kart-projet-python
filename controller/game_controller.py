# Kart-Engine v2.3
import pygame
import sys
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GameState
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key):
        if key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
            return
        state = self.model.state
        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECT:
            if key in (pygame.K_LEFT, pygame.K_UP):
                self.model.select_previous_circuit()
            elif key in (pygame.K_RIGHT, pygame.K_DOWN):
                self.model.select_next_circuit()
            elif key == pygame.K_RETURN:
                self.model.start_race()
            elif key == pygame.K_ESCAPE:
                self.model.return_to_menu()
        elif state == GameState.RACING:
            if key == pygame.K_ESCAPE:
                self.model.return_to_menu()
        elif state == GameState.FINISHED:
            if key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                self.model.result_index = 1 - self.model.result_index
            elif key == pygame.K_RETURN:
                if self.model.result_index == 0:
                    self.model.start_race()
                else:
                    self.model.return_to_menu()
            elif key == pygame.K_ESCAPE:
                self.model.return_to_menu()

    def handle_menu_key(self, key):
        if self.model.show_controls:
            if key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.model.show_controls = False
            return
        if key == pygame.K_UP:
            self.model.menu_index = (self.model.menu_index - 1) % 4
        elif key == pygame.K_DOWN:
            self.model.menu_index = (self.model.menu_index + 1) % 4
        elif key == pygame.K_RETURN:
            index = self.model.menu_index
            if index in (0, 1):
                self.model.player_count = index + 1
                self.model.state = GameState.CIRCUIT_SELECT
            elif index == 2:
                self.model.show_controls = True
            else:
                self.quit()
        elif key == pygame.K_ESCAPE:
            self.quit()

    def update(self):
        if self.model.state != GameState.RACING:
            return
        for car in self.model.cars:
            car.reset_controls()
            self.apply_input(car, self.input_handler.get_inputs(car.player_index))
        self.model.update()

    def apply_input(self, car, player_input):
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        if player_input['left']:
            car.turn_left()
        if player_input['right']:
            car.turn_right()

    def render(self):
        self.view.draw(self.model)

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()
