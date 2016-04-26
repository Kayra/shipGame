import sys
from pkg_resources import resource_filename
from shipGame.utils import (deconstructShipLocation, formatShipLocationOutput, formatShipLocationInput,
                            formatMoveCommandInput, formatShootCommandInput, isMoveCommand, isShootCommand)


class ShipGame(object):

    def __init__(self, filename):
        """
        Initialises the object by creating the compass mapping and parsing the data in the input file
        and assigning it to the relevant variables.
        """
        self.sunkenShips = []
        self.compassMapping = ['N', 'E', 'S', 'W']
        inputFileContents = self.parseInputFile(filename)
        self.gameInformation = self.assignGameParameters(inputFileContents)

        try:
            self.board = self.initialiseBoard(self.gameInformation['boardSize'])
            self.initialiseShipLocations(self.gameInformation['shipLocations'])
        except KeyError:
            sys.exit('Initialisation failed. Data missing from input file.')

    def initialiseBoard(self, size):
        """
        Creates a game board of square 'size' x 'size', where 'size' is a positive integer.
        Each cell can be empty, or occupied by a ship. This is denoted by a 0 integer value for empty,
        or one of N, E, S, W string values to specify the orientation for a ship in an occupied cell.
        """

        board = {}
        for row in range(size):
            for column in range(size):
                board[(row, column)] = 0
        return board

    def initialiseShipLocations(self, shipLocations):
        """
        Places each ship into the appropriate cell on the existing board, with the correct orientation
        as the value for the cell.
        Example input for two ships: [((0, 0), 'N'), ((9, 2), 'E')]
        Example result portion: {(0, 0): 'N', (6, 5): 0, (5, 3): 0, (9, 2): 'E'}
        Working with the assumption that the first location's direction persists.
        """
        for ship in shipLocations:
            coordinates, direction = deconstructShipLocation(ship)
            if self.board[coordinates] == 0 and direction in self.compassMapping:
                self.board[coordinates] = direction

    def moveShip(self, shipLocation, moveCommands):
        """
        Moves a ship specified by an initial coordinate a series of cells forward (in the direction
        that the ship is facing), and accordingly rotates it left and right.
        A ship can navigate through an occupied cell. However, two ships cannot occupy the same cell
        at the end of a move operation.
        Example input: (0, 0), MRMLMM
        Example result portion (if initial direction 'N'): {(0, 0): 0, (6, 5): 0, (1, 3): 'N', (9, 2): 0}
        Working with the assumption that the bottom-left cell is the origin (0, 0).
        """

        if not moveCommands:
            raise TypeError("No move operations given.")

        for moveOperation in moveCommands:
            if moveOperation not in 'MRL':
                raise ValueError("Invalid move operations. Must be in 'MRL'. %s was given." % moveOperation)

        def getDirection(shipLocation):
            """
            Takes a two integer tuple coordinate and returns a string compass direction.
            Example input: (1, 2)
            Example output: 'N'
            """
            return self.board[shipLocation]

        def changeDirection(initialDirection, directionToTurn):
            """
            Takes an initial string compass direction, and a string of L or R to denote
            which direction to turn, and returns the new string compass direction.
            Example input: 'N', 'L'
            Example output: 'W'
            """

            direction = self.compassMapping.index(initialDirection)

            if directionToTurn == 'R':
                if direction != 3:
                    direction += 1

                elif direction == 3:
                    direction = 0

            elif directionToTurn == 'L':
                if direction != 0:
                    direction -= 1

                elif direction == 0:
                    direction = 3

            return self.compassMapping[direction]

        def move(initialCoordinates, direction):
            """
            Takes an initial two integer tuple coordinate, and a string compass direction, and
            returns a new two integer coordinate.
            Example input: (1, 2) 'N'
            Example output: (1, 3)
            """
            x, y = initialCoordinates

            if direction == 'N':
                y += 1
            elif direction == 'E':
                x += 1
            elif direction == 'S':
                y -= 1
            elif direction == 'W':
                x -= 1

            return (x, y)

        direction = getDirection(shipLocation)

        if direction == 0:
            raise ValueError("Attempting to move a ship that does not exist.")

        location = shipLocation
        initialLocation = shipLocation

        for moveCommand in moveCommands:
            if moveCommand == 'M':
                location = move(location, direction)
            elif moveCommand in ('L', 'R'):
                direction = changeDirection(direction, moveCommand)

        if 'M' not in moveCommands:
            self.board[location] = direction
        elif self.board[location] == 0:
            self.board[initialLocation] = 0
            self.board[location] = direction

    def shootShip(self, shipLocation):
        """
        Takes a two integer tuple coordinate. If it the cell contains a ship, it
        adds the ship location to a list of sunken ships to be output later.
        Example input: (9, 2)
        Example result: [((9, 2), 'N')]
        """
        if self.board[shipLocation] != 0:
            self.sunkenShips.append((shipLocation, self.board[shipLocation]))
            self.board[shipLocation] = 0

    def parseInputFile(self, fileName):
        """
        Reads the contents of a text file and returns a list of strings representing the lines
        in the file.
        Example input: 'input.txt'
        Example output: ['10', '(0, 0, N) (9, 2, E)', '(0, 0) MRMLMM', '(9, 2)']
        """
        file = resource_filename('shipGame', fileName)
        contents = open(file).read()
        return contents.splitlines()

    def assignGameParameters(self, parameters):
        """
        Returns a dictionary containing the game parameters from the contents of a text file.
        Example input: ['10', '(0, 0, N) (9, 2, E)', '(0, 0) MRMLMM', '(9, 2)']
        Example output: {'boardSize': 10,
                         'shipLocations': [(('0', '0'), 'N'),
                                           (('9', '2'), 'E')],
                         'movingAndShootingCommands': [((0, 0), 'MRMLMM'),
                                                       (9, 2)]}
        """

        def parseShipLocations(shipLocationsString):
            """
            Parses a string of ship locations and formats it into a list of tuples each
            containing a two integer tuple location and string direction.
            Example input: "(0, 0, N) (9, 2, E)"
            Example output: [(('0', '0'), 'N'), (('9', '2'), 'E')]
            """
            return [(formatShipLocationInput(location)) for location in shipLocationsString.split(') (')]

        def parseMoveOrShoot(commandString):
            """
            Parses a string of either a move or a shoot command and fomats it into a tuple
            containing the relevant information.
            Example input for move: '(0, 0) MRMLMM'
            Example output for move: ((0, 0), 'MRMLMM')
            Example input for shoot: '(9, 2)'
            Example output for shoot: (9, 2)
            """
            if isMoveCommand(commandString):
                coordinates, direction = formatMoveCommandInput(commandString)
                return((coordinates, direction))

            elif isShootCommand(commandString):
                coordinates = formatShootCommandInput(commandString)
                return((coordinates))

        gameInformation = {}
        movingAndShootingCommands = []

        for index, parameter in enumerate(parameters):
            if index == 0:
                gameInformation['boardSize'] = int(parameter)
            elif index == 1:
                gameInformation['shipLocations'] = parseShipLocations(parameter)
            else:
                movingAndShootingCommands.append(parseMoveOrShoot(parameter))

        if movingAndShootingCommands:
            gameInformation['movingAndShootingCommands'] = movingAndShootingCommands

        return gameInformation

    def writeOutput(self):
        """
        Writes a list of existing and sunken ship's locations and directions to a text file.
        Example input portion: {(7, 3): 0, (6, 9): 0, (9, 6): 'W', (7, 9): 'N'}
                               [((0, 0), 'N'), ((9, 2), 'E')]
        Example result: ['(7, 9, N)', '(9, 6, W)', '(0, 0, N) SUNK', '(9, 2, E) SUNK']
        """
        file = resource_filename('shipGame', 'output.txt')
        output = open(file, 'w')

        for key, value in self.board.items():
            if value != 0:
                string = formatShipLocationOutput(key, value)
                output.write(string)
                output.write('\n')

        for ship in self.sunkenShips:
            string = formatShipLocationOutput(ship[0], ship[1]) + ' SUNK'
            output.write(string)
            output.write('\n')

    def calculateGame(self):
        """
        Runs through the move and shoot commands to alter the board based
        on their contents.
        """
        if not self.gameInformation['movingAndShootingCommands']:
            raise TypeError('No commands to calculate')

        for command in self.gameInformation['movingAndShootingCommands']:
            if isMoveCommand(command):
                self.moveShip(command[0], command[1])
            elif isShootCommand(command):
                self.shootShip(command)


if __name__ == '__main__':
    shipGame = ShipGame('input.txt')
    shipGame.calculateGame()
    shipGame.writeOutput()
