# -*- coding: utf-8 -*-

def factorial(n):
    if n==1:
        return 1
    else:
        return n * factorial(n-1)

n=int(input("Numero de Factorial: "))
print(factorial(n))
