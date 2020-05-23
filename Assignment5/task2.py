import numpy as np

X2 = np.array(([[0, 0.12, 0.3, 1],
                [0.12, 0, 0.18, 0.88],
                [0.3, 0.18, 0, 0.71],
                [1, 0.88, 0.71, 0]]))

X = np.array(([0, 0.6, 0.2, 0.4],
               [0.6, 0, 0.4, 1],
               [0.2, 0.4, 0, 0.6],
               [0.4, 1, 0.6, 0]))

inp = np.array(([5, 7, 10, 8]),dtype=np.float)

alpha = 0.01

for ind in range(1,4):
    dist = np.array((np.abs(inp[0] - inp),
                        np.abs(inp[1] - inp),
                        np.abs(inp[2] - inp),
                        np.abs(inp[3] - inp)))

    J0 = 2 / (np.power(X[0], 2).sum() +
              np.power(X[1, 1:4], 2).sum() +
              np.power(X[2, 2:4], 2).sum() +
              (np.power(X[3, 3:4], 2).sum()))

    J = np.zeros(4, dtype=np.float)

    for i in range(0, 4):
        for k in range(0, 4):
            if i != k:
                J[i] += ((dist[i, k] - X[i, k]) / np.power(X[i, k], 2)) * ((inp[i] - inp[k]) / dist[i, k])

    print(J)

    print("\n")

    inp -= alpha * J

print(inp)

