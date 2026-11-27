
# Kart-Engine v2.3

import pygame

from constants import TILE_SIZE
from model.circuit_data import create_circuit_one, create_circuit_two


def draw_circuit(screen, circuit, offset_x):
    """Dessine un circuit à partir des terrains et des blocs."""

    for row in circuit.grid:
        for tile in row:
            rect = pygame.Rect(
                offset_x + tile.col * TILE_SIZE,
                tile.row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            # Dessiner le terrain
            pygame.draw.rect(screen, tile.terrain.color, rect)

            # Contour des cases
            pygame.draw.rect(screen, (30, 30, 30), rect, 1)

            # Dessiner les blocs
            if tile.block is not None:
                if tile.block.__class__.__name__ == "StartBlock":
                    color = (50, 100, 255)
                elif tile.block.__class__.__name__ == "CheckpointBlock":
                    color = (255, 220, 0)
                elif tile.block.__class__.__name__ == "FinishLineBlock":
                    color = (255, 255, 255)
                else:
                    color = (255, 0, 255)

                pygame.draw.circle(
                    screen,
                    color,
                    rect.center,
                    TILE_SIZE // 5
                )


def main():
    """Affiche les deux circuits côte à côte."""

    pygame.init()

    circuit_one = create_circuit_one()
    circuit_two = create_circuit_two()

    # Dimensions de la fenêtre
    width = circuit_one.pixel_width() + circuit_two.pixel_width()
    height = max(
        circuit_one.pixel_height(),
        circuit_two.pixel_height()
    ) + 50

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Kart-Engine - Comparaison des circuits")

    font = pygame.font.SysFont(None, 28)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((25, 25, 25))

        # Titres
        title_one = font.render("Circuit 1", True, (255, 255, 255))
        title_two = font.render("Circuit 2", True, (255, 255, 255))

        screen.blit(title_one, (10, 10))
        screen.blit(
            title_two,
            (circuit_one.pixel_width() + 10, 10)
        )

        # Afficher les deux circuits
        draw_circuit(screen, circuit_one, 0)
        draw_circuit(
            screen,
            circuit_two,
            circuit_one.pixel_width()
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
