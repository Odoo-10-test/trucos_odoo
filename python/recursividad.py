# -*- coding: utf-8 -*-

def sumatoria(num):
    if num==1:
        return 1
    else:
        return num + sumatoria(num-1)

num=int(input("Numero de Sumatoria: "))
print(sumatoria(num))
