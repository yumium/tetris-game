# PyTest file
import sys
sys.path.append('../')
from TetrisGame import TetrisGame
from tetris import parse_sequence, simulate_game
import pytest

def test_add_empty():
    # setup
    board = []
    tetris = TetrisGame()
    tetris._set_board(board)

    # execute
    tetris.add('Q', 0)

    # assert
    assert tetris.board[::-1] == [
        [1,1,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0]
    ] and tetris.heights == [2,2,0,0,0,0,0,0,0,0]

def test_add_stack():
    # setup
    board = [
        [1,1,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0]
    ]
    tetris = TetrisGame()
    tetris._set_board(board)

    # execute
    tetris.add('Q', 1)

    # assert
    assert tetris.board[::-1] == [
        [0,1,1,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0]
    ] and tetris.heights == [2,4,4,0,0,0,0,0,0,0]

def test_add_clear_line():
    # setup
    board = [
        [1,1,1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,1,0,0]
    ]
    tetris = TetrisGame()
    tetris._set_board(board)

    # execute
    tetris.add('J', 8)

    # assert
    assert tetris.board[::-1] == [
        [0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,0,1]
    ] and tetris.heights == [1,1,1,1,1,1,1,1,0,2]

def test_add_clear_line_multiple():
    # setup
    board = [
        [1,1,1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,1,1,0,0]
    ]
    tetris = TetrisGame()
    tetris._set_board(board)

    # execute
    tetris.add('Q', 8)

    # assert
    assert tetris.board[::-1] == [] and tetris.heights == [0,0,0,0,0,0,0,0,0,0]

def test_get_height_empty():
    # setup
    tetris = TetrisGame()
    board = []
    tetris._set_board(board)

    # execute
    res = tetris.get_height()

    # assert
    assert res == 0

def test_get_height_single():
    # setup
    tetris = TetrisGame()
    board = [
        [1,1,0,0,0,0,0,0,0,0]
    ]
    tetris._set_board(board)

    # execute
    res = tetris.get_height()

    # assert
    assert res == 1

def test_get_height_multiple():
    # setup
    tetris = TetrisGame()
    board = [
        [1,1,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0]
    ]
    tetris._set_board(board)

    # execute
    res = tetris.get_height()

    # assert
    assert res == 2

def test__lock_empty():
    # setup
    tetris = TetrisGame()
    piece = [
        [1,1],
        [1,1]
    ]
    board = []
    tetris._set_board(board)

    # execute
    res = tetris._lock(piece, 0)

    # assert
    assert res == 1

def test__lock_stack():
    # setup
    tetris = TetrisGame()
    piece = [
        [0,1,1],
        [1,1,0]
    ]
    board = [[1,1,0,0,0,0,0,0,0,0]]
    tetris._set_board(board)

    # execute
    res = tetris._lock(piece, 1)

    # assert
    assert res == 2

def test__lock_fit():
    # setup
    tetris = TetrisGame()
    piece = [
        [1,1,1],
        [0,1,0]
    ]
    board = [
        [1,0,1,0,0,0,0,0,0,0],
        [1,1,1,0,0,0,0,0,0,0]
    ]
    tetris._set_board(board)

    # execute
    res = tetris._lock(piece, 0)

    # assert
    assert res == 2

def test_parse_sequence_empty():
    # setup
    seq = ''

    # execute
    res = parse_sequence(seq)

    # assert
    assert res == []

def test_parse_sequence_single():
    # setup
    seq = 'Q0'

    # execute
    res = parse_sequence(seq)

    # assert
    assert res == [('Q',0)]

def test_parse_sequence_multiple():
    # setup
    seq = 'Q0,Q0,T2'

    # execute
    res = parse_sequence(seq)

    # assert
    assert res == [('Q',0), ('Q',0), ('T',2)]

def load_test_cases():
    with open('./test.in', 'r') as f:
        return [l.strip() for l in f.readlines()]

def load_answers():
    with open('./test.ans', 'r') as f:
        return [int(l.strip()) for l in f.readlines()]

@pytest.mark.parametrize("sequence,ans", list(zip(load_test_cases(), load_answers())))
def test_tetris_game(sequence, ans):
    # execute
    res = simulate_game(parse_sequence(sequence))

    # assert
    assert res == ans
