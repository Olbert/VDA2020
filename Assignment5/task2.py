import numpy as np
np.set_printoptions(precision=2)
# initial matrices
X2 = np.array(([[0, 0.12, 0.3, 1],
                [0.12, 0, 0.18, 0.88],
                [0.3, 0.18, 0, 0.71],
                [1, 0.88, 0.71, 0]]))

X = np.array(([0, 0.6, 0.2, 0.4],
               [0.6, 0, 0.4, 1],
               [0.2, 0.4, 0, 0.6],
               [0.4, 1, 0.6, 0]))

inp = np.array(([5, 7, 10, 8]),dtype=np.float)

# The shift
alpha = 0.5
print("Errors:")
for ind in range(1,4):
    # distances calculation
    dist = np.array((np.abs(inp[0] - inp),
                        np.abs(inp[1] - inp),
                        np.abs(inp[2] - inp),
                        np.abs(inp[3] - inp)))

    # Left part for absolute error
    J0 = 2 / (np.power(X[0], 2).sum() +
              np.power(X[1, 1:4], 2).sum() +
              np.power(X[2, 2:4], 2).sum() +
              (np.power(X[3, 3:4], 2).sum()))

    # Relative error calculation
    J = np.zeros(4, dtype=np.float)

    for i in range(0, 4):
        for k in range(0, 4):
            if i != k:
                # J[i] += ((dist[i, k] - X[i, k]) / np.power(X[i, k], 2)) * ((inp[i] - inp[k]) / dist[i, k])
                J[i] += (dist[i, k] - X[i, k]) * ((inp[i] - inp[k]) / dist[i, k])
                # print((dist[i, k], '-', X[i, k]), '*', ((inp[i] ,'-', inp[k]) ,'/', dist[i, k]))
    print(J)
    J = J*J0
    print(J)

    # Shift of dataK
    inp -= alpha * J
    print(inp)
print("Data:")
print(inp)

