# -*- coding: utf-8 -*-
import re
import numpy as np


class VirginiaEncryption(object):
    def __init__(self, plaintext: str, key: str):
        self.plaintext = plaintext
        self.key = key

    def getText(self) -> str:
        """Remove non-alphabetic characters from the text"""
        return re.sub("[^a-z]", "", self.plaintext.lower())

    def encryption(self) -> str:
        length = len(self.key)
        ciphertext = ""
        i = 0
        for p in self.getText():
            i = i % length
            ciphertext += chr((ord(p) + ord(self.key[i]) - 2 * ord("a")) % 26 + ord("a"))
            i += 1

        return ciphertext


class VirginiaDecryption(object):
    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext
        self.cipher_len = len(ciphertext)

    def getText(self) -> str:
        """Remove non-alphabetic characters from the text"""
        return re.sub("[^a-z]]", "", self.ciphertext)

    @staticmethod
    def getIc(text) -> float:
        """calculate the Ic of the text"""
        count = [0 for _ in range(26)]
        length = len(text)
        ic = 0.0
        for i in range(length):
            count[ord(text[i]) - ord("a")] += 1
        for i in range(26):
            ic += (count[i] * (count[i] - 1)) / (length * (length - 1))

        return ic

    def groupIc(self, key_len: int) -> np.ndarray:
        """When the key length is key_len, return the average Ic"""
        groups = ["" for _ in range(key_len)]
        for i in range(self.cipher_len):
            index = i % key_len
            groups[index] += self.ciphertext[i]
        ics = [0 for _ in range(key_len)]
        for i in range(key_len):
            ics[i] = self.getIc(groups[i])

        return np.mean(ics)

    """
    Obtain the key length: 
    When the key length is i, the coincidence index of each group is calculated, 
    and the key length closest to 0.065 is the corresponding key length
    """

    def getKeyLength(self) -> int:
        """determine the key length"""
        key_len = 0
        min_ic = 1.0
        for i in range(1, 10):
            tmp = self.groupIc(i)
            if abs(tmp - 0.065) < min_ic:
                min_ic = abs(tmp - 0.065)
                key_len = i

        return key_len

    @staticmethod
    def getMg(s1: str, s2: str, offset: int) -> int:
        """calculate the coincidence index"""
        count1 = [0 for _ in range(26)]
        count2 = [0 for _ in range(26)]
        l1 = len(s1)
        l2 = len(s2)
        mg = 0
        for i in range(l1):
            count1[ord(s1[i]) - ord("a")] += 1
        for j in range(l2):
            count2[(ord(s2[j]) - ord("a") + offset + 26) % 26] += 1
        for k in range(26):
            mg += count1[k] * count2[k] / (l1 * l2)

        return mg

    def getOffset(self, s1: str, s2: str) -> int:
        """The optimal coincidence index of two stringsand return the most appropriate offset"""
        offset = 0  # Relative to the first group
        minn = 100
        tmp = [0.0 for _ in range(26)]
        for i in range(26):
            tmp[i] = self.getMg(s1, s2, i)
            if (abs(tmp[i] - 0.065)) < minn:
                minn = abs(tmp[i] - 0.065)
                offset = i
        return offset  # Offset when Mg and 0.065 are closest

    def relativeOffset(self) -> list:
        cipher_len = len(self.ciphertext)
        key_len = self.getKeyLength()
        groups = ["" for _ in range(key_len)]
        offsets = [0 for _ in range(key_len)]
        # group
        for i in range(cipher_len):
            index = i % key_len
            groups[index] += self.ciphertext[i]
        for j in range(1, key_len):
            offsets[j] = self.getOffset(groups[0], groups[j])

        return offsets

    """
    When the key length m is determined, the cipher is divided into M groups, and each group is a single table substitution password.
    The first group has 26 kinds of offsets, assuming that the offset of the first group is 0, calculate the relative offsets of the second to last group and the first group and the corresponding mutual coincidence index, determine each character of the key, and list the 26 kinds of offsets
    """

    def getKey(self, k: int) -> list:
        s = self.relativeOffset()
        key_len = self.getKeyLength()
        key = ["" for _ in range(key_len)]
        for i in range(key_len):
            s[i] = k - s[i]
            key[i] = chr((s[i] + 26) % 26 + ord("a"))
        key = "".join(key)
        print("偏移量:{0: >2}-密钥为\"{1}\"时, 部分明文: ".format(k, key), end=" ")
        return s

    def getPlain(self, key: str) -> str:
        plaintext = ""
        key_len = self.getKeyLength()
        i = 0
        while i < self.cipher_len:
            for j in range(key_len):
                plaintext += chr((ord(self.ciphertext[i]) - ord("a") - key[j] + 26) % 26 + ord("a"))
                i += 1
                if i == self.cipher_len:
                    break
        return plaintext

    def decryption(self) -> str:
        s = self.relativeOffset()
        for k in range(26):
            tmp = s.copy()
            tmp = self.getKey(k)
            plaintext = self.getPlain(tmp)
            print(plaintext[0:50])
            print()
        print("参考以上结果，确定第一个子串的偏移量:", end="")
        k = int(input())
        s = self.getKey(k)
        plaintext = self.getPlain(s)
        print("明文".center(100, "-"))
        print(plaintext)
        print("明文".center(100, "-"))
        return plaintext
