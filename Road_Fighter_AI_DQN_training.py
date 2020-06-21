import pygame
import os
import cv2
import numpy as np
import time
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Dense,Flatten
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2 


pygame.init()
info = pygame.display.Info()
W ,H = info.current_w,info.current_h
white = (255,255,255)
green = (0, 255, 0) 
blue = (0, 0, 128) 


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (W-W//3,50)
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
player_car_size = (window_size[0]//12, window_size[0]//11)
player_car_pos = window_size[0]//2
player_car_x = window_size[0]//2
player_car_y = int(H*2/3)



class collide_car:
    def __init__(self):
        self.car = pygame.image.load("images/blue_car.png")
        self.car_img = pygame.transform.scale(self.car, (window_size[0]//10, window_size[0]//9))
        self.size = (window_size[0]//10, window_size[0]//9)
        self.x = int(np.random.uniform(low=left_max,high=right_max-self.size[0],size=1)[0])
        self.y = 0
    def get_pos(self):
        return (x,y)

def get_state():
    state =[player_car_x,player_car_y,player_car_x+player_car_size[0],player_car_y,player_car_x,player_car_y+player_car_size[1],player_car_x+player_car_size[0],player_car_y+player_car_size[1]]
    for blue_car in blue_cars:
        #if blue_car.y>(player_car_y-8*player_car_size[1]) and blue_car.y<(player_car_y+2*player_car_size[1]):
        state+=[blue_car.x,blue_car.y,blue_car.x+blue_car.size[0],blue_car.y,blue_car.x,blue_car.y+blue_car.size[1],blue_car.x+blue_car.size[0],blue_car.y+blue_car.size[1]]
            
    return np.array(state)/700

no_blue_cars=5

blue_cars = []
for i in range(no_blue_cars):
    temp_obj = collide_car()
    temp_obj.y=(i*window_size[1]//no_blue_cars)*-1
    blue_cars.append(temp_obj)

clock = pygame.time.Clock()
crashed = False
 
speed = 10
count=0
car_shift=10

discount_factor =0.95
learning_rate =0.5
reward_val=10
crash_count =0

train_image_size = (right_max-left_max,int(H)-int(H//4),1)

X = []
y = []

model = Sequential()
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dense(126))
model.add(Dense(3))



#comment the below line if you want to train a model
model = load_model('Trained_models/model-v1.model')
model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])

#print(model.summary())

l= len(get_state())
print(window_size)


old_reward = 0
while not crashed:
    #count+=1
    start =time.time()
    reward = 1
    
    current_state = get_state()
    temp_state = current_state
    pred_prev = model.predict(current_state[np.newaxis,...,np.newaxis])[0]
    current_action  = np.argmax(pred_prev)
    current_q_value = pred_prev[current_action]
    
    #spawn car ----------------------------------------------------------------------------------
    for blue_car in blue_cars:
        if blue_car.y<window_size[1]:
            blue_car.y+=speed//2
        else:
            blue_car.y=-30
            blue_car.x = int(np.random.uniform(low=left_max,high=right_max-blue_car.size[0],size=1)[0])
    #spawn car ----------------------------------------------------------------------------------
    

    #keyboard control ---------------------------------------------------------------------------
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        	crashed = True
        
        if event.type == pygame.KEYUP:
            if event.key==276 or current_action==0:
                #print("left key pressed",end='\r')
                player_car_pos-=car_shift
                gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
                #pygame.display.update()

            if event.key==275 or current_action==2:
                #print("right key pressed",end='\r')
                player_car_pos+=car_shift
                gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
                #pygame.display.update()
                
    #keyboard control ---------------------------------------------------------------------------
    if current_action==0:
        #print("left key pressed",end='\r')
        player_car_pos-=car_shift
        if player_car_pos<left_max:
        	player_car_pos =max(left_max,player_car_pos) 
        gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
        #pygame.display.update()

    if current_action==1:
    	pass
        #print("middle key pressed",end='\r')

    if current_action==2:
        #print("right key pressed",end='\r')
        player_car_pos+=car_shift
        if player_car_pos+player_car_size[0]>right_max:
        	player_car_pos =min(right_max-player_car_size[0],player_car_pos) 
        gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
        #pygame.display.update()
    player_car_x = player_car_pos
    
     
    #background-----------------------------------------------------------------
    frame = np.roll(frame,speed,axis=1)
    
    img = pygame.surfarray.make_surface(frame)
    gameDisplay.blit(img,(0,0))
    #background-----------------------------------------------------------------
    
    
    # blit all cars ------------------------------------------------------------
    gameDisplay.blit(player_car,(player_car_pos,int(H*2/3)))
    for blue_car in blue_cars:
        gameDisplay.blit(blue_car.car_img,(blue_car.x,blue_car.y))
    # blit all cars ------------------------------------------------------------
    
    
    #crash detection-----------------------------------------------------------
    #with border
    if player_car_pos<=left_max or player_car_pos+player_car_size[0]>=right_max:
        crash_count+=1
        #print(f"crashed:{crash_count}",end='\r')
        reward = -1*reward_val
    #with cars
    for blue_car in blue_cars:
        if player_car_x>blue_car.x and player_car_x<blue_car.x+blue_car.size[0] and player_car_y>blue_car.y and player_car_y<blue_car.y+blue_car.size[1]:
            crash_count+=1
            #print(f"crashed:{crash_count}block1",end='\r')
            reward = -1*reward_val
            
        elif player_car_x+player_car_size[0]>blue_car.x and player_car_x+player_car_size[0]<blue_car.x+blue_car.size[0] and player_car_y>blue_car.y and player_car_y<blue_car.y+blue_car.size[1]:
            crash_count+=1
            #print(f"crashed:{crash_count}block2",end='\r')
            reward = -1*reward_val
            
        elif player_car_x+player_car_size[0]>blue_car.x and player_car_x+player_car_size[0]<blue_car.x+blue_car.size[0] and player_car_y+player_car_size[1]>blue_car.y and player_car_y+player_car_size[1]<blue_car.y+blue_car.size[1]:
            crash_count+=1
            #print(f"crashed:{crash_count}block3",end='\r')
            reward = -1*reward_val
           
        if player_car_x>blue_car.x and player_car_x<blue_car.x+blue_car.size[0] and player_car_y+player_car_size[1]>blue_car.y and player_car_y+player_car_size[1]<blue_car.y+blue_car.size[1]:
            crash_count+=1
            #print(f"crashed:{crash_count}block4",end='\r')   
            reward = -1*reward_val
    #crash detection-----------------------------------------------------------
    
    
    #model train--------------------------------
    new_state = get_state()
    pred = model.predict(new_state[np.newaxis,...,np.newaxis])[0]
    new_max_q  = np.max(pred)
    
    new_modified_q = (1-learning_rate)*current_q_value + learning_rate * (reward +discount_factor* new_max_q)
    pred_prev[current_action]=new_modified_q
    
    X.append(current_state)
    y.append(pred_prev)
   
    #train every 200 frames
    if len(X)>=200:
        count=0
        X = np.array(X).reshape(-1,l,1)
        y = np.array(y).reshape(-1,3)
        
        model.fit(X,y,batch_size =2,epochs=30,shuffle=True)
        model.save('model-v1.model')
        X=[]
        y=[]
    
    #print(f"\n{temp_state}\npred_prev:{pred_prev} current_action:{current_action} current_q_value :{current_q_value} reward:{reward} new_max_q:{new_max_q} new_modified_q:{new_modified_q}",end='\n')   
    #print(f"reward:{reward}  ",end='\r')

    #model train--------------------------------

    old_reward = reward

    
    pygame.display.update()
    clock.tick(120)
    print(f"time:{np.round(time.time()-start,4)} fps:{int(1/(time.time()-start))} count:{count}         ",end='\r')
pygame.quit()

