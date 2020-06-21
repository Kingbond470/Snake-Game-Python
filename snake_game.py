import pygame
import random
import os

#addding music
pygame.mixer.init()


pygame.init()
screen_width=1200
screen_heigth=600
pygame.display.set_caption("snake game")
gameWindow=pygame.display.set_mode((screen_width,screen_heigth))
#background image
bgimg=pygame.image.load("bg_snake.jpg")
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_heigth)).convert_alpha()

pygame.display.update()
clock=pygame.time.Clock()
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
font=pygame.font.SysFont(None,55)



def text_screen(text,color,x,y):
	screen_text=font.render(text,True,color)
	gameWindow.blit(screen_text,[x,y])

#used to solve the continuously growing snake during game (without removing its earlier part....solved)
def plot_snake(gameWindow,color,snk_list,snake_size):
	for x,y in snk_list:
		pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

def welcome():
	exit_game=False
	bgimg1=pygame.image.load("bg.jpg")
	bgimg1=pygame.transform.scale(bgimg1,(screen_width,screen_heigth)).convert_alpha()   #convert alpha is used,so that it wont affect the game during again again... loading
	while not exit_game:
		gameWindow.fill(white)
		gameWindow.blit(bgimg1,(0,0))
		text_screen("Welcome to Ludo - Snake Game by KingbondL",black,260,250)
		text_screen("Press Space to Play",black,260,300)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				exit_game=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE:
					pygame.mixer.music.load('back.mp3')
					pygame.mixer.music.play()
					gameloop()

			pygame.display.update()
			clock.tick(60)
#game loop
def gameloop():

	exit_game=False
	game_over=False
	snake_x=65
	snake_y=75
	snake_size=10
	fps=60
	with open("highscore_stored.txt","r") as f:
		highscore=f.read()  #file will give values as string

	init_velocity=10
	velocity_x=2
	velocity_y=2
	food_x=random.randint(20,screen_width/2)
	food_y=random.randint(20,screen_heigth/2)
	score=0
	snk_list=[]
	snk_length=1
	#to check the file exists or not
	if(not os.path.exists("highscore_stored.txt")):
		with open("highscore_stored.txt","w") as f:
			f.write("0")

	while not exit_game:
		if game_over:
			gameWindow.fill(white)
			with open("highscore_stored.txt","w") as f:
				f.write(str(highscore))
			text_screen("Game Over!Enter to continue",red,250,250)


			for event in pygame.event.get():
				#to quit the game from cross button
				if event.type==pygame.QUIT:
					exit_game=True

			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_RETURN:
					gameloop()
		else:
			for event in pygame.event.get():
				head=[]
				head.append(snake_x)
				head.append(snake_y)
				snk_list.append(head)
				snake_x=snake_x+velocity_x
				snake_y=snake_y+velocity_y
				#to quit the game from cross button
				if event.type==pygame.QUIT:
					exit_game=True

				#to check that user has pressed any key
				if event.type==pygame.KEYDOWN:     
					#to check that user has pressed the right arrow key 
					if event.key==pygame.K_RIGHT:
						#increase the value by 10    
						velocity_x=init_velocity
						velocity_y=0
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_LEFT:
						velocity_x= -init_velocity
						velocity_y=0

				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_UP:
						velocity_y=-init_velocity
						velocity_x=0

				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_DOWN:
						velocity_y=init_velocity
						velocity_x=0

				#just little change
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_a:
						velocity_y=init_velocity
						velocity_x=init_velocity
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_s:
						velocity_y=-init_velocity
						velocity_x=-init_velocity
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_q:
						score+=10	

				#if head include in list then game should be over	
				if head in snk_list[:-1]:
					game_over=True
					pygame.mixer.music.load('game_over.mp3')
					pygame.mixer.music.play()
				if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:
					score+=10
					food_x=random.randint(20,screen_width/2)
					food_y=random.randint(20,screen_heigth/2)
					snk_length+=5
					if score>int(highscore):
						highscore=score
			
				
			#filling the color of screen with white
			gameWindow.fill(white)
			gameWindow.blit(bgimg,(0,0))
			text_screen("Score: "+str(score)+"    High score: "+str(highscore),red,50,50)
			#pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])
			pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])

			if len(snk_list)>snk_length:
				del snk_list[0]             #to check that if co-ordinate of head and others meet at same then game should be over
			
			if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_heigth:
				game_over=True
				pygame.mixer.music.load('game_over.mp3')
				pygame.mixer.music.play()
				
			plot_snake(gameWindow,black,snk_list,snake_size)	
		clock.tick(fps)
		pygame.display.update() #to update the screen after every clock tick 

	pygame.quit()
	quit()
welcome()
gameloop()