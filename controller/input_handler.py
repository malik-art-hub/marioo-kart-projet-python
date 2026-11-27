# Kart-Engine v2.3

import pygame


MAPPING_P1 = {
    pygame.K_z: "accelerate",
    pygame.K_s: "brake",
    pygame.K_q: "left",
    pygame.K_d: "right",
}

MAPPING_P2 = {
    pygame.K_UP: "accelerate",
    pygame.K_DOWN: "brake",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}


class InputHandler:

    def __init__(self):
        self.mappings = [MAPPING_P1, MAPPING_P2]

    def get_inputs(self, player_index: int = 0) -> dict:
        keys = pygame.key.get_pressed()
        mapping = self.mappings[player_index]

        p = {action: False for action in mapping.values()}

        for key, action in mapping.items():
            if keys[key]:
                p[action] = True

        return p