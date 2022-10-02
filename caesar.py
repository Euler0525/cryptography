# -*- coding: utf-8 -*-

def encryption(plaintext: str, key: int) -> str:
    """Caesar encryption"""
    cipher_text = ""
    for p in plaintext:
        if ord("a") <= ord(p) <= ord("z"):
            cipher_text += chr((ord(p) + key - ord("a")) % 26 + ord("a"))
        elif ord("A") <= ord(p) <= ord("Z"):
            cipher_text += chr((ord(p) + key - ord("A")) % 26 + ord("A"))
        else:
            cipher_text += p

    return cipher_text


def descryption(ciphertext: str):
    """Caesar decryption"""
    for key in range(0, 26):
        plain_text = ""
        for c in ciphertext:
            if ord("a") <= ord(c) <= ord("z"):
                plain_text += chr((ord(c) - key - ord("a")) % 26 + ord("a"))
            elif ord("A") <= ord(c) <= ord("Z"):
                plain_text += chr((ord(c) - key - ord("A")) % 26 + ord("A"))
            else:
                plain_text += c
        print("key={0:2}: ".format(key) + plain_text)
