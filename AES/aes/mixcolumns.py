# -*- coding: utf-8 -*-
def xorM(x: int, y: int) -> int:
    if x == 0x01:
        return y
    elif x == 0x02:
        if y < 128:
            return y << 1
        else:
            return ((y << 1) % 256) ^ 0x1b
    else:
        return xorM(0x02, y) ^ y


def oneColumn(m: list) -> list:
    lst = [[0x02, 0x03, 0x01, 0x01], [0x01, 0x02, 0x03, 0x01], [0x01, 0x01, 0x02, 0x03], [0x03, 0x01, 0x01, 0x02]]
    r1 = xorM(lst[0][0], m[0]) ^ xorM(lst[0][1], m[1]) ^ xorM(lst[0][2], m[2]) ^ xorM(lst[0][3], m[3])
    r2 = xorM(lst[1][0], m[0]) ^ xorM(lst[1][1], m[1]) ^ xorM(lst[1][2], m[2]) ^ xorM(lst[1][3], m[3])
    r3 = xorM(lst[2][0], m[0]) ^ xorM(lst[2][1], m[1]) ^ xorM(lst[2][2], m[2]) ^ xorM(lst[2][3], m[3])
    r4 = xorM(lst[3][0], m[0]) ^ xorM(lst[3][1], m[1]) ^ xorM(lst[3][2], m[2]) ^ xorM(lst[3][3], m[3])
    return [hex(r1), hex(r2), hex(r3), hex(r4)]


def mixColumns(grid: list) -> list:
    tmp = [[] for _ in range(4)]
    result = [[] for _ in range(4)]
    for i in range(4):
        tmp[i] = [eval(grid[j][i]) for j in range(4)]
        result[i] = oneColumn(tmp[i])
    return list(map(list, zip(*result)))
