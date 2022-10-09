# -*- coding: utf-8 -*-
from .subbytes import *
from copy import deepcopy


def rotWord(m: list) -> list:
    tmp = deepcopy(m)
    tmp.insert(len(m), m[0])
    tmp.remove(m[0])

    return tmp


def xor(l1: list, l2: list) -> list:
    result = []
    for i in range(4):
        if isinstance(l1[i], str):
            l1[i] = eval(l1[i])
        if isinstance(l2[i], str):
            l2[i] = eval(l2[i])
        result.append(hex(l1[i] ^ l2[i]))

    return result


def genRoundKey(key: list, round: int) -> list:
    w = []
    if round == 0:
        return key
    for j in range(4 * (round - 1), 4 * (round - 1) + 4):
        w.append([key[i][j] for i in range(4)])

    for i in range(4 * round, 4 * round + 4):
        if i % 4 != 0:
            w.append(xor(w[i - 4], w[i - 1]))
        else:
            w.append(xor(w[i - 4], xor([0x01, 0x0, 0x0, 0x0], subByte(rotWord(w[i - 1])))))
    return w[4:]


def addRoundKey(key: list, plain: list, round: int) -> list:
    key = genRoundKey(key, round)
    if round != 0:
        key = list(map(list, zip(*key)))
    result = []
    for i in range(4):
        result.append(xor(plain[i], key[i]))

    return result
