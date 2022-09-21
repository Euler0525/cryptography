# 维吉尼亚密码（密码学导论作业）

## 加密

### 原理

维吉尼亚密码是一种多表代换密码，密码体制如下：

> 设$m$是一个正整数，定义$\mathcal{P}=\mathcal{C}=\mathcal{K}=(Z_{26})^m$，对任意的密钥$K=(k_1,k_2,\cdots,k_m)$，则有
> $$
> e_K(x_1,x_2,\cdots,x_m)=(x_1+k_1,x_2+k_2,\cdots,x_m+k_m)\\
> d_K(y_1,y_2,\cdots,y_m)=(y_1-k_1,y_2-k_2,\cdots,y_m-k_m)
> $$

### 代码实现

读取`plaintext.txt`中的文本作为明文，输入密钥，将密文存储到`cipher.txt`文件中。

```python
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

```

## 解密

### 原理分析

维吉尼亚密码是多表代换密码，相通的明文可能被加密成不同的密文，因此不能使用词频分析来破解维吉尼亚密码。

1. 首先需要利用重合指数法确定密钥的长度，已知随机的英文文本中$I_c=0.0385$，一段有意义的英文文本中$I_c=0.065$，设待破解的密文中$I'_c=\displaystyle\sum^n_{i=1}\dfrac{f_i f_{i}-1}{l(l-1)}$，若$I'_C$与$0.065$相差较大，则确定是多表代换；

2. 当密文长度分别取从1到10时，求出各自的重合指数$I_c$，各个重合指数中最接近0.065对应的密钥长度即为所求；
3. 分别求出互重合指数$M_g$，和$0.065$接近的即为密钥；

4. 分别列出每种密钥对应的偏移量和明文，找到符合英语语法和语义的文本，选择对应的偏移量；

### 代码实现

读取`cipher.txt`中的密文文本，列出各个偏移量对应的部分明文，选择符合英文语法和语义的文本输出。

```python
# -*- coding: utf-8 -*-
import numpy as np
import re


def getText(cipher: str) -> str:
    """Remove the non-lowercase letters"""
    return re.sub("[^a-z]", "", cipher)


def getIc(cipher: str) -> float:
    """Calculate the Ic of the ciphertext"""
    count = [0 for _ in range(26)]  # Count the frequency of each letter
    length = len(cipher)
    ic = float()
    for i in range(len(cipher)):
        count[ord(cipher[i]) - ord("a")] += 1
    for i in range(26):
        ic += (count[i] * (count[i] - 1)) / (length * (length - 1))

    return ic


def listKeyLen(cipher: str, key_len: int) -> np.ndarray:
    """When the key length is key_len, return the average Ic"""
    length = len(cipher)
    # Group the ciphertext
    groups = ["" for _ in range(key_len)]
    for i in range(length):
        index = i % key_len
        groups[index] += cipher[i]
    # Calculate the Ic of each group
    ics = [0 for _ in range(key_len)]
    for i in range(key_len):
        ics[i] = getIc(groups[i])

    return np.mean(ics)


def detemineLength(cipher: str) -> int:
    """Determine the most likely key length"""
    key_len = 0
    minic = 1.0  # The minimum difference of coincidence indices
    for i in range(1, 10):
        tmp = listKeyLen(cipher, i)
        if abs(tmp - 0.065) < minic:
            minic = abs(tmp - 0.065)
            key_len = i

    return key_len


def getMg(s1: str, s2: str, offset: int) -> int:
    """Calculate the coincidence index"""
    count1 = [0 for _ in range(26)]
    count2 = [0 for _ in range(26)]
    l1 = len(s1)
    l2 = len(s2)
    mg = 0
    for i in range(l1):
        count1[ord(s1[i]) - ord("a")] += 1
    for i in range(l2):
        count2[(ord(s2[i]) - ord("a") + offset + 26) % 26] += 1
    for i in range(26):
        mg += count1[i] * count2[i] / (l1 * l2)
    return mg


def calcOffset(s1: str, s2: str) -> int:
    """The optimal coincidence index of two strings"""
    offset = 0
    minn = 100
    tmp = [0.0 for _ in range(26)]
    for i in range(26):
        tmp[i] = getMg(s1, s2, i)
        if abs(tmp[i] - 0.065) < minn:
            minn = abs(tmp[i] - 0.065)
            offset = i
    return offset


def relativeOffset(cipher: str, key_len: int) -> list:
    """Group and calculate the optimal relative offset of each group from the first group"""
    groups = ["" for _ in range(key_len)]
    mgs = [0 for _ in range(key_len)]
    offsets = [0 for _ in range(key_len)]
    for i in range(len(cipher)):  # Group the ciphertext
        index = i % key_len
        groups[index] += cipher[i]
    for i in range(1, key_len):
        offsets[i] = calcOffset(groups[0], groups[i])  # s[i] = k[1]-k[i+1]
        mgs[i] = getMg(groups[0], groups[i], offsets[i])  # mgs[i] = mgs(1,i+1)

    return offsets


def getKey(key_len: int, s: list, k: int) -> str:
    key = ["" for _ in range(key_len)]
    for i in range(key_len):
        s[i] = k - s[i]  # k2=k1-n
        key[i] = chr((s[i] + 26) % 26 + ord("a"))
    print("偏移量:{0: >2}-密钥为{1}时, 部分密文: ".format(k, key))
    return s


def decrypt(cipher: str, key_len: int, key: str) -> str:
    """Decryption"""
    plain = str()
    i = 0
    while i < len(cipher):
        for j in range(key_len):
            plain += chr((ord(cipher[i]) - ord("a") - key[j] + 26) % 26 + ord("a"))
            i += 1
            if i == len(cipher):
                break
    return plain


def main():
    f = open("cipher.txt", "r")
    fi = f.read()
    f.close()
    cipher_text = getText(fi)
    key_len = detemineLength(cipher_text)
    s = relativeOffset(cipher_text, key_len)
    for i in range(26):
        tmp = s.copy()
        tmp = getKey(key_len, tmp, i)
        plain = decrypt(cipher_text, key_len, tmp)
        print(plain[0: 50])
        print()
    print("参考以上结果，确定第一个子串的偏移量:", end="")
    k = int(input())
    s = getKey(key_len, s, k)
    plain = decrypt(cipher_text, key_len, s)

    print("明文".center(100, "-"))
    print(plain)
    print("明文".center(100, "-"))


if __name__ == "__main__":
    main()

```

