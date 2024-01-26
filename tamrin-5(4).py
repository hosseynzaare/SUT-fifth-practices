import re
def find(n, text, word2):
    words = text.split()
    word3 = word2.lower()
    lst = []
    for word in words:
        word4 = word.lower()
        while len(word3) > len(word4):
            word4 += "_"
        while len(word4) > len(word3):
            word3 += "_"
        distance = 0
        for i in range(len(word3)):
            if word3[i]!=word4[i]:
                distance+=1
        if distance <= n:
            lst.append(word)
    return lst

n = int(input())
text = input()[:-1]
text = re.sub(r"[،:؛.؟!٬٫]+","",text)
word2 = input()
output = find(n, text, word2)
for i in output:
    print(i)
