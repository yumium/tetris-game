# Tetris Game Simulator
A simulator for Tetris that takes in a comma separated list of Tetris pieces and positions and return the height of the final board.

The pieces take the following shape:

![tetris-pieces](.\static\tetris-pieces.png)

 An example input could be

> Q0,I2,I6,I0,I6,I6,Q2,Q4

Meaning in the game we first add shape T where its left column is positioned at column with index 0, then adding shape Z where its left column is positioned at column with index 2, and so on ...

Here, the board has 10 columns. There is no height limit.

After the first three pieces drop, the result is as follows:

![step-1](.\static\step-1.png)

The bottom line is cleared, and after the next five pieces drop, here is the result:

![step-2](.\static\step-2.png)

The second line clears, and the final result is as follows:

![step-3](.\static\step-3.png)

Hence, the simulator returns height "3".





### Example usage
Running in command line
```bash
$ ./tetris < input.txt > output.txt
```

Where `input.txt` contains sequences of pieces inputs:
```

Q0
Q0,Q2,Q4,Q6,Q8,Q1
Q0,I2,I6,I0,I6,I6,Q2,Q4
```

And `output.txt` should contain the corresponding resulting heights:
```
0
2
2
3
```





### Running tests

To run the unit tests you will have to install [pytest](https://docs.pytest.org/en/7.1.x/index.html). Then simply:
```shell
cd tests
python -m pytest .\test_tetris.py
```

To visualise the test coverage you will have to additionally install [pytest-cov](https://pypi.org/project/pytest-cov/). Then simply: 
```shell
py.test --cov tetris --cov-report html --cov-branch .\test_tetris.py
```

