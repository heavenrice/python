import pygame as pg
from pygame.constants import QUIT,K_DOWN,K_UP,K_LEFT,K_RIGHT,K_SPACE,K_ESCAPE
import random
import os
from pygame import mixer

pg.init()
mixer.init()
WIDTH=900;HEIGHT=506 #SD
main_display=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("BanderoGoose v1.1")

C_ORANGE=(250,200,0);C_BLACK=(0,0,0)
C_F=(50,50,255);C_M=(0,50,250)
SIZE1=(20,20);SIZE2=(30,30)
s_font=pg.font.SysFont("Arial",30)
bg=pg.image.load('bg2.png')
bg=pg.transform.scale(bg,(WIDTH,HEIGHT))
bx1=0;bx2=bg.get_width();bg_move=1
main_display.blit(bg,(bx1,0))
main_display.blit(s_font.render("Press ''SPACE'' to start.",True,C_BLACK),(round(WIDTH/2,0),round(HEIGHT/2,0)))

SIZE1=(20,20);SIZE2=(30,30)
player=pg.image.load('player.png').convert_alpha()
player=pg.transform.scale(player,(91,38))
RECT1=player.get_rect().move((round(WIDTH/2,0)-111,round(HEIGHT/2,0)))
SPEED1=pg.time.Clock() #FPS

p_life=pg.Surface((WIDTH,3))
PR_LIFE=player.get_rect() #LIFE BAR
p_life.fill((250,0,0));lwidth=WIDTH
p_bonus=pg.Surface((0,4))
PR_BONUS=player.get_rect().move((0,3)) #BONUS BAR
p_bonus.fill((0,150,50));bwidth=WIDTH

def new_enemy():
    enemy=pg.image.load('enemy.png').convert_alpha()
    enemy=pg.transform.scale(enemy,(61,21))
    # E_RECT=pg.Rect(WIDTH,random.randint(0,HEIGHT),*enemy_size)
    E_RECT=pg.Rect(WIDTH,random.randint(RECT1.top-50,RECT1.top+50),*enemy.get_size())
    E_MOVE=[-1*random.randint(2,10),0]
    E_BACK=[5,0]
    return [enemy,E_RECT,E_MOVE,E_BACK]
NEW_ENEMY=pg.USEREVENT+1
pg.time.set_timer(NEW_ENEMY,random.randint(900,1200))
enemies=[]

def new_bonus():
    bonus=pg.image.load('bonus.png').convert_alpha()
    bonus=pg.transform.scale(bonus,(53,89))
    B_RECT=pg.Rect(random.randint(0,WIDTH),0,*bonus.get_size())
    B_MOVE=[0,random.randint(1,2)]
    return [bonus,B_RECT,B_MOVE]
NEW_BONUS=pg.USEREVENT+2
pg.time.set_timer(NEW_BONUS,random.randint(700,1000))
bonuses=[]

ipath="C:\Python\game\pics\goose"
player_images=os.listdir(ipath)
change_image=pg.USEREVENT+3
pg.time.set_timer(change_image,200)
image_index=0

mixer.music.set_volume(0.1)
# mixer.music.load("C:\Downloads\dvf.mp3")
# mixer.music.play(-1)
boom=mixer.Sound("C:\Windows\Media\Windows Critical Stop.wav")
ding=mixer.Sound("C:\Windows\Media\Windows Hardware Remove.wav")
gend3=mixer.Sound("C:\Windows\Media\Windows Notify Calendar.wav")
gend2=mixer.Sound("C:\Windows\Media\Windows Hardware Insert.wav")

e=0;b=0;pm=3;score=0;life=10
left_side=False;fly=False
playing=True;nopause=False #True

while playing: #START
    SPEED1.tick(200)
    keys=pg.key.get_pressed()
    if keys[K_ESCAPE]:
        playing=False
    for event in pg.event.get():
        if event.type==QUIT:
            playing=False
        if nopause: #SPACE BUTON
            if event.type==NEW_ENEMY:
                enemies.append(new_enemy());e+=1
            if event.type==NEW_BONUS:
                bonuses.append(new_bonus());b+=1
            if event.type==change_image:
                player=pg.image.load(os.path.join(ipath,player_images[image_index]))
                player=pg.transform.scale(player,(91,38))
                image_index+=1
                if image_index>=len(player_images):
                    image_index=0
                if left_side:
                    player=pg.transform.flip(player,True,False)
                if fly:
                    pg.time.set_timer(change_image,50)
                else:
                    pg.time.set_timer(change_image,200)

    if nopause: #SPACE BUTON
        bx1-=bg_move;bx2-=bg_move
        if bx1<-bg.get_width():
            bx1=bg.get_width()
        if bx2<-bg.get_width():
            bx2=bg.get_width()
        main_display.blit(bg,(bx1,0))
        main_display.blit(bg,(bx2,0))

    if keys[K_SPACE]: #PRESS SPACE BUTON
        nopause=not nopause
        main_display.blit(s_font.render("Press ''SPACE'' to start.",True,C_BLACK),(round(WIDTH/2,0),round(HEIGHT/2,0)))
    if nopause: #SPACE BUTON
        if keys[K_UP] and RECT1.top>0:
            RECT1=RECT1.move([0,-1*(pm+1)])
        if keys[K_DOWN] and RECT1.bottom<=HEIGHT:
            RECT1=RECT1.move([0,1*pm])
        if keys[K_LEFT] and RECT1.left>0:
            RECT1=RECT1.move([-1*(pm*2),0])
            left_side=True
        if keys[K_RIGHT] and RECT1.right<=WIDTH:
            RECT1=RECT1.move([1*(pm*2),0])
            left_side=False
        if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
            fly=True
        else:
            fly=False

    main_display.blit(p_life,PR_LIFE)
    main_display.blit(p_bonus,PR_BONUS)
    main_display.blit(player,RECT1)
    main_display.blit(s_font.render("♥ "+str(life)+" / ♦ "+str(score)+" $"+str(bwidth),True,C_BLACK),(10,10))

    if nopause: #SPACE BUTON
        if RECT1.bottom<=HEIGHT:
            RECT1=RECT1.move([0,1])
        for enemy in enemies:
            enemy[1]=enemy[1].move(enemy[2])
            main_display.blit(enemy[0],enemy[1])
            if RECT1.colliderect(enemy[1]):
                mixer.Channel(1).play(boom)
                enemies.pop(enemies.index(enemy))
                life-=1;lwidth-=90
                p_life=pg.Surface((lwidth,3))
                p_life.fill((255,0,0))
                # if life<3:
                #     mixer.Channel(1).play(gend3)
                if life<2:
                    mixer.Channel(1).play(gend2)
                if life<1:
                    # playing=False
                    # START OVER
                    mixer.Channel(1).play(gend3)
                    life=10;lwidth=WIDTH;score=0;e=0;b=0
                    p_life=pg.Surface((lwidth,3))
                    p_life.fill((255,0,0))
                    for enemy in enemies:
                        enemies.pop(enemies.index(enemy))
                    for bonus in bonuses:
                        bonuses.pop(bonuses.index(bonus))
        for bonus in bonuses:
            bonus[1]=bonus[1].move(bonus[2])
            main_display.blit(bonus[0],bonus[1])
            if RECT1.colliderect(bonus[1]):
                mixer.Channel(2).play(ding)
                bonuses.pop(bonuses.index(bonus));score+=1
                bwidth=round(WIDTH/b*score,0)
                p_bonus=pg.Surface((bwidth,4))
                p_bonus.fill((0,150,50))
                # rockerts elimination with bonuses

        for enemy in enemies:
            if enemy[1].left<0:
                enemies.pop(enemies.index(enemy))
        for bonus in bonuses:
            if bonus[1].bottom>HEIGHT:
                bonuses.pop(bonuses.index(bonus))
    else:
        for enemy in enemies:
            main_display.blit(enemy[0],enemy[1])
        for bonus in bonuses:
            main_display.blit(bonus[0],bonus[1])

    pg.display.flip() #REFRESH