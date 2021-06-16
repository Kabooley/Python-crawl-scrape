# 条件分岐
# インデント、スペースに気をつけましょう

# 論理演算子
# `and`や`or`を使う
a = 1
b = 1
# &&
print(a > 0 and b > 0)
# ||
print(a > 0 or b < 0)
# 以下はtypeerror
# print(a > 0 && b > 0)
# print(a > 0 || b < 0)


# In , Not

y = [1, 2, 3]
x = 1
if x in y:
    print('in')

# NotはC言語系の!である
if 100 not in y:
    print('not in')

# NOT recommended
# "aとbは等しくない"なら
if not a == b:
    print("not equal")

A = False
B = True
B = not A
print(B)


# 値が入っていないのかのチェック
# 判定が真になる
is_ok = True
# 他、0(0.0)じゃない数値、空じゃない配列（文字列）

# OK
if is_ok:
    print("OK")
else:
    print('No')

str = ""
# No
if str:
    print("OK")
else:
    print('No')

arr = []
# No
if arr:
    print("OK")
else:
    print('No')


# Noneを判定する方法(is)
# とにかくNoneであるかどうかを判定するときだけに`is`を使おうとのこと

is_empty = None
# NOT THIS
# if is_empty == None:
if is_empty is None:
    print('it is none')
else:
    print("it is not none")


print('-----------------------------------------')

# `is`と`==`の違い
test_list1 = [100, 200, 300]
test_list2= [100, 200, 300]
test_list3 = [100, 200, 300]

# `==`はオブジェクト同士が等価であるかの判定演算子
print(test_list1 == test_list2)     # True
print(test_list1 == test_list3)     # True

# `is`はオブジェクトのidを比較する演算子
# idとはPythonがオブジェクトを生成するときに内部的に割り振っている一意のid
print(test_list1 is test_list2)     # False
print(id(test_list1) is id(test_list2))     # False

# つまり、`==`は値の比較、`is`はまったく同じオブジェクトか？の比較である


