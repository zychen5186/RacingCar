#5:160->120 2:200->160

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        | 12 | 14 | 13 |
        | 10 |    | 11 |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        if scene_info.__contains__("coins"):
            self.coins_pos = scene_info["coins"]

        def check_grid():#看哪裡可以走
            grid = set()#grid存不可走的方向
            speed_ahead = 100
            speed_front_ahead = 100
            speed_behind_left = 0
            speed_behind_right = 0
            if self.car_lane == 0: # 在第一車道
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_lane == 8: # 在第九車道
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no: #自己除外的其他車子
                    x = self.lanes[self.car_lane] - car["pos"][0] #x relative position 以車道中心為基準
                    x_self = self.car_pos[0] - car["pos"][0] # x relative position以車自身為基準，
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    # if(x_self < -35 and x_self > -105):
                    #     if y > 100 and y < 160: #右前有車
                    #         grid.add(3)
                    # if(x_self > 35 and x_self < 105):
                    #     if y > 100 and y < 160: #右前有車
                    #         grid.add(1)

                    # if x_self <= -40 and x_self >= -42 and y >= -80 and y <= 80:
                    #     grid.add(16)
                    # if x_self >= 40 and x_self <= 42 and y >= -80 and y <= 80:
                    #     grid.add(17)
                    if (self.car_pos[0] - car["pos"][0] <= 46 and self.car_pos[0] - car["pos"][0] >= 40) and (self.car_pos[1] - car["pos"][1] < 80 and self.car_pos[1] - car["pos"][1] > -80):
                        grid.add(15)#左有車要撞到了
                    if (self.car_pos[0] - car["pos"][0] <= -40 and self.car_pos[0] - car["pos"][0] >=-46) and (self.car_pos[1] - car["pos"][1] < 80 and self.car_pos[1] - car["pos"][1] > -80):
                        grid.add(16)#右有車要撞到了
                    if x < 35 and x > -35 :#40才不會剛跨過車道就以為前面沒車又跨回去;但設40又會明明前面沒車，卻以為有車卡在車到之間
                        if y > 200 and y < 400:
                            speed_front_ahead = car["velocity"]
                            grid.add(14) #看前方是否有急煞
                        if y > 0 and y < 180: #前方有車
                            grid.add(2)#2用來決定是否要開始換車道
                        elif y < 0 and y > -160: #後方有車
                            grid.add(8)    
                    if x_self < 45 and x_self > -45: 
                        # if(self.car_pos[1] < 450):
                        if y < 130 and y > 0 : #前方有車很近
                            speed_ahead = car["velocity"]
                            grid.add(5) #5用來看是否要煞車
                        # elif(self.car_pos[1] >= 450):
                        #     if y < 10 and y > 0:
                        #         speed_ahead = car["velocity"]
                        #         grid.add(5) 
                    if x > -105 and x < -35 :
                        if y > 100 and y < 160:#右前有車
                            grid.add(3)
                        elif y > 160 and y < 240:
                            grid.add(11)
                        elif y > 240 and y < 320:
                            grid.add(13)                            
                        elif y < -100 and y > -160:#右後有車
                            grid.add(9)
                            speed_behind_right = car["velocity"]
                        elif y < 100 and y > -100:#右方有車
                            grid.add(6)
                    if x < 105 and x > 35:
                        if y > 100 and y < 160:#左前有車
                            grid.add(1)
                        elif y > 160 and y < 240:
                            grid.add(10)
                        elif y > 240 and y < 320:
                            grid.add(12)
                        elif y < -100 and y > -160:#左後有車
                            grid.add(7)
                            speed_behind_left = car["velocity"]
                        elif y < 100 and y > -100:#左方有車
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead, speed_behind_left = speed_behind_left, speed_behind_right = speed_behind_right, speed_front_ahead = speed_front_ahead)
            
        def move(grid, speed_ahead, speed_behind_left, speed_behind_right, speed_front_ahead): 
            if self.player_no == 0:
                print(grid)

            coin_prior = "none"
            for coin in self.coins_pos:
                coin_lane = coin[0]//70
                if((self.car_pos[1] - coin[1] >=0) and self.car_pos[1] - coin[1] <= 360):
                    #if((coin[0] - self.car_pos[0] >= -45) and (coin[0] - self.car_pos[0] <= 25)):
                    if coin_lane == self.car_lane:
                        coin_prior = "mid"
                    #elif(coin[0] - self.car_pos[0] > 25) and (coin[0] - self.car_pos[0] < 95) and coin_prior != "mid": 
                    elif coin_lane == self.car_lane+1 and coin_prior != "mid":
                        coin_prior = "right"
                    #elif(coin[0] - self.car_pos[0] > -115) and (coin[0] - self.car_pos[0] < -45) and coin_prior != "mid":
                    elif coin_lane == self.car_lane-1 and coin_prior != "mid":
                        coin_prior = "left"
            if self.player_no == 0:
                print(coin_prior)

            if len(grid) == 0:
                if coin_prior == "right" :
                    return["SPEED", "MOVE_RIGHT"]
                elif coin_prior == "left" :
                    return["SPEED", "MOVE_LEFT"]
                else:
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :
                        return ["SPEED"]
            else:
                #看遠一點決定優先往哪邊
                if(self.car_pos[0] > 280):
                    prior = "left"
                    if(1 not in grid and 3 not in grid):
                        if(10 not in grid and 11 not in grid):
                            if(12 in grid and 13 not in grid):
                                prior = "right"
                        elif(10 in grid and 11 not in grid):
                            prior = "right"   
                    elif(1 in grid and 3 not in grid):
                        prior = "right"
                else:
                    prior = "right"   
                    if(1 not in grid and 3 not in grid):
                        if(10 not in grid and 11 not in grid):
                            if(13 in grid and 12 not in grid):
                                prior = "left"
                        elif(11 in grid and 10 not in grid):
                            prior = "left"   
                    elif(3 in grid and 1 not in grid):
                        prior = "left" 

                if(4 in grid and 6 in grid):
                    prior = "none"
                elif(4 in grid):
                    prior = "right"
                elif(6 in grid):
                    prior = "left"
                
                if(((len(grid)==1 and 2 in grid) or (len(grid)==2 and 2 in grid and 14 in grid)) and self.car_lane == 4):
                    prior = "left"

                # if(self.player_no == 0):
                #     print(prior)
                if(15 in grid):
                    return["SPEED", "MOVE_RIGHT"]
                elif(16 in grid):
                    return["SPEED", "MOVE_LEFT"]
                if (14 in grid and self.car_vel > speed_front_ahead + 5):
                    if(self.car_pos[0]<280 and  6 not in grid):
                        return ["MOVE_RIGHT"]
                    elif(self.car_pos[0]>280 and 4 not in grid ):
                        return ["MOVE_LEFT"]                                            
                    if self.player_no == 0:
                        print("brake")
                    return ["BRAKE"]
                if (2 not in grid): # Check forward 前方沒車就往前（沒2必沒5)

                    #Back to lane center
                    if coin_prior == "mid":
                        if self.car_pos[0] > self.lanes[self.car_lane]:
                            if self.player_no == 0:
                                print("1")
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0] < self.lanes[self.car_lane]:
                            if self.player_no == 0:
                                print("2")
                            return ["SPEED", "MOVE_RIGHT"]
                        else :
                            if self.player_no == 0:
                                print("3")
                            return ["SPEED"]
                    elif coin_prior == "right" and 6 not in grid and 3 not in grid:
                        return["SPEED", "MOVE_RIGHT"]
                    elif coin_prior == "left" and 4 not in grid and 1 not in grid:
                        return["SPEED", "MOVE_LEFT"]
                    elif coin_prior =="none" and (3 not in grid) and (6 not in grid) and (9 not in grid) and (11 not in grid) and self.car_lane == 0 :
                        return ["SPEED", "MOVE_RIGHT"]
                    elif coin_prior =="none" and (1 not in grid) and (4 not in grid) and (7 not in grid) and(10 not in grid) and self.car_lane == 8:
                        return ["SPEED", "MOVE_LEFT"]
                    else:
                        if self.car_pos[0] > self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0] < self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_RIGHT"]
                        else :
                            return ["SPEED"]

                elif (2 in grid):#前面有車
                    if (5 in grid): # NEED to BRAKE 
                        if(prior == "right"):
                            if (6 not in grid) and speed_behind_right-0.5 <= self.car_vel: # turn right
                                if self.car_vel < speed_ahead - 0.5:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    if self.player_no == 0:
                                        print("brake")
                                    return ["BRAKE", "MOVE_RIGHT"] 

                        elif(prior == "left"):              
                            if (4 not in grid) and speed_behind_left-0.5 <= self.car_vel: # turn left 
                                if self.car_vel < speed_ahead - 0.5:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    if self.player_no == 0:
                                        print("brake")
                                    return ["BRAKE", "MOVE_LEFT"] 

                        if self.car_vel < speed_ahead - 0.5:  # BRAKE
                            return ["SPEED"]
                        else:
                            if self.player_no == 0:
                                print("brake")
                            return ["BRAKE"]                                                                                        
                    #2有車但5沒車
                    #此段讓車子優先往左，可修改  
                    elif(5 not in grid): 
                        # if(self.car_vel > speed_ahead+3 ):
                        #     if self.player_no == 0:
                        #         print("brake")
                        #     return ["BRAKE"]
                        # if(1 in grid and 3 in grid):#測試
                        #     if self.player_no == 0:
                        #         print("brake")
                        if (prior == "right"):
                            if(6 not in grid):
                                if(9 in grid):
                                    if(self.car_vel >= speed_behind_right):
                                        if (self.car_pos[0] < 60 ):
                                            return ["SPEED", "MOVE_RIGHT"]
                                        return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    if (self.car_pos[0] < 60 ):
                                        return ["SPEED", "MOVE_RIGHT"]
                                    return ["SPEED", "MOVE_RIGHT"]
                            # elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right 右完全沒車
                            #     if(self.player_no == 0):
                            #         print('2有車右完全沒車')
                            #     return ["SPEED", "MOVE_RIGHT"]
                            # elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 左完全沒車
                            #     if(self.player_no == 0):
                            #         print('2有車左完全沒車') 
                            #     return ["SPEED", "MOVE_LEFT"]   
                            # elif (3 not in grid) and (6 not in grid): # turn right 右前及右沒車
                            #     if(self.player_no == 0):   
                            #         print('2有車右前、右沒車')
                            #     return ["SPEED", "MOVE_RIGHT"]
                            # elif (1 not in grid) and (4 not in grid): # turn left 左前及左沒車
                            #     if(self.player_no == 0):
                            #         print('2有車左前、左沒車')
                            #     return ["SPEED", "MOVE_LEFT"]                                
                            # elif (6 not in grid) and (9 not in grid): # turn right 右後及右沒車
                            #     if(self.player_no == 0):
                            #         print('2有車右後、右沒車')
                            #     return ["MOVE_RIGHT"] 
                            # elif (4 not in grid) and (7 not in grid): # turn left 左後及左沒車
                            #     if(self.player_no == 0):
                            #         print('2有車左後、左沒車')
                            #     return ["MOVE_LEFT"]    

                        elif (prior == "left"):
                            if(4 not in grid):
                                if(7 in grid):
                                    if(self.car_vel >= speed_behind_left):
                                        if (self.car_pos[0] > 560 ):
                                            return ["SPEED", "MOVE_LEFT"]                                        
                                        return ["SPEED", "MOVE_LEFT"]
                                else:
                                    if (self.car_pos[0] > 560 ):
                                        return ["SPEED", "MOVE_LEFT"]
                                    return ["SPEED", "MOVE_LEFT"]
                            # elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 左完全沒車
                            #     if(self.player_no == 0):
                            #         print('2有車左完全沒車') 
                            #     return ["SPEED", "MOVE_LEFT"]
                            # elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right 右完全沒車
                            #     if(self.player_no == 0):
                            #         print('2有車右完全沒車')
                            #     return ["SPEED", "MOVE_RIGHT"]
                            # elif (1 not in grid) and (4 not in grid): # turn left 左前及左沒車
                            #     if(self.player_no == 0):
                            #         print('2有車左前、左沒車')
                            #     return ["SPEED", "MOVE_LEFT"]
                            # elif (3 not in grid) and (6 not in grid): # turn right 右前及右沒車
                            #     if(self.player_no == 0):
                            #         print('2有車右前、右沒車')
                            #     return ["SPEED", "MOVE_RIGHT"]
                            # elif (4 not in grid) and (7 not in grid): # turn left 左後及左沒車
                            #     if(self.player_no == 0):
                            #         print('2有車左後、左沒車')
                            #     return ["MOVE_LEFT"]    
                            # elif (6 not in grid) and (9 not in grid): # turn right 右後及右沒車
                            #     if(self.player_no == 0):
                            #         print('2有車右後、右沒車')
                            #     return ["MOVE_RIGHT"]
                        else:
                            if self.car_pos[0] > self.lanes[self.car_lane]:
                                return ["SPEED", "MOVE_LEFT"]
                            elif self.car_pos[0] < self.lanes[self.car_lane]:
                                return ["SPEED", "MOVE_RIGHT"]
                            else :
                                return ["SPEED"]
        
        if len(scene_info[self.player]) != 0:#如果len==0代表自己的這台車不在畫面中就不會讀取了
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:#從所有車輛中找到self的car，並儲存自身的速度
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70 #計算賽道
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass