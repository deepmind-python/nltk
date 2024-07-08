from random import choice

bird_snake = """                                  
                                          ___     _,-----._                /^\/^\                                         
                    _________          ,-'   `.--'   __    `.            _| O | O|                                    
                _,-'--  __,--`-._     ,'  ,(o);___,-'  `-----|  \/     /)     \_/ \                                   
             ,-'  -- ,-'         `._,-'  `'~~``.__,-'~~~~~`-.;   \____|__________/  \                                 
           ,'---  --:             ;     ,' ~`' ;            `           \_______      \                               
        _,-.------  `._            :   ,'   _,-'                                `\     \                 \            
     ,-'    ~~~~~~~`.__`._        ;  _,' _,'                                      |     |                  \          
     ;---'~~~~~~~~_,----.___     ,(   _,'                                        /      /                    \        
    ,'-- __,---'~~~/ _,-._  `----'_;-'                                          /     /                       \\      
  ,' `,-'`.  (    / /____ `------'                                            /      /                         \ \    
  `-'~    ;  :  ,{_______`--.__`.`-.                                         /     /                            \  \  
                                                                           /     /             _----_            \   \

                                                                         (      (        _-)    _--_    )-_     _/   |
                                                                          \      )-____-)    _-)    )-_    )-_-)    / 
                                                                            )-_           _-)          )-_       _-)  
                                                                               )--______-)                )-___-)     





  """

print(bird_snake)

coordinate_numbers = range(1, 11)
space_snake_coordinate = choice(coordinate_numbers)
big_bird_coordinate = choice(coordinate_numbers)
while big_bird_coordinate == space_snake_coordinate:
    new_coordinate = choice(coordinate_numbers)
    big_bird_coordinate = new_coordinate

print("人工巨鳥正在尋找太空怪蛇。")
print("總共有", len(coordinate_numbers), "個座標位置。")

while True:
    print("人工巨鳥目前所在位置:", big_bird_coordinate)
    print("太空怪蛇目前所在位置:", space_snake_coordinate)

    if (big_bird_coordinate == space_snake_coordinate - 1 or
            big_bird_coordinate == space_snake_coordinate + 1):
        print("正察覺到太空怪蛇在附近...")

    print("請輸入人工巨鳥要去的位置！")
    big_bird_coordinate = input(">>>")
    big_bird_coordinate = int(big_bird_coordinate)
    if big_bird_coordinate == space_snake_coordinate:
        print("抓到太空怪蛇了!")
        print("太空怪蛇被吃掉了!")
        print("現在您可以無憂無慮地駕駛太空船了!")
        break
