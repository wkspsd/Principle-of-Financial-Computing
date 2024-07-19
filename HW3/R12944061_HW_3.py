import sys
import math


class UpAndOutBarrierPut:
    def __init__(self, S, X, r, s, T, H, n):
        # Initialization function, set initial parameters
        self.S = S
        self.X = X
        self.r = r
        self.s = s
        self.T = T / 365  # Convert time to years
        self.H = H
        self.n = int(n)

        # Calculate time step, up factor, down factor, and probability of up movement
        self.dt = self.T / self.n if self.n != 0 else 0
        self.u = math.exp(self.s * math.sqrt(self.dt))
        self.d = 1 / self.u
        self.p = (math.exp(self.r * self.dt) - self.d) / (self.u - self.d) if self.n != 0 else 0

    def price(self):
        # Check if the number of time steps is 0, if so, calculate and return the option price at the initial time point directly
        if self.n == 0:
            return max(0, self.X - self.S) if self.S < self.H else 0
        
        # Initialize matrices for stock prices and option prices
        prices = [[0.0 for _ in range(i + 1)] for i in range(self.n + 1)]
        for j in range(self.n + 1):
            for i in range(j + 1):
                # Fill the matrix of stock prices
                prices[j][i] = self.S * (self.u ** (j - i)) * (self.d ** i)

        put_prices = [[0.0 for _ in range(i + 1)] for i in range(self.n + 1)]
        for i in range(self.n + 1):
            put_prices[self.n][i] = max(0, self.X - prices[self.n][i])

        # Use backward induction to calculate option prices
        for j in range(self.n - 1, -1, -1):
            for i in range(j + 1):
                # Calculate option prices based on trinomial tree
                put_prices[j][i] = (
                    (1 + self.r * self.dt) ** -1 * (
                        self.p * put_prices[j + 1][i] +
                        (1 - self.p) * put_prices[j + 1][i + 1]
                    )
                )
                # If the upper barrier is reached, set option price to 0
                if prices[j][i] >= self.H:
                    put_prices[j][i] = 0.0

        return put_prices[0][0]


def main():
    S, X, r, s, T, H, n = map(float, sys.argv[1:])
    option = UpAndOutBarrierPut(S, X, r, s, T, H, n)
    print(round(option.price(), 6))


if __name__ == "__main__":
    main()