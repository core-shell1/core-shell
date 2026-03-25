import sys
src = r'C:\Users\lian1\Documents\Work\LAINCP\projects\소상공인_영업툴\영업타겟-수집\main_v2.py'
dst = r'C:\Users\lian1\Documents\Work\LAINCP\projects\소상공인_영업툴\영업타겟-수집\test_yangju.py'
with open(src, 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('REGION = "\ud3ec\ucc9c"', 'REGION = "\uc591\uc8fc"')
with open(dst, 'w', encoding='utf-8') as f:
    f.write(code)
print("OK")
