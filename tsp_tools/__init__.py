def tsp(nodes, dist=None):
    """
    巡回セールスマン問題
    入力
        nodes: 点(dist未指定時は、座標)のリスト
        dist: (i,j)をキー、距離を値とした辞書
    出力
        距離と点番号リスト
    """
    import numpy as np
    import pandas as pd
    from more_itertools import iterate, take
    from pulp import PULP_CBC_CMD, LpBinary, LpProblem, LpVariable, lpDot, lpSum, value

    n = len(nodes)
    if not dist:
        dist = {
            (i, j): np.linalg.norm(np.subtract(nodes[i], nodes[j]))
            for i in range(n)
            for j in range(i + 1, n)
        }
        dist.update({(j, i): d for (i, j), d in dist.items()})
    a = pd.DataFrame(
        [(i, j, dist[i, j]) for i in range(n) for j in range(n) if i != j],
        columns=["NodeI", "NodeJ", "Dist"],
    )
    m = LpProblem()
    m.setSolver(PULP_CBC_CMD(msg=False))
    a["VarIJ"] = [LpVariable("x%d" % i, cat=LpBinary) for i in a.index]
    a["VarJI"] = a.sort_values(["NodeJ", "NodeI"]).VarIJ.values
    u = [0] + [LpVariable("y%d" % i, lowBound=0) for i in range(n - 1)]
    m += lpDot(a.Dist, a.VarIJ)
    for _, v in a.groupby("NodeI"):
        m += lpSum(v.VarIJ) == 1  # 出次数制約
        m += lpSum(v.VarJI) == 1  # 入次数制約
    for _, (i, j, _, vij, vji) in a.query("NodeI!=0 & NodeJ!=0").iterrows():
        m += u[i] + 1 - (n - 1) * (1 - vij) + (n - 3) * vji <= u[j]  # 持ち上げポテンシャル制約(MTZ)
    for _, (_, j, _, v0j, vj0) in a.query("NodeI==0").iterrows():
        m += 1 + (1 - v0j) + (n - 3) * vj0 <= u[j]  # 持ち上げ下界制約
    for _, (i, _, _, vi0, v0i) in a.query("NodeJ==0").iterrows():
        m += u[i] <= (n - 1) - (1 - vi0) - (n - 3) * v0i  # 持ち上げ上界制約
    m.solve()
    a["ValIJ"] = a.VarIJ.apply(value)
    dc = dict(a[a.ValIJ > 0.5][["NodeI", "NodeJ"]].values)
    return value(m.objective), list(take(n, iterate(lambda k: dc[k], 0)))


def tsp2(pos):
    """
    巡回セールスマン問題
    入力
        pos: 座標のリスト
    出力
        距離と点番号リスト
    """
    import numpy as np
    from ortoolpy import unionfind
    from pulp import LpBinary, LpProblem, LpVariable, lpDot, lpSum, value

    pos = np.array(pos)
    N = len(pos)
    m = LpProblem()
    v = {}
    for i in range(N):
        for j in range(i + 1, N):
            v[i, j] = v[j, i] = LpVariable("v%d%d" % (i, j), cat=LpBinary)
    m += lpDot(
        [np.linalg.norm(pos[i] - pos[j]) for i, j in v if i < j],
        [x for (i, j), x in v.items() if i < j],
    )
    for i in range(N):
        m += lpSum(v[i, j] for j in range(N) if i != j) == 2
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                m += v[i, j] + v[j, k] + v[k, i] <= 2
    st = set()
    while True:
        m.solve()
        u = unionfind(N)
        for i in range(N):
            for j in range(i + 1, N):
                if value(v[i, j]) > 0:
                    u.unite(i, j)
        gg = u.groups()
        if len(gg) == 1:
            break
        for g_ in gg:
            g = tuple(g_)
            if g not in st:
                st.add(g)
                m += (
                    lpSum(
                        v[i, j]
                        for i in range(N)
                        for j in range(i + 1, N)
                        if (i in g and j not in g) or (i not in g and j in g)
                    )
                    >= 1
                )
                break
    cn = [0] * N
    for i in range(N):
        for j in range(i + 1, N):
            if value(v[i, j]) > 0:
                if i or cn[i] == 0:
                    cn[i] += j
                cn[j] += i
    p, q, r = cn[0], 0, [0]
    while p != 0:
        r.append(p)
        q, p = p, cn[p] - q
    return value(m.objective), r


def tsp3(point):
    from itertools import permutations
    from math import sqrt

    n = len(point)
    bst, mn = None, 1e100
    for d in permutations(range(1, n)):
        e = [point[i] for i in [0] + list(d) + [0]]
        s = sum(
            sqrt((e[i][0] - e[i + 1][0]) ** 2 + (e[i][1] - e[i + 1][1]) ** 2) for i in range(n)
        )
        if s < mn:
            mn = s
            bst = [0] + list(d)
    return mn, bst
