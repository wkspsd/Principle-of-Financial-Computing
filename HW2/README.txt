R12944061 陳光遠

How to execute:

Just type:"python R12944061_HW_2.py [S] [X] [r] [s] [T] [m] [E]" to run the code


Format of input.txt:
S (stock price)
X (strike price)
r (continuously compounded annual interest rate)
s (annual volatility)
T (time to maturity in days, which is an integer and also an exercise date)
m (number of periods per day for the tree, an integer)
E (early exercise dates from now, a list of integers)


example:
input.txt:
100
110
0.03
0.3
60
5
[10, 20, 30, 40, 50]

The program should output:
11.248139
BUT BUT！
My program will output:
11.248121

I don't konw what's wrong.
Thanks!