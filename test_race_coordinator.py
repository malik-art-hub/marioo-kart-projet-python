from model.race_coordinator import RaceCoordinator
from model.car import Car


# Circuit temporaire pour les tests
class TestCircuit:
    total_laps = 2
    checkpoint_count = 3


circuit = TestCircuit()

car1 = Car(0, 2, 3, (255, 0, 0))
car2 = Car(1, 3, 3, (0, 0, 255))

race = RaceCoordinator(circuit, [car1, car2])


# Test 1 : Initialisation
assert race.laps == [0, 0]
assert race.winner is None
print("Test 1 OK : Initialisation")


# Test 2 : Checkpoint en double
race.register_checkpoint(car1, 1)
race.register_checkpoint(car1, 1)

assert len(race.checkpoints_passed[0]) == 1
print("Test 2 OK : Checkpoint en double")


# Test 3 : Tour incomplet
race.register_finish_line(car1)

assert race.laps[0] == 0
print("Test 3 OK : Tour incomplet refuse")


# Test 4 : Tour complet
race.register_checkpoint(car1, 2)
race.register_checkpoint(car1, 3)
race.register_finish_line(car1)

assert race.laps[0] == 1
assert len(race.checkpoints_passed[0]) == 0
assert race.laps[1] == 0
print("Test 4 OK : Tour valide")


# Test 5 : Reapparition
car1.x = 200
car1.y = 300
race.register_checkpoint(car1, 1)

car1.x = 900
car1.y = 900
car1.vx = 10.0

race.respawn(car1)

assert car1.x == 200
assert car1.y == 300
assert car1.speed == 0
print("Test 5 OK : Reapparition")


# Test 6 : Victoire
race.register_checkpoint(car1, 2)
race.register_checkpoint(car1, 3)
race.register_finish_line(car1)

assert race.winner == 0
assert race.is_finished()
print("Test 6 OK : Victoire")

print("\nTous les tests sont passes !")