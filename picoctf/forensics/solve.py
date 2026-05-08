import base64

data = base64.b64decode("SFxRWXJicU1KBVVDAmlUBVRZbUIBQQREZwJXD1VQBAcBSA==")

key = b'85261676'
flag = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

print(flag.decode())

