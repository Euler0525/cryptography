import base64


s = "mTyqm7wjODkrNLcWl0eqO8K8gc1BPk1GNLgUpI=="
s1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
s2 = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0987654321/+"

ss = s.translate(str.maketrans(s2, s1))  # 还原编码表
print(base64.b64decode(ss).decode())


