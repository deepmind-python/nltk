from random import choice

def instruction2():
    print("你可以按下一個按鍵繼續玩。")

def instruction():
    print("您將要前往需要醫療用品的星球。")
    print("大部分的旅程時間，都在睡眠。")
    print("先交待電腦要分配多少能量給防護罩......")
    print("當醒來時，電腦將提供旅途中發生的報告。")
    instruction2()

i = input("需要顯示任務說明嗎？(y 或 n) ")
if i == "y":
	instruction()
	a = input()
	while a == "":
		instruction2()
		a = input("不可按Enter鍵！： ")

D = choice(range(100,800))
E = choice(range(400,410))
T = int(D/E + 100)

decoration_line = "<@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>"

print(decoration_line)
print("這星球距離地球"+str(D)+"光年。")
print("你總共有"+str(E)+"個單位的能量")
print("及剩下"+str(T)+"天的時間。")
print(decoration_line, "\n")



