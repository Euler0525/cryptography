# -*- coding: utf-8 -*-
import re
from destable import *


class DESEncrypt(object):
    def __init__(self, plain: str, key: str):
        self.plain = plain
        self.key = key

    @staticmethod
    def str2bin(str_text: str) -> str:
        bin_text = str()
        for c in str_text:
            tmp = str(bin(ord(c)))[2:]
            while len(tmp) < 8:
                tmp = "0" + tmp
            bin_text += tmp

        return bin_text

    @staticmethod
    def bin2str(bin_text: str) -> str:
        str_text = str()
        tmp = re.findall(r".{8}", bin_text)
        for i in tmp:
            str_text += chr(int(i, 2))

        return str_text

    def strXor(self, s1: str, s2: str) -> str:
        result = ""
        for i in range(len(s1)):
            x = int(s1[i], 10) ^ int(s2[i], 10)
            if x == 1:
                result += "1"
            else:
                result += "0"

        return result

    def ipChange(s):
        result = ""
        for i in IP_TABLE:
            result += s[i - 1]

        return result

    def ipReChange(self, s):
        result = ""
        for i in IP_RE_TABLE:
            result += s[i - 1]
        return result

    def eReplace(self, s):
        result = ""
        for i in E:
            result += s[i - 1]
        return result

    def leftTurn(self, s: str, num: int):
        return s[num:] + s[0:num]

    def pc1Replace(self, key: str):
        result = ""
        for i in PC_1:
            result += key[i - 1]

        return result

    def pc2Replace(self, key: str):
        result = ""
        for i in PC_2:
            result += key[i - 1]

        return result

    def sBox(self, s):
        result = ""
        round = 0
        for i in range(0, len(s), 6)
            now_str = s[i: i + 6]
            row = int(now_str[0] + now_str[5], 2)
            column = int(now_str[1:5], 2)
            num = bin(S[round][row * 16 + column])[2:]
            for _ in range(4 - len(num)):
                num = "0" + num
            result += num
            round += 1

        return result

    def pBox(self, s):
        result = ""
        for i in P:
            result += s[i - 1]
        return result

    def func(self, s, key):
        first = self.eReplace(s)
        second = self.strXor(first, key)
        third = self.sBox(second)
        last = self.pBox(third)

        return last

    def getKeys(self, key):
        key_list = []
        divide = self.pc1Replace(key)
        key_c0 = divide[0:28]
        key_d0 = divide[28:]
        for i in SHIFT:
            key_c1 = self.leftTurn(key_c0, i)
            key_d1 = self.leftTurn(key_d0, i)
            result = self.pc2Replace(key_c1 + key_d1)
            key_list.append(result)

        return key_list
