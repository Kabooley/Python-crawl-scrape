s1 = ("Hi, " * 3 + "Michael")
s2 = ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa""bbbbbbbbbbbbbbbbbbbbbbbbbbb")
print(s1)
print(s2)

print("###########################")
# indexアクセス
word = "Pythonthon"

print(word[0])
print(word[1])
# 末尾を返す
print(word[-1])
print(word[0:2])
print(word[2:5])
print(word[2:])
""" output
P
y
n
Py
tho
thonthon
"""

print("###########################")
# stringメソッド
mike = "My name is Mike. You all know me!"
# 長さ
print(len(mike))
is_start = mike.startswith("My")
# true
print(is_start)
is_start = mike.startswith("Mike")
# false
print(is_start)


print(mike.find("name"))
print(mike.rfind("name"))
print(mike.capitalize())
print(mike.upper())
print(mike.lower())
print(mike.replace("Mike", "Jessica"))

print("###########################")
# 文字列の代入

# String.format("")で文字列中の{}へ任意の文字列を代入することができる
print('a is {}'.format("a"))
print('a is {}'.format("test"))
# 複数にも対応
print('a is {} {} {}' .format(1,2,3))
# 順番のコントロール
print('a is {0} {1} {2}' .format(11,22,33))
print('a is {2} {1} {0}' .format(11,22,33))
# 引数の指定
print("My name is {name} {family}. ".format(name="Mike", family="Shinoda"))



print("###########################")
# f-strings
# formatに代わる文字列メソッド。format()と比較してコードが短くなる
a = "a"
# print('a is {}'.format("a"))の代わり
print(f"a is {a}")

print("My name is {name} {family}. ".format(name="Mike", family="Shinoda"))
name = "Mike"
family = "Shionoda"
print(f"My name is {name} {family}.")

print("###########################")
print("###########################")