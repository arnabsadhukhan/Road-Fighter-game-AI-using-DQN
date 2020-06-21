
import pygame
import os
import cv2
import numpy as np
import time



class collide_car:
    def __init__(self,image_name):
        self.car = pygame.image.load(image_name)
        self.car_img = pygame.transform.scale(self.car, (window_size[0]//10, window_size[0]//9))
        self.size = (window_size[0]//10, window_size[0]//9)
        self.x = int(np.random.uniform(low=left_max,high=right_max-self.size[0],size=1)[0])
        self.y = 0
    def get_pos(self):
        return (x,y)


pygame.init()
info = pygame.display.Info()
W ,H = info.current_w,info.current_h
white = (255,255,255)
green = (0, 255, 0) 
blue = (0, 0, 128) 
font = pygame.font.Font('freesansbold.ttf', 32) 
font2 = pygame.font.Font('freesansbold.ttf', 64) 


score = font.render('Score', True,white) 
Crashed = font2.render('Crashed', True,white) 




#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (W-W//3,0)
gameDisplay = pygame.display.set_mode((W//3,H))

window_size = (W//3,H)

pygame.display.set_caption('Road Fighter')

left_max =  window_size[0]//7
right_max = int((window_size[0]//7)*5.5)

frame = cv2.imread('images/road.png')
frame=np.rot90(frame)
frame = cv2.resize(frame,(window_size[1],window_size[0]))

player_car = pygame.image.load("images/red_car.png")
player_car = pygame.transform.scale(player_car, (window_size[0]//10, window_size[0]//9))
player_car_size = (window_size[0]//12, window_size[0]//14)
player_car_pos = window_size[0]//2
player_car_x = window_size[0]//2
player_car_y = int(H*2/3)



no_yellow_cars=5
no_blue_cars = 1

blue_cars= []
yellow_cars = []
for i in range(no_yellow_cars+no_blue_cars):
    
    if i<no_yellow_cars:
        temp_obj = collide_car("images/yellow_car.png")
        temp_obj.y=(i*window_size[1]//(no_yellow_cars+no_blue_cars))*-1
        yellow_cars.append(temp_obj)
    else:
        temp_obj = collide_car("images/blue_car.png")
        temp_obj.y=(i*window_size[1]//(no_yellow_cars+no_blue_cars))*-1
        blue_cars.append(temp_obj)



flag =0
clock = pygame.time.Clock()
crashed = False
 
speed = 5
count=0
car_shift=30

crash_count =0

while not crashed:
    count+=1
    start =time.time()    
    #spawn car ----------------------------------------------------------------------------------
    for yellow_car in yellow_cars:
        if yellow_car.y<window_size[1]:
            yellow_car.y+=speed//2
        else:
            yellow_car.y=-30
            yellow_car.x = int(np.random.uniform(low=left_max,high=right_max-yellow_car.size[0],size=1)[0])
    for blue_car in blue_cars:
        if blue_car.y<window_size[1]:
            blue_car.y+=speed//2
        else:
            blue_car.y=-30
            blue_car.x = int(np.random.uniform(low=left_max,high=right_max-blue_car.size[0],size=1)[0])
        if blue_car.y>(player_car_y-2*player_car_size[1]) and blue_car.y<(player_car_y+player_car_size[1]):
            if blue_car.x<player_car_x:  
                if blue_car.x+1>left_max: 
                    blue_car.x+=1
            else:
                if blue_car.x-1<right_max: 
                    blue_car.x-=1
    #spawn car ----------------------------------------------------------------------------------
    

    #keyboard control ---------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        	crashed = True
        
        if event.type == pygame.KEYUP:
            if event.key==276 :
                #print("left key pressed",end='\r')
                for i in range(car_shift//2):
                	player_car_pos-=2
                	gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
                	pygame.display.update()

            if event.key==275:
                #print("right key pressed",end='\r')
                for i in range(car_shift//2):
                	player_car_pos+=2
                	gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
                	pygame.display.update()
               
    #keyboard control ---------------------------------------------------------------------------
    player_car_x = player_car_pos
    
    
    
            
    #background-----------------------------------------------------------------
    frame = np.roll(frame,speed,axis=1)
    img = pygame.surfarray.make_surface(frame)
    gameDisplay.blit(img,(0,0))
    #background-----------------------------------------------------------------
    
    
    # blit all cars ------------------------------------------------------------
    gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
    for yellow_car in yellow_cars:
        gameDisplay.blit(yellow_car.car_img,(yellow_car.x,yellow_car.y))
    for blue_car in blue_cars:
        gameDisplay.blit(blue_car.car_img,(blue_car.x,blue_car.y))
    # blit all cars ------------------------------------------------------------
    
    
    #crash detection-----------------------------------------------------------
    #with border
    if player_car_pos<=left_max or player_car_pos+player_car_size[0]>=right_max:
        crash_count+=1
        player_car_pos = window_size[0]//2

    #with cars
    for yellow_car in yellow_cars+blue_cars:
        if player_car_x>yellow_car.x and player_car_x<yellow_car.x+yellow_car.size[0] and player_car_y>yellow_car.y and player_car_y<yellow_car.y+yellow_car.size[1]:
            crash_count+=1
            player_car_pos = window_size[0]//2
            
        elif player_car_x+player_car_size[0]>yellow_car.x and player_car_x+player_car_size[0]<yellow_car.x+yellow_car.size[0] and player_car_y>yellow_car.y and player_car_y<yellow_car.y+yellow_car.size[1]:
            crash_count+=1
            player_car_pos = window_size[0]//2

        elif player_car_x+player_car_size[0]>yellow_car.x and player_car_x+player_car_size[0]<yellow_car.x+yellow_car.size[0] and player_car_y+player_car_size[1]>yellow_car.y and player_car_y+player_car_size[1]<yellow_car.y+yellow_car.size[1]:
            crash_count+=1
            player_car_pos = window_size[0]//2
                
        if player_car_x>yellow_car.x and player_car_x<yellow_car.x+yellow_car.size[0] and player_car_y+player_car_size[1]>yellow_car.y and player_car_y+player_car_size[1]<yellow_car.y+yellow_car.size[1]:
            crash_count+=1
            player_car_pos = window_size[0]//2
    #crash detection-----------------------------------------------------------
    
    if crash_count>0:
    	pygame.display.update()
    	Score = font.render(f'Score:{count}', True,white) 
    	gameDisplay.blit(Score, (0,0)) 
    	Crashed = font.render(f'Crashed quit in 3 sec', True,white) 
    	text_rect = Crashed.get_rect(center=(window_size[0]/2, window_size[1]/2))
    	gameDisplay.blit(Crashed, text_rect) 
    	pygame.display.update()
    	crashed = True
    	time.sleep(3)

    Score = font.render(f'Score:{count}', True,white) 
    gameDisplay.blit(Score, (0,0)) 
    
    pygame.display.update()
    print(f"time:{np.round(time.time()-start,4)} fps:{int(1/(time.time()-start))}        ",end='\r')
pygame.quit()

