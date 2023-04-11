from my_class import MyClass

x = int(input("数値入力:"))

#if
if x < 0:
    x = 0
    print("0未満でした")
elif x == 0:
    print("0でした")
elif x == 1:
    print("1でした")
else :
    print("0or1以外です")

#for
for i in range(10):
    print(i)

#list
list = ["test1"]
list.append("test2")
for item in list:
    print(item)

#open
with open("README.md","r") as file:
    data = file.read()
    print(data)

with open("README.md","a") as file:
    file.write("test1")
    print(data)

#Class読み込み
my_instance = MyClass("World")
my_instance.say_hello()

