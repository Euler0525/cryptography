class Encryption(object):
    def __init__(self, plain_text: str, key: str):
        self.plain_text = plain_text
        self.key = key

    def caesarPassword(self) -> str:
        """Caesar encryption"""
        cipher_text = ""
        for p in self.plain_text:
            if ord("a") <= ord(p) <= ord("z"):
                cipher_text += chr((ord(p) + eval(self.key) - ord("a")) % 26 + ord("a"))
            elif ord("A") <= ord(p) <= ord("Z"):
                cipher_text += chr((ord(p) + eval(self.key) - ord("A")) % 26 + ord("A"))
            else:
                cipher_text += p

        return cipher_text


class Decryption(object):
    def __init__(self, cipher_text: str, key: str):
        self.cipher_text = cipher_text
        self.key = key

    def caesarPassword(self) -> str:
        """Caesar decryption"""
        plain_text = ""
        for c in self.cipher_text:
            if ord("a") <= ord(c) <= ord("z"):
                plain_text += chr((ord(c) - eval(self.key) - ord("a")) % 26 + ord("a"))
            elif ord("A") <= ord(c) <= ord("Z"):
                plain_text += chr((ord(c) - eval(self.key) - ord("A")) % 26 + ord("A"))
            else:
                plain_text += c

        return plain_text

