from TetrisGame import TetrisGame

def simulate_game(pieces):
    '''
    Return height of board at end of adding `pieces`

    Args:
        pieces (list of tuple): list of (piece, pos) representing piece name and column index
    '''
    game = TetrisGame()
    for p, i in pieces:
        game.add(p, i)
    return game.get_height()


def parse_sequence(pieces):
    '''
    Return list of tuples of (piece, pos) of piece name and column index

    Args:
        pieces (str): `pieces` is a comma separated list, each item is a string with 2 characters of piece name and column index
    '''
    if len(pieces) == 0:
        return []
    else:
        return [(x[0], int(x[1])) for x in pieces.split(',')]
    

if __name__ == '__main__':
    import sys
    first = True
    for l in sys.stdin.readlines():
        if first:
            sys.stdout.write(str(simulate_game(parse_sequence(l.strip()))))
            first = False
        else:
            sys.stdout.write('\n' + str(simulate_game(parse_sequence(l.strip()))))