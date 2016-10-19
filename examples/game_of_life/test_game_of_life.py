import unittest

from boolean_solver.solver import Conditions, Code, execute
from examples.game_of_life.game_of_life import is_alive, valid_indexes, get_neighbors, me, solve


class GameOfLifeTest(unittest.TestCase):

    def test_living_rule(self):

        """
        1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        2. Any live cell with more than three live neighbours dies, as if by overcrowding.
        3. Any live cell with two or three live neighbours lives on to the next generation.
        4. Any dead cell with exactly three live neighbours becomes a live cell.
        """

        cond = Conditions(rule1=Code(code_str='sum(neighbors) < 2'), output=False)
        cond.add(rule2=Code('sum(neighbors) > 3'), output=False)
        cond.add(alive=True, rule3=Code(code_str='sum(neighbors) == 2'), output=True)
        cond.add(alive=True, rule4=Code(code_str='sum(neighbors) == 3'), output=True)
        cond.add(alive=False, rule5=Code(code_str='sum(neighbors) == 3'), output=True)

        execute(self, is_alive, cond)

    def test_valid_indexes(self):

        # TODO: ERROR when output is not present. FIX
        cond = Conditions(more_than1=Code(code_str='idx1 >= 0'),
                          less_than1=Code(code_str='idx1 < max_idx1'),
                          more_than2=Code(code_str='idx2 >= 0'),
                          less_than2=Code(code_str='idx2 < max_idx2'), output=True)

        execute(self, valid_indexes, cond)

    def test_me(self):

        #TODO: make it right should return not (idx1 != x and idx1 != y)
        #cond = Conditions(different1=Code('idx1 != x'),
        #                  different2=Code('idx2 != y'), output=False)

        cond = Conditions(different1=Code(code_str='idx == x'),
                          different2=Code(code_str='idy == y'), output=True)
        execute(self, me, cond)

    def test_get_neighbors(self):

        cells = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        self.assertEqual(get_neighbors(x=1, y=1, cells=cells), [0, 1, 0, 0, 0, 0, 1, 0])
        self.assertEqual(get_neighbors(x=0, y=0, cells=cells), [1, 0, 1])
        self.assertEqual(get_neighbors(x=1, y=0, cells=cells), [0, 0, 0, 1, 0])
        self.assertEqual(get_neighbors(x=2, y=1, cells=cells), [1, 0, 1, 1, 0])

    def test_solve(self):

        cells = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[0, 0, 0], [0, 0, 0], [0, 1, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[1, 1, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        cells = [[1, 1, 0], [1, 0, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[1, 1, 0], [1, 1, 0], [0, 0, 0]])

        # Square lives forever!!!
        cells = [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
        self.assertEqual(solve(cells), [[1, 1, 0], [1, 1, 0], [0, 0, 0]])