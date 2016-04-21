import sys


class ShipGame(object):

    def __init__(self, filename):
        self.sunkenShips = []
        self.compassMapping = ['N', 'E', 'S', 'W']
        inputFileContents = self.parseInputFile(filename)
        self.gameInformation = self.assignOperations(inputFileContents)

        try:
            self.board = self.initialiseBoard(self.gameInformation['boardSize'])
            self.initialiseShipLocations(self.gameInformation['shipLocations'])
        except KeyError:
            sys.exit('Initialisation failed. Data missing from input file.')


    def initialiseBoard(self, size):
        """
        Create a game board of square 'size' x 'size', where 'size' is a positive integer.
        Each cell can be empty, or occupied by a ship. This is denoted by a 0 integer value for empty,
        or one of N, E, S, W string values to specify the orientation for a ship in an occupied cell.
        """
        if type(size) is not int or size < 1:
            raise ValueError('Board size must be a positive integer.')

        else:
            board = {}
            for row in range(size):
                for column in range(size):
                    board[(row, column)] = 0
            return board


    def initialiseShipLocations(self, shipLocations):
        """
        Place each ship into the appropriate cell on the existing board, with the correct orientation
        as the value for the cell.
        Example input for two ships: [((0, 0), 'N'), ((9, 2), 'E')]
        Working with the assumption that the first location's direction persists.
        """
        for ship in shipLocations:
            coordinates = (ship[0][0], ship[0][1])
            if self.board[coordinates] == 0 and ship[1] in self.compassMapping:
                self.board[coordinates] = ship[1]


    def moveShip(self, shipLocation, moveOperations):
        """
        Working with the assumption that the bottom-left cell is the origin (0, 0).
        Specified by an initial coordinate and a series of movements which can be move forward (in the
        direction that ship is facing), rotate left, rotate right.
        A ship can navigate through an occupied cell. However, two ships cannot occupy the same cell
        at the end of a move operation.
        Example input: (0, 0), MRMLMM
        """

        if not moveOperations:
            raise TypeError("No move operations given.")

        for moveOperation in moveOperations:
            if moveOperation not in 'MRL':
                raise ValueError("Invalid move operations.")

        def getDirection(shipLocation):
            """
            Takes a two integer tuple coordinate and returns a string compass direction.
            """
            return self.board[shipLocation]

        def changeDirection(initialDirection, directionToTurn):
            """
            Takes an initial string compass direction, and a string of L or R to denote
            which direction to turn, and returns the new string compass direction.
            Example input: 'N', 'L'
            """

            direction = self.compassMapping.index(initialDirection)

            if directionToTurn == 'R' and direction != 3:
                direction += 1
            elif directionToTurn == 'L' and direction != 0:
                direction -= 1
            elif directionToTurn == 'R' and direction == 3:
                direction = 0
            elif directionToTurn == 'L' and direction == 0:
                direction = 3

            return self.compassMapping[direction]


        def move(initialCoordinates, direction):
            """
            Takes an initial two integer tuple coordinate, and a string compass direction, and
            returns a new two integer coordinate.
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

        for moveOperation in moveOperations:
            if moveOperation == 'M':
                location = move(location, direction)
            elif moveOperation in ('L', 'R'):
                direction = changeDirection(direction, moveOperation)

        if 'M' not in moveOperations:
            self.board[location] = direction
        elif self.board[location] == 0:
            self.board[initialLocation] = 0
            self.board[location] = direction


    def shootShip(self, shipLocation):
        """
        Takes a two integer tuple coordinate. If it contains a ship, it adds the ship
        and direction to a list of sunken ships to be output later.
        Example input: (9, 2)
        """
        if self.board[shipLocation] != 0:
            self.sunkenShips.append((shipLocation, self.board[shipLocation]))
            self.board[shipLocation] = 0


    def parseInputFile(self, fileName):
        """
        Reads the contents of a text file and returns a list of strings representing the lines
        in the file.
        """
        contents = open(fileName).read()
        return contents.splitlines()


    def assignOperations(self, operations):
        """
        Return a dictionary containing the game operations from the contents of a text file.
        Example output: {'boardSize': 10,
                         'shipLocations': [(('0', '0'), 'N'),
                                           (('9', '2'), 'E')],
                         'movingAndShootingCommands': [((0, 0), 'MRMLMM'),
                                                       (9, 2)]}
        """

        def parseShipLocations(shipLocationsString):
            """
            Parse a string of ship locations and format it into a list of tuples containing
            a location and direction.
            Example input: "(0, 0, N) (9, 2, E)"
            Example output: [(('0', '0'), 'N'), (('9', '2'), 'E')]
            """
            shipLocations = []
            for location in shipLocationsString.split(') ('):
                charactersToRemove = str.maketrans("", "", ",() ")
                shipLocation = location.translate(charactersToRemove)
                coordinates = int(shipLocation[0]), int(shipLocation[1])
                direction = shipLocation[2]
                shipLocations.append((coordinates, direction))

            return shipLocations

        def parseMoveOrShoot(operationString):
            """
            Parse a string of either a move or shoot command and fomat it into a tuple
            containing the relevant information.
            Example output for move: ((0, 0), 'MRMLMM')
            Example output for shoot: (9, 2)
            """

            if isMoveCommand(operation):
                charactersToRemove = str.maketrans("", "", ",() ")
                operationString = operation.translate(charactersToRemove)
                coordinates = (int(operationString[0]), int(operationString[1]))
                moveCommands = operationString[2:]
                return((coordinates, moveCommands))

            elif isShootCommand(operation):
                charactersToRemove = str.maketrans("", "", ",() ")
                operationString = operation.translate(charactersToRemove)
                return((int(operationString[0]), int(operationString[1])))

        def isMoveCommand(operation):
            return len(operation.split()) == 3

        def isShootCommand(operation):
            return len(operation.split()) == 2

        gameInformation = {}
        movingAndShootingCommands = []

        for index, operation in enumerate(operations):
            if index == 0:
                gameInformation['boardSize'] = int(operation)
            elif index == 1:
                gameInformation['shipLocations'] = parseShipLocations(operation)
            else:
                movingAndShootingCommands.append(parseMoveOrShoot(operation))

        if movingAndShootingCommands:
            gameInformation['movingAndShootingCommands'] = movingAndShootingCommands

        return gameInformation


    def writeOutput(self):
        """
        Writes a list of existing and sunken ship's locations and directions to a text file.
        """
        output = open('output.txt', 'w')

        for key, value in self.board.items():
            if value != 0:
                charactersToRemove = str.maketrans("", "", "()")
                string = '(' + str(key).translate(charactersToRemove) + ', ' + value + ')'
                output.write(string)
                output.write('\n')

        for ship in self.sunkenShips:
            charactersToRemove = str.maketrans("", "", "()")
            string = '(' + str(ship[0]).translate(charactersToRemove) + ', ' + ship[1] + ') SUNK'
            output.write(string)
            output.write('\n')


    def calculateGame(self):
        def isMoveCommand(operation):
            return type(operation[1]) is str

        def isShootCommand(operation):
            return type(operation[1]) is int

        if not self.gameInformation['movingAndShootingCommands']:
            raise TypeError('No commands to calculate')

        for operation in self.gameInformation['movingAndShootingCommands']:
            if isMoveCommand(operation):
                self.moveShip(operation[0], operation[1])
            elif isShootCommand(operation):
                self.shootShip(operation)


if __name__ == '__main__':
    shipGame = ShipGame('input.txt')
    shipGame.calculateGame()
    shipGame.writeOutput()
