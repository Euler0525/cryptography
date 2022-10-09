# -*- coding: utf-8 -*-
def shiftRows(m: list) -> list:
    for i in range(4):
        for j in range(i):
            m[i].insert(4, m[i][0])
            m[i].remove(m[i][0])

    return m
