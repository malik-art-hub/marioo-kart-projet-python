# Kart-Engine v2.3


class RaceCoordinator:
    """Gère la progression des joueurs et les règles de la course."""

    def __init__(self, circuit, cars):
        """Initialise les données de la course pour chaque joueur."""
        self.total_laps = circuit.total_laps
        self.checkpoint_count = circuit.checkpoint_count

        self.laps = [0 for car in cars]
        self.checkpoints_passed = [set() for car in cars]

        self.last_checkpoint_pos = [
            (car.x, car.y) for car in cars
        ]

        self.winner = None

    def register_checkpoint(self, car, checkpoint_index: int) -> None:
        """Enregistre un point de passage franchi par un joueur."""
        player = car.player_index

        self.checkpoints_passed[player].add(checkpoint_index)
        self.last_checkpoint_pos[player] = (car.x, car.y)

    def register_finish_line(self, car) -> None:
        """Valide un tour et détermine éventuellement le vainqueur."""
        player = car.player_index

        if len(self.checkpoints_passed[player]) == self.checkpoint_count:
            self.laps[player] += 1
            self.checkpoints_passed[player].clear()

            if self.laps[player] >= self.total_laps and self.winner is None:
                self.winner = player

    def respawn(self, car) -> None:
        """Replace la voiture à son dernier point de passage."""
        player = car.player_index
        car.reset_to(*self.last_checkpoint_pos[player])

    def is_finished(self) -> bool:
        """Indique si un joueur a remporté la course."""
        return self.winner is not None