import re


a = '第三回　　秋风野店书生笛,!'

b = re.sub('\W','m',a)

print(b)