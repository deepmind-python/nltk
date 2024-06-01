from random import choice

def success():
    print("成功起飛！")

def delay():
    print("安全機制開始運作。")
    print("外星人將抓到你！")

def fail():
    print("起飛失敗")
    print("外星人將抓到你！")

print("飛碟起飛")

G = choice(range(1, 21))
W = choice(range(1, 41))

R = G*W
print(R)

for c in range(3):
    F = input("請輸入起飛動力:")
    if int(F) > R:
        print("太大了")
        if c == 2:
            delay()
    elif int(F) < R:
        print("太小了")
        if c == 2:
            fail()
    elif int(F) == R:
        success()
        break


            
    
