import pytest
from shipGame.shipGame import ShipGame


@pytest.fixture
def testGame():
    testGame = ShipGame("tests/inputs/input.txt")
    return testGame


def test_incomplete_input_file():
    with pytest.raises(SystemExit):
        testGame = ShipGame("tests/inputs/incompleteInput.txt")


def test_initialiseBoard_size_of_zero(testGame):
    with pytest.raises(ValueError):
        testGame.initialiseBoard(0)


def test_initialiseBoard_size_of_float(testGame):
    with pytest.raises(ValueError):
        testGame.initialiseBoard(1.5)


def test_initialiseBoard_size_of_ten(testGame):
    assert testGame.initialiseBoard(10) == {(7, 3): 0, (6, 9): 0, (1, 3): 0, (4, 8): 0, (3, 0): 0, (2, 8): 0, (9, 8): 0, (8, 0): 0, (0, 7): 0, (6, 2): 0, (1, 6): 0, (3, 7): 0, (2, 5): 0, (8, 5): 0, (5, 8): 0, (4, 0): 0, (9, 0): 0, (6, 7): 0, (5, 5): 0, (7, 6): 0, (5, 0): 0, (0, 4): 0, (3, 5): 0, (1, 1): 0, (3, 2): 0, (2, 6): 0, (8, 2): 0, (4, 5): 0, (9, 3): 0, (6, 0): 0, (1, 4): 0, (7, 5): 0, (2, 3): 0, (1, 9): 0, (8, 7): 0, (4, 2): 0, (9, 6): 0, (6, 5): 0, (5, 3): 0, (0, 1): 0, (7, 0): 0, (6, 8): 0, (3, 1): 0, (9, 9): 0, (0, 6): 0, (1, 7): 0, (0, 9): 0, (7, 8): 0, (2, 4): 0, (8, 4): 0, (5, 9): 0, (4, 7): 0, (9, 1): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (2, 1): 0, (8, 9): 0, (9, 4): 0, (5, 1): 0, (0, 3): 0, (7, 2): 0, (1, 2): 0, (3, 8): 0, (4, 9): 0, (3, 3): 0, (2, 9): 0, (8, 1): 0, (4, 4): 0, (6, 3): 0, (1, 5): 0, (8, 8): 0, (3, 6): 0, (2, 2): 0, (8, 6): 0, (4, 1): 0, (9, 7): 0, (6, 4): 0, (5, 4): 0, (0, 0): 0, (7, 1): 0, (0, 5): 0, (1, 0): 0, (0, 8): 0, (7, 9): 0, (2, 7): 0, (8, 3): 0, (4, 6): 0, (9, 2): 0, (3, 4): 0, (6, 1): 0, (5, 7): 0, (7, 4): 0, (2, 0): 0, (1, 8): 0, (3, 9): 0, (4, 3): 0, (9, 5): 0, (5, 2): 0, (0, 2): 0}


def test_initialiseShipLocations_no_input(testGame):
    with pytest.raises(TypeError):
        testGame.initialiseShipLocations()


def test_initialiseShipLocations_invalid_input(testGame):
    with pytest.raises(IndexError):
        testGame.initialiseShipLocations('invalid')

    with pytest.raises(TypeError):
        testGame.initialiseShipLocations((0, 0))
        testGame.initialiseShipLocations([(0, 0)])
        testGame.initialiseShipLocations([(0, 0), (0, 1)])

    with pytest.raises(KeyError):
        testGame.initialiseShipLocations([((0, 11), 'N'), ((0, 1), 'E')])

    testGame.initialiseShipLocations([((0, 9), 'T'), ((0, 1), 3)])
    assert testGame.board.get((0, 9)) == 0
    assert testGame.board.get((0, 1)) == 0


def test_initialiseShipLocations_valid_input(testGame):
    testGame.initialiseShipLocations([((0, 9), 'N'), ((2, 1), 'E'), ((0, 2), 'S'), (((9, 9), 'W'))])
    assert testGame.board.get((0, 9)) == 'N'
    assert testGame.board.get((2, 1)) == 'E'
    assert testGame.board.get((0, 2)) == 'S'
    assert testGame.board.get((9, 9)) == 'W'


def test_intialiseShipLocations_first_location_persists(testGame):
    testGame.initialiseShipLocations([((2, 2), 'N'), ((2, 2), 'E')])
    assert testGame.board.get((2, 2)) == 'N'


def test_moveShip_no_input(testGame):
    with pytest.raises(TypeError):
        testGame.moveShip()


def test_moveShip_invalid_input(testGame):
    with pytest.raises(TypeError):
        testGame.moveShip('invalid')

    with pytest.raises(KeyError):
        testGame.moveShip((10, 10), 'MMLRM')

    with pytest.raises(ValueError):
        testGame.moveShip((0, 9), 'MMLRM')
        testGame.moveShip((2, 3), 'invalid')
        testGame.moveShip('invalid', 'invalid')
        testGame.moveShip((4, 4), 'MM')


def test_moveShip_valid_input(testGame):
    testGame.initialiseShipLocations([((3, 3), 'E'), ((5, 6), 'N'), ((7, 7), 'S')])
    testGame.moveShip((3, 3), 'MMLMMRMM')
    assert testGame.board.get((7, 5)) == 'E'
    testGame.moveShip((5, 6), 'MMLLMMLM')
    assert testGame.board.get((6, 6)) == 'E'
    testGame.moveShip((7, 7), 'MMRMLMLLLMMM')
    assert testGame.board.get((3, 4)) == 'W'


def test_moveShip_north_turn_left(testGame):
    testGame.initialiseShipLocations([((1, 1), 'N')])
    testGame.moveShip((1, 1), 'L')
    assert testGame.board.get((1, 1)) == 'W'


def test_moveShip_west_turn_right(testGame):
    testGame.initialiseShipLocations([((1, 1), 'W')])
    testGame.moveShip((1, 1), 'R')
    assert testGame.board.get((1, 1)) == 'N'


def test_moveShip_to_occupied_cell(testGame):
    testGame.initialiseShipLocations([((2, 2), 'N')])
    testGame.moveShip((0, 0), 'MMRMM')
    assert testGame.board.get((2, 2)) == 'N'


def test_shootShip_no_input(testGame):
    with pytest.raises(TypeError):
        testGame.shootShip()


def test_shootShip_invalid_input(testGame):
    with pytest.raises(KeyError):
        testGame.shootShip('invalid')
        testGame.shootShip(('invalid', 'invalid'))


def test_shootShip_occupied_cell(testGame):
    testGame.initialiseShipLocations([((1, 3), 'N')])
    testGame.shootShip((1, 3))
    assert ((1, 3), 'N') in testGame.sunkenShips


def test_shootShip_empty_cell(testGame):
    testGame.shootShip((1, 3))
    assert ((1, 3), 'N') not in testGame.sunkenShips


def test_parseInputFile_no_input(testGame):
    with pytest.raises(TypeError):
        testGame.parseInputFile()


def test_parseInputFile_invalid_input(testGame):
    with pytest.raises(FileNotFoundError):
        testGame.parseInputFile('tests/inputs/doesntExist.txt')


def test_parseInputFile_valid_input(testGame):
    assert testGame.parseInputFile('tests/inputs/input.txt') == ['10', '(0, 0, N) (9, 2, E)', '(0, 0) MRMLMM', '(9, 2)']


def test_assignOperations_no_input(testGame):
    with pytest.raises(TypeError):
        testGame.assignOperations()


def test_assignOperations_invalid_input(testGame):
    with pytest.raises(ValueError):
        testGame.assignOperations('invalid')


def test_assignOperations_valid_input(testGame):
    assert testGame.assignOperations(['10', '(0, 0, N) (9, 2, E)', '(0, 0) MRMLMM', '(9, 2)']) == {'boardSize': 10, 'movingAndShootingCommands': [((0, 0), 'MRMLMM'), (9, 2)], 'shipLocations': [((0, 0), 'N'), ((9, 2), 'E')]}


def test_assignOperaations_heavy_input(testGame):
    assert testGame.assignOperations(['10', '(0, 0, N) (9, 2, E) (3, 4, E) (5, 6, W) (7, 7, S) (3, 3, W)', '(0, 0) MRMLMM', '(9, 2)', '(3, 5)', '(5, 6) MLRMRR', '(8, 4)', '(7, 7) RMRMMRMMMR', '(5, 3)']) == {'boardSize': 10, 'movingAndShootingCommands': [((0, 0), 'MRMLMM'), (9, 2), (3, 5), ((5, 6), 'MLRMRR'), (8, 4), ((7, 7), 'RMRMMRMMMR'), (5, 3)], 'shipLocations': [((0, 0), 'N'), ((9, 2), 'E'), ((3, 4), 'E'), ((5, 6), 'W'), ((7, 7), 'S'), ((3, 3), 'W')]}


def test_writeOutput_no_occupied_cells_or_sunken_ships(testGame):
    testGame.board = {(7, 3): 0, (6, 9): 0, (1, 3): 0, (4, 8): 0, (3, 0): 0, (2, 8): 0, (9, 8): 0, (8, 0): 0, (0, 7): 0, (6, 2): 0, (1, 6): 0, (3, 7): 0, (2, 5): 0, (8, 5): 0, (5, 8): 0, (4, 0): 0, (9, 0): 0, (6, 7): 0, (5, 5): 0, (7, 6): 0, (5, 0): 0, (0, 4): 0, (3, 5): 0, (1, 1): 0, (3, 2): 0, (2, 6): 0, (8, 2): 0, (4, 5): 0, (9, 3): 0, (6, 0): 0, (1, 4): 0, (7, 5): 0, (2, 3): 0, (1, 9): 0, (8, 7): 0, (4, 2): 0, (9, 6): 0, (6, 5): 0, (5, 3): 0, (0, 1): 0, (7, 0): 0, (6, 8): 0, (3, 1): 0, (9, 9): 0, (0, 6): 0, (1, 7): 0, (0, 9): 0, (7, 8): 0, (2, 4): 0, (8, 4): 0, (5, 9): 0, (4, 7): 0, (9, 1): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (2, 1): 0, (8, 9): 0, (9, 4): 0, (5, 1): 0, (0, 3): 0, (7, 2): 0, (1, 2): 0, (3, 8): 0, (4, 9): 0, (3, 3): 0, (2, 9): 0, (8, 1): 0, (4, 4): 0, (6, 3): 0, (1, 5): 0, (8, 8): 0, (3, 6): 0, (2, 2): 0, (8, 6): 0, (4, 1): 0, (9, 7): 0, (6, 4): 0, (5, 4): 0, (0, 0): 0, (7, 1): 0, (0, 5): 0, (1, 0): 0, (0, 8): 0, (7, 9): 0, (2, 7): 0, (8, 3): 0, (4, 6): 0, (9, 2): 0, (3, 4): 0, (6, 1): 0, (5, 7): 0, (7, 4): 0, (2, 0): 0, (1, 8): 0, (3, 9): 0, (4, 3): 0, (9, 5): 0, (5, 2): 0, (0, 2): 0}
    testGame.sunkenShips = []

    testGame.writeOutput()

    output = open('output.txt').read()
    contents = output.splitlines()
    assert contents == []


def test_writeOutput_no_occupied_cells(testGame):
    testGame.board = {(7, 3): 0, (6, 9): 0, (1, 3): 0, (4, 8): 0, (3, 0): 0, (2, 8): 0, (9, 8): 0, (8, 0): 0, (0, 7): 0, (6, 2): 0, (1, 6): 0, (3, 7): 0, (2, 5): 0, (8, 5): 0, (5, 8): 0, (4, 0): 0, (9, 0): 0, (6, 7): 0, (5, 5): 0, (7, 6): 0, (5, 0): 0, (0, 4): 0, (3, 5): 0, (1, 1): 0, (3, 2): 0, (2, 6): 0, (8, 2): 0, (4, 5): 0, (9, 3): 0, (6, 0): 0, (1, 4): 0, (7, 5): 0, (2, 3): 0, (1, 9): 0, (8, 7): 0, (4, 2): 0, (9, 6): 0, (6, 5): 0, (5, 3): 0, (0, 1): 0, (7, 0): 0, (6, 8): 0, (3, 1): 0, (9, 9): 0, (0, 6): 0, (1, 7): 0, (0, 9): 0, (7, 8): 0, (2, 4): 0, (8, 4): 0, (5, 9): 0, (4, 7): 0, (9, 1): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (2, 1): 0, (8, 9): 0, (9, 4): 0, (5, 1): 0, (0, 3): 0, (7, 2): 0, (1, 2): 0, (3, 8): 0, (4, 9): 0, (3, 3): 0, (2, 9): 0, (8, 1): 0, (4, 4): 0, (6, 3): 0, (1, 5): 0, (8, 8): 0, (3, 6): 0, (2, 2): 0, (8, 6): 0, (4, 1): 0, (9, 7): 0, (6, 4): 0, (5, 4): 0, (0, 0): 0, (7, 1): 0, (0, 5): 0, (1, 0): 0, (0, 8): 0, (7, 9): 0, (2, 7): 0, (8, 3): 0, (4, 6): 0, (9, 2): 0, (3, 4): 0, (6, 1): 0, (5, 7): 0, (7, 4): 0, (2, 0): 0, (1, 8): 0, (3, 9): 0, (4, 3): 0, (9, 5): 0, (5, 2): 0, (0, 2): 0}
    testGame.sunkenShips = [((0, 0), 'N'), ((9, 2), 'E')]

    testGame.writeOutput()

    output = open('output.txt').read()
    contents = output.splitlines()
    assert contents == ['(0, 0, N) SUNK', '(9, 2, E) SUNK']


def test_writeOutput_no_sunken_ships(testGame):
    testGame.board = {(7, 3): 0, (6, 9): 0, (1, 3): 0, (4, 8): 0, (3, 0): 0, (2, 8): 0, (9, 8): 0, (8, 0): 0, (0, 7): 0, (6, 2): 0, (1, 6): 0, (3, 7): 0, (2, 5): 0, (8, 5): 0, (5, 8): 0, (4, 0): 0, (9, 0): 0, (6, 7): 0, (5, 5): 0, (7, 6): 0, (5, 0): 0, (0, 4): 0, (3, 5): 0, (1, 1): 0, (3, 2): 0, (2, 6): 0, (8, 2): 0, (4, 5): 0, (9, 3): 0, (6, 0): 0, (1, 4): 0, (7, 5): 0, (2, 3): 0, (1, 9): 0, (8, 7): 0, (4, 2): 0, (9, 6): 'W', (6, 5): 0, (5, 3): 0, (0, 1): 0, (7, 0): 0, (6, 8): 'E', (3, 1): 0, (9, 9): 0, (0, 6): 0, (1, 7): 0, (0, 9): 'S', (7, 8): 0, (2, 4): 0, (8, 4): 0, (5, 9): 0, (4, 7): 0, (9, 1): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (2, 1): 0, (8, 9): 0, (9, 4): 0, (5, 1): 0, (0, 3): 0, (7, 2): 0, (1, 2): 0, (3, 8): 0, (4, 9): 0, (3, 3): 0, (2, 9): 0, (8, 1): 0, (4, 4): 0, (6, 3): 0, (1, 5): 0, (8, 8): 0, (3, 6): 0, (2, 2): 0, (8, 6): 0, (4, 1): 0, (9, 7): 0, (6, 4): 0, (5, 4): 0, (0, 0): 0, (7, 1): 0, (0, 5): 0, (1, 0): 0, (0, 8): 0, (7, 9): 'N', (2, 7): 0, (8, 3): 0, (4, 6): 0, (9, 2): 0, (3, 4): 0, (6, 1): 0, (5, 7): 0, (7, 4): 0, (2, 0): 0, (1, 8): 0, (3, 9): 0, (4, 3): 0, (9, 5): 0, (5, 2): 0, (0, 2): 0}
    testGame.sunkenShips = []

    testGame.writeOutput()

    output = open('output.txt').read()
    contents = output.splitlines()
    assert contents == ['(7, 9, N)', '(9, 6, W)', '(6, 8, E)', '(0, 9, S)']


def test_writeOutput_valid_occupied_cells_and_sunken_ships(testGame):
    testGame.board = {(7, 3): 0, (6, 9): 0, (1, 3): 0, (4, 8): 0, (3, 0): 0, (2, 8): 0, (9, 8): 0, (8, 0): 0, (0, 7): 0, (6, 2): 0, (1, 6): 0, (3, 7): 0, (2, 5): 0, (8, 5): 0, (5, 8): 0, (4, 0): 0, (9, 0): 0, (6, 7): 0, (5, 5): 0, (7, 6): 0, (5, 0): 0, (0, 4): 0, (3, 5): 0, (1, 1): 0, (3, 2): 0, (2, 6): 0, (8, 2): 0, (4, 5): 0, (9, 3): 0, (6, 0): 0, (1, 4): 0, (7, 5): 0, (2, 3): 0, (1, 9): 0, (8, 7): 0, (4, 2): 0, (9, 6): 'W', (6, 5): 0, (5, 3): 0, (0, 1): 0, (7, 0): 0, (6, 8): 'E', (3, 1): 0, (9, 9): 0, (0, 6): 0, (1, 7): 0, (0, 9): 'S', (7, 8): 0, (2, 4): 0, (8, 4): 0, (5, 9): 0, (4, 7): 0, (9, 1): 0, (6, 6): 0, (5, 6): 0, (7, 7): 0, (2, 1): 0, (8, 9): 0, (9, 4): 0, (5, 1): 0, (0, 3): 0, (7, 2): 0, (1, 2): 0, (3, 8): 0, (4, 9): 0, (3, 3): 0, (2, 9): 0, (8, 1): 0, (4, 4): 0, (6, 3): 0, (1, 5): 0, (8, 8): 0, (3, 6): 0, (2, 2): 0, (8, 6): 0, (4, 1): 0, (9, 7): 0, (6, 4): 0, (5, 4): 0, (0, 0): 0, (7, 1): 0, (0, 5): 0, (1, 0): 0, (0, 8): 0, (7, 9): 'N', (2, 7): 0, (8, 3): 0, (4, 6): 0, (9, 2): 0, (3, 4): 0, (6, 1): 0, (5, 7): 0, (7, 4): 0, (2, 0): 0, (1, 8): 0, (3, 9): 0, (4, 3): 0, (9, 5): 0, (5, 2): 0, (0, 2): 0}
    testGame.sunkenShips = [((0, 0), 'N'), ((9, 2), 'E')]

    testGame.writeOutput()

    output = open('output.txt').read()
    contents = output.splitlines()
    assert contents == ['(7, 9, N)', '(9, 6, W)', '(6, 8, E)', '(0, 9, S)', '(0, 0, N) SUNK', '(9, 2, E) SUNK']


def test_calculateGame_no_input(testGame):
    testGame.gameInformation['movingAndShootingCommands'] = []
    with pytest.raises(TypeError):
        testGame.calculateGame()


def test_calculateGame_valid_input(testGame):
    testGame.board[(0, 0)] = 'N'
    testGame.board[(9, 2)] = 'E'
    testGame.gameInformation['movingAndShootingCommands'] = [((0, 0), 'MRMLMM'), (9, 2)]

    testGame.calculateGame()

    assert testGame.board.get((1, 3)) == 'N'
    assert testGame.sunkenShips == [((9, 2), 'E')]


if __name__ == '__main__':
    pytest.main()
