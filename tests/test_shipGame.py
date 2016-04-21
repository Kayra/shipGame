import pytest
from shipGame.shipGame import ShipGame


@pytest.fixture
def testGame():
    testGame = ShipGame("tests/input.txt")
    return testGame


def test_incomplete_input_file():
    with pytest.raises(SystemExit):
        testGame = ShipGame("tests/incompleteInput.txt")


def test_initialiseBoard_size_of_zero(testGame):
    with pytest.raises(ValueError):
        testGame.initialiseBoard(0)


def test_initialiseBoard_size_of_float(testGame):
    with pytest.raises(ValueError):
        testGame.initialiseBoard(1.5)


def test_initialiseBoard_size_of_ten(testGame):
    assert testGame.initialiseBoard(10) == {(7, 3): 0, (6, 9): 0, (1, 3): 0, (4, 8): 0, (3, 0): 0, (2, 8): 0, (9, 8): 0, (8, 0): 0, (0, 7): 0, (6, 2): 0, (1, 6): 0, (3, 7): 0, (2, 5): 0, (8, 5): 0, (5, 8): 0, (4, 0): 0, (9, 0): 0, (6, 7): 0, (5, 5): 0, (7, 6): 0, (5, 0): 0, (0, 4): 0, (3, 5): 0, (1, 1): 0, (3, 2): 0, (2, 6): 0, (8, 2): 0, (4, 5): 0, (9, 3): 0, (6, 0): 0, (1, 4): 0, (7, 5): 0, (2, 3): 0, (1, 9): 0, (8, 7): 0, (4, 2): 0, (9, 6): 0, (6, 5): 0, (5, 3): 0, (0, 1): 0, (7, 0): 0, (6, 8): 0, (3, 1): 0, (9, 9): 0, (0, 6): 0, (1, 7): 0, (0, 9): 0, (7, 8): 0, (2, 4): 0, (8, 4): 0, (5, 9): 0, (4, 7): 0, (9, 1): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (2, 1): 0, (8, 9): 0, (9, 4): 0, (5, 1): 0, (0, 3): 0, (7, 2): 0, (1, 2): 0, (3, 8): 0, (4, 9): 0, (3, 3): 0, (2, 9): 0, (8, 1): 0, (4, 4): 0, (6, 3): 0, (1, 5): 0, (8, 8): 0, (3, 6): 0, (2, 2): 0, (8, 6): 0, (4, 1): 0, (9, 7): 0, (6, 4): 0, (5, 4): 0, (0, 0): 0, (7, 1): 0, (0, 5): 0, (1, 0): 0, (0, 8): 0, (7, 9): 0, (2, 7): 0, (8, 3): 0, (4, 6): 0, (9, 2): 0, (3, 4): 0, (6, 1): 0, (5, 7): 0, (7, 4): 0, (2, 0): 0, (1, 8): 0, (3, 9): 0, (4, 3): 0, (9, 5): 0, (5, 2): 0, (0, 2): 0}


def test_initialiseShipLocations_no_input(testGame):
    pass


def test_initialiseShipLocations_invalid_input(testGame):
    pass


def test_initialiseShipLocations_valid_input(testGame):
    pass


def test_moveShip_no_input(testGame):
    pass


def test_moveShip_invalid_input(testGame):
    pass


def test_moveShip_valid_input(testGame):
    pass


def test_moveShip_north_turn_left(testGame):
    pass


def test_moveShip_west_turn_right(testGame):
    pass


def test_moveShip_to_occupied_cell(testGame):
    pass


def test_shootShip_no_input(testGame):
    pass


def test_shootShip_invalid_input(testGame):
    pass


def test_shootShip_occupied_cell(testGame):
    pass


def test_shootShip_empty_cell(testGame):
    pass


def test_parseInputFile_no_input(testGame):
    pass


def test_parseInputFile_invalid_input(testGame):
    pass


def test_parseInputFile_valid_input(testGame):
    pass


def test_assignOperations_no_input(testGame):
    pass


def test_assignOperations_invalid_input(testGame):
    pass


def test_assignOperations_valid_input(testGame):
    pass


def test_assignOperaations_heavy_input(testGame):
    pass


def test_writeOutput_no_occupied_cells(testGame):
    pass


def test_writeOutput_no_sunken_ships(testGame):
    pass


def test_calculateGame_no_input(testGame):
    pass


def test_calculateGame_valid_input(testGame):
    pass


if __name__ == '__main__':
    pytest.main()
