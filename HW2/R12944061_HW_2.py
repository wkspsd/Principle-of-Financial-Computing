import sys
import math


def Bermuda_put(S, X, r, s, T, m, E):
    mature = T
    holiday = 0
    trading = mature - holiday

    T = int(trading * m)
    N = int(mature * m)
    R = math.exp(r * (1 / (365 * m)))
    u = math.exp(s * ((1 / (365 * m)) ** (0.5)))
    d = 1 / u
    q = (R - d) / (u - d)

    option_price = []
    stock_price = []

    for i in range(0, T + 1):
        stock_price.append(S * u ** (T - i) * d ** i)
        option_price.append(max(0, X - stock_price[i]))

    for i in range(0, N):
        day = i / m  
        for j in range(0, T):
            if int(day) in E or int(day) == mature:  
                option_price[j] = max((option_price[j] * q + option_price[j + 1] * (1 - q)) / R,
                                      X - stock_price[j])
            else:
                option_price[j] = (option_price[j] * q + option_price[j + 1] * (1 - q)) / R
            stock_price[j] = stock_price[j] / u  

    return option_price[0]


if __name__ == '__main__':
    args = [float(arg) for arg in sys.argv[1:]]
    S, X, r, s, T, m = args[:6]
    E = [int(arg) for arg in args[6:]]
    put_price = Bermuda_put(S, X, r, s, T, m, E)
    print("{:.6f}".format(put_price))