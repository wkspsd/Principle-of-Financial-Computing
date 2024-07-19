import math
import numpy as np
import sys
np.random.seed(seed=1)


def calAmericanStyleAsianPuts(Spot, sigma, n, m, Strike, r, nT):

    T = nT / n
    priceMatrix = np.zeros((m, n))
    for i in range(m):
        priceMatrix[i, :] = Spot * np.exp(
            np.cumsum(
                (r - 0.5 * sigma ** 2) * T
                + (sigma * math.sqrt(T) * np.random.normal(0, 1, n))
            )
        )


    meanMatrix = np.concatenate((np.reshape(priceMatrix[:, 0], (m, -1)), np.zeros((m, n - 1))), axis=1)
    for i in range(1, n):
        meanMatrix[:, i] = np.mean(priceMatrix[:, :i + 1], axis=1)

    diffMatrix = np.maximum(0, Strike - meanMatrix)
    X = np.where(diffMatrix > 0, priceMatrix, 0)
    Xsh = X[:, :-1]
    Y1 = diffMatrix * math.exp(-r * T)
    Y2 = np.concatenate((np.zeros((m, n - 1)), np.vstack(Y1[:, n - 1])), axis=1)
    CV = np.zeros((m, n - 1))

    # iteration
    for i in range(n - 2, -1, -1):
        degree = 5
        reg1 = np.polyfit(Xsh[:, i], Y2[:, i + 1], degree)
        for d in range(degree + 1):
            CV[:, i] += reg1[-d - 1] * Xsh[:, i] ** d


        CV[:, i] = np.nan_to_num(CV[:, i])
        Y2[:, i] = np.where(diffMatrix[:, i] > CV[:, i], Y1[:, i], Y2[:, i + 1] * math.exp(-r * T))

    CV = np.nan_to_num(CV)
    CVp = np.concatenate((CV, np.zeros((m, 1))), axis=1)
    pofMatrix = np.where(CVp > diffMatrix, 0, diffMatrix)

    # first value row
    M = np.zeros((m,n))
    for i in range(m):
        M[i, :] = np.cumsum(pofMatrix[i, :])
    M2 = np.concatenate((np.zeros((m, 1)), M[:, :-1]), axis=1)
    fpofMatrix = np.zeros((m, n))
    for i in range(pofMatrix.shape[1]):
        fpofMatrix[:, i] = np.where(M2[:, i] > 0, 0, pofMatrix[:, i])

    dfpofMatrix = np.zeros((m, n))
    for i in range(n):
        dfpofMatrix[:, i] = fpofMatrix[:, i] * math.exp(-T * r * (i + 1))
    PRICE = np.mean(np.sum(dfpofMatrix, axis=1))

    return PRICE


def calculate_delta(Spot, sigma, n, m, Strike, r, nT):
    Spot_up = 1.01 * Spot
    Spot_down = 0.99 * Spot

    price_up = calAmericanStyleAsianPuts(Spot_up, sigma, n, m, Strike, r, nT)
    price_down = calAmericanStyleAsianPuts(Spot_down, sigma, n, m, Strike, r, nT)

    delta = (price_up - price_down) / (Spot_up - Spot_down)
    return delta


if __name__ == "__main__":
    S, X, T, r, s, n, N = map(float, sys.argv[1:])
    T = int(T)
    T = T / 365
    n = int(n)
    N = int(N)

    price = calAmericanStyleAsianPuts(Spot = S, sigma = s, n = n, m = N, Strike = X, r = r, nT = T)
    delta = calculate_delta(S, s, n, N, X, r, T) 

    print("{:.6f}, {:.6f}".format(price, delta))
   