# -*- coding: utf-8 -*-
import destable
import re

class FileProcess(object):
    def __init__(self, filename: str):
        self.file = filename

    def writeFile(self, message: str):
        """Writes the ciphertext to a text file"""
        f = open(self.file, "w", encoding="utf-8")
        f.write(message)
        f.close()

    def readFile(self) -> str:
        """Obtain the ciphertext in the text file"""
        f = open(self.file, "r", encoding="utf-8")
        message = f.read()
        f.close()
        return message


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

    @ staticmethod
    def bin2str(bin_text: str) -> str:
        pass




