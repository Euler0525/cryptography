import re


def getText(in_file: str) -> str:
    with open(in_file, "r", encoding="utf-8") as f:
        return re.sub("[^a-z]", "", f.read().lower())


def encrypt(key: str, plain: str, out_filename="cipher.txt"):
    length = len(key)
    i = 0
    result = str()
    for ch in plain:
        i = i % length
        result += chr((ord(key[i]) - 2 * ord("a") + ord(ch)) % 26 + ord("a"))
        i += 1

    out_file = open(out_filename, "w")
    out_file.write(result)
    out_file.close()


if __name__ == "__main__":
    k = input("Please enter the key: ")
    encrypt(k, getText("plaintext.txt"))
