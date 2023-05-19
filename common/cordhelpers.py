def parse_coordinate(coordinate):
    coordinate = coordinate.upper()  # Convert to uppercase for consistency

    if len(coordinate) < 2 or not coordinate[0].isalpha() or not coordinate[1:].isdigit():
        print ("Invalid coordinate format")
        return (-1, -1)

    column = ord(coordinate[0]) - 65  # Convert letter to column index (0-based)
    row = int(coordinate[1:]) - 1  # Convert number to row index (0-based)
    
    if row < 0 or column < 0:
        print ("Invalid coordinate values")
        return (-1, -1)
    
    return (column, row)
