
# Kart-Engine v2.3

from model.tile import Tile
from model.circuit import Circuit
from model.terrain import (
    RoadTerrain,
    GrassTerrain,
    DirtTerrain,
    IceTerrain,
    VoidTerrain
)
from model.block import (
    StartBlock,
    CheckpointBlock,
    FinishLineBlock
)


def _build_circuit(
    name: str,
    terrain_map: list[str],
    start_positions: list[tuple[int, int]],
    checkpoints: list[tuple[int, int]],
    finish_position: tuple[int, int]
) -> Circuit:
    """Construit un circuit à partir d'une carte de caractères."""

    terrain_types = {
        "R": RoadTerrain,
        "G": GrassTerrain,
        "D": DirtTerrain,
        "I": IceTerrain,
        "V": VoidTerrain
    }

    grid = []

    for row_index, line in enumerate(terrain_map):
        row = []

        for col_index, symbol in enumerate(line):
            terrain_class = terrain_types[symbol]
            terrain = terrain_class()

            row.append(
                Tile(
                    col=col_index,
                    row=row_index,
                    terrain=terrain
                )
            )

        grid.append(row)

    # Placement des blocs de départ
    for player_number, (col, row) in enumerate(start_positions):
        grid[row][col].block = StartBlock(player_number)

    # Placement des checkpoints
    for checkpoint_index, (col, row) in enumerate(checkpoints):
        grid[row][col].block = CheckpointBlock(checkpoint_index)

    # Placement de la ligne d'arrivée
    finish_col, finish_row = finish_position
    grid[finish_row][finish_col].block = FinishLineBlock()

    return Circuit(
        name=name,
        grid=grid,
        total_laps=3,
        checkpoint_count=len(checkpoints),
        start_positions=start_positions
    )


def create_circuit_one() -> Circuit:
    """Crée le premier circuit avec une route entourée d'herbe."""

    terrain_map = [
        "GGGGGGGGGGGG",
        "GGGGGGGGGGGG",
        "GGRRRRRRRRGG",
        "GGRGGGGGGRGG",
        "GGRGGGGGGRGG",
        "GGRGGGGGGRGG",
        "GGRGGGGGGRGG",
        "GGRRRRRRRRGG",
        "GGGGGGGGGGGG",
        "GGGGGGGGGGGG"
    ]

    return _build_circuit(
        name="Circuit 1",
        terrain_map=terrain_map,
        start_positions=[(4, 2), (5, 2)],
        checkpoints=[(9, 4), (5, 7)],
        finish_position=(2, 4)
    )


def create_circuit_two() -> Circuit:
    """Crée un deuxième circuit avec de la terre, de la glace et du vide."""

    terrain_map = [
        "GGGGGGGGGGGG",
        "GGVVGGGGVVGG",
        "GGRRRRRRRRGG",
        "GGRDDDDGGRGG",
        "GGRDIIIGGRGG",
        "GGRDIIIGGRGG",
        "GGRDDDDGGRGG",
        "GGRRRRRRRRGG",
        "GGVVGGGGVVGG",
        "GGGGGGGGGGGG"
    ]

    return _build_circuit(
        name="Circuit 2",
        terrain_map=terrain_map,
        start_positions=[(4, 2), (5, 2)],
        checkpoints=[(9, 4), (5, 7)],
        finish_position=(2, 4)
    )
