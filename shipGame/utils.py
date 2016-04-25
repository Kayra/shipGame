
def removeStringCharacters(string):
    """
    Removes unnecessary characters from a string.
    Example input: '(1, 3, N)'
    Example output: '13N'
    """
    charactersToRemove = str.maketrans("", "", ",() ")
    return string.translate(charactersToRemove)


def deconstructShipLocation(shipLocation):
    """
    Returns the coordinates and direction of a ship location separated out.
    Example input: ((1, 3), 'N')
    Example output: (1, 3), 'N'
    """
    return (shipLocation[0][0], shipLocation[0][1]), shipLocation[1]


def formatShipLocationOutput(coordinates, direction):
    """
    Returns a formatted ship location string ready to be written to an output file.
    Example input: (1, 3), 'N'
    Example output: '(1, 3, N)'
    """
    charactersToRemove = str.maketrans("", "", "()")
    return '(' + str(coordinates).translate(charactersToRemove) + ', ' + direction + ')'


def formatShipLocationInput(locationString):
    """
    Takes a string denoting a ship location and returns the integer coordinates and
    string direction of the ship separated out.
    Example input: '(0, 0, N)'
    Example output: 0, 0, 'N'
    """
    strippedShipLocationString = removeStringCharacters(locationString)
    coordinates = int(strippedShipLocationString[0]), int(strippedShipLocationString[1])
    direction = strippedShipLocationString[2]
    return coordinates, direction


def formatMoveCommandInput(moveCommandString):
    """
    Takes a string denoting a move command and returns the integer coordinates and
    string move operations of the command separated out.
    Example input: '(0, 0) MRMLMM'
    Example output: 0, 0, 'MRMLMM'
    """
    strippedMoveCommandString = removeStringCharacters(moveCommandString)
    coordinates = (int(strippedMoveCommandString[0]), int(strippedMoveCommandString[1]))
    moveOperations = strippedMoveCommandString[2:]
    return coordinates, moveOperations


def formatShootCommandInput(shootCommandString):
    """
    Takes a string denoting a shoot command and returns the integer coordinates of the command.
    Example input: '(9, 2)'
    Example output: 9, 2
    """
    strippedShootCommandString = removeStringCharacters(shootCommandString)
    return int(strippedShootCommandString[0]), int(strippedShootCommandString[1])


def isMoveCommand(command):
    """
    Checks to see if the value passed in is a move command or not.
    Example input: ((0, 0), 'MRMLMM')
    Example output: True
    """
    if type(command) is str:
        return len(command.split()) == 3
    else:
        return type(command[1]) is str


def isShootCommand(command):
    """
    Checks to see if the value passed in is a shoot command or not.
    Example input: (9, 2)
    Example output: True
    """
    if type(command) is str:
        return len(command.split()) == 2
    else:
        return type(command[1]) is int
