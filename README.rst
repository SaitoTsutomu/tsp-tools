`tsp` is a package for Traveling Salesman Problem for Python.

::

    import tsp
    t = tsp.tsp([(0,0), (0,1), (1,0), (1,1)])
    print(t)  # distance, node index list
    >>>
    (4, [0, 1, 3, 2])

    mat = [[  0,   1, 1, 1.5],
           [  1,   0, 1.5, 1],
           [  1, 1.5,   0, 1],
           [1.5,   1,   1, 0]]  # Distance Matrix
    r = range(len(mat))
    # Dictionary of distance
    dist = {(i, j): mat[i][j] for i in r for j in r}
    print(tsp.tsp(r, dist))
    >>>
    (4, [0, 1, 3, 2])

See also https://pypi.org/project/ortoolpy/

Requirements
------------
* Python 3
* PuLP
* more-itertools

Features
--------
* nothing

Setup
-----
::

   $ pip install tsp

History
-------
0.0.1 (2015-10-2)
~~~~~~~~~~~~~~~~~~
* first release
