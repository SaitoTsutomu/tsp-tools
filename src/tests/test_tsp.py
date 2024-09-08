from tsp_tools import tsp


def test_tsp():
    actual = tsp([(0, 0), (0, 1), (1, 0), (1, 1)])
    assert actual == (4.0, [0, 2, 3, 1])
