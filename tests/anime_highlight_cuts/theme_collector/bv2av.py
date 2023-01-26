

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def dec(x):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor


def enc(x):
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''.join(r)


def main():
    while True:
        av_bv = input("请输入BV或AV号,需要带上BV或AV前缀(输入q以退出):") + "  "
        head = str(av_bv[0]) + str(av_bv[1])
        av = ["av", "AV", "Av", "aV"]
        bv = ["bv", "BV", "Bv", "bV"]
        if av_bv == "q  " or av_bv == "Q  ":
            quit()
        elif head in av:
            print(enc(int(av_bv[2:-2])))
        elif head in bv:
            print("av", dec("BV" + av_bv[2:-2]), sep="")
        else:
            print("你的输入有误请重新输入")


main()
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
BV2AV/BV2AV.py at master · kuailett/BV2AV